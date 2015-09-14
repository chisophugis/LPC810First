from __future__ import print_function

# stty -F /dev/ttyUSB0 115200 -echo raw

import struct

import serial

def main():

    ser = serial.Serial('/dev/ttyUSB0')

    # See UM10601: "LPC81x User manual"
    # 21.6.2 Boot process

    ser.write('?')
    s = ser.readline()
    assert s.strip() == 'Synchronized'

    w = lambda s: write_with_echo(ser, s + '\r\n')
    w('Synchronized')
    s = ser.readline()
    assert s.strip() == 'OK'

    w('12000')
    s = ser.readline()
    print('Read: {!r}'.format(s))
    assert s == 'OK\r\n'

    uid = cmd_N(ser)
    print(uid)

    bootcode_version = cmd_K(ser)
    print(bootcode_version)

    cmd_U(ser)

    ADDR = 0x10000000
    cmd_W(ser, ADDR, 'UAUA')
    mem = cmd_R(ser, ADDR, 4)
    print('Memory was: {!r}'.format(mem))
    assert mem == 'UAUA'

    def h(s):
        clean = s.replace('_', '')
        assert len(clean) == 16
        return int(clean, base=2)
    p = struct.pack
    ph = lambda x: p('<H', h(x))
    pw = lambda x: p('<I', x)
    code = [
    #0x1000_0000: - base of SRAM
    #  01001_000_00000010 ; ldr r0, dir0
        '01001_000_00000010',
    #  01001_001_00000011 ; ldr r1, not0
        '01001_001_00000011',
    #0x1000_0004 - i.e 4 - i.e. 1 word
    #  01001_010_00000011 ; ldr r2, pi0_3_mask
        '01001_010_00000011',
    #  01100_00000_000_010 ; str r2, [r0]
        '01100_00000_000_010',
    #0x1000_0008 - loop: - 8 i.e. 2 words
    #  01100_00000_001_010 ; str r2, [r1]
        '01100_00000_001_010',
    #  11100_11111111101 ; b loop
        '11100_11111111101'
    ]
    image = ''
    image += ''.join(ph(x) for x in code)

    consts = [
    #0x1000_000C - dir0: i.e. 12 - i.e. 3 words
    #0xA000_2000 ; dir0
        0x4006401C, # HACK: USART0 TXDATA
        #0xA0002000,
    #0x1000_0010 - not0: i.e. 16 - i.e. 4 words
    #0xA000_2300 ; not0
        0x4006401C, # HACK: USART0 TXDATA
        #0xA0002300,
    #0x1000_0014 - pi0_3_mask: i.e. 20 - i.e. 5 words
    #0x0000_0008 ; pi0_3_mask
        0x0000003F # HACK: whatever character I want
    ]

    image += ''.join(pw(x) for x in consts)

    cmd_W(ser, ADDR, image)
    image_read = cmd_R(ser, ADDR, len(image))
    assert image_read == image

    cmd_G(ser, ADDR)



def write_with_echo(ser, s):
    print('write_with_echo(ser, {!r})'.format(s))
    print(' '*8 + 'sent: {!r}'.format(s))
    ser.write(s)
    echoed = ser.readline()
    print(' '*8 + 'echo: {!r}'.format(echoed))
    assert echoed == s


# See UM10601: "LPC81x User manual"
# 22.5.1 "UART ISP commands"

def cmd_N(ser):
    w = lambda s: write_with_echo(ser, s + '\r\n')
    w('N')
    s = ser.readline()
    assert s == '0\r\n' # CMD_SUCCESS == 0
    l = []
    for i in range(4):
        line = ser.readline()
        l.append(int(line.strip()))
    return l

def cmd_K(ser):
    w = lambda s: write_with_echo(ser, s + '\r\n')
    w('K')
    s = ser.readline()
    assert s == '0\r\n' # CMD_SUCCESS == 0
    ret = []
    for i in range(2):
        line = ser.readline()
        ret.append(int(line.strip()))
    return ret

def cmd_U(ser):
    w = lambda s: write_with_echo(ser, s + '\r\n')
    w('U 23130')
    s = ser.readline()
    assert s == '0\r\n' # CMD_SUCCESS == 0

def cmd_W(ser, addr, bs):
    assert isinstance(addr, int)
    length = len(bs)
    assert length % 4 == 0

    w = lambda s: write_with_echo(ser, s + '\r\n')
    w('W {} {}'.format(addr, length))
    s = ser.readline()
    assert s == '0\r\n' # CMD_SUCCESS == 0

    ser.write(bs)
    s = ser.read(len(bs))
    assert s == bs
    # Contrary to the docs, I'm not seeing a returned "OK<CR><LF>" after
    # the raw bytes are sent.

def cmd_R(ser, addr, length):
    assert length % 4 == 0

    w = lambda s: write_with_echo(ser, s + '\r\n')
    w('R {} {}'.format(addr, length))
    s = ser.readline()
    assert s == '0\r\n' # CMD_SUCCESS == 0

    s = ser.read(length)
    return s

def cmd_G(ser, addr):
    assert addr % 4 == 0

    w = lambda s: write_with_echo(ser, s + '\r\n')
    w('G {} T'.format(addr))

main()
