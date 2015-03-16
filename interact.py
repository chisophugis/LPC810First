from __future__ import print_function

# stty -F /dev/ttyUSB0 115200 -echo raw

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



main()
