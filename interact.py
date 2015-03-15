from __future__ import print_function

# stty -F /dev/ttyUSB0 115200 -echo raw

import serial

def main():

    ser = serial.Serial('/dev/ttyUSB0')

    # See UM10601 "LPC81x User manual"
    # 21.6.2 Boot process

    ser.write('?')
    s = ser.readline()
    print('Read: {!r}'.format(s))
    assert s.strip() == 'Synchronized'

    ser.write('Synchronized\r\n')
    s = ser.readline()
    print('Read: {!r}'.format(s))
    assert s == 'Synchronized\r\n'
    s = ser.readline()
    print('Read: {!r}'.format(s))
    assert s.strip() == 'OK'

    ser.write('12000\r\n')
    s = ser.readline()
    print('Read: {!r}'.format(s))
    assert s == '12000\r\n'
    s = ser.readline()
    print('Read: {!r}'.format(s))
    assert s == 'OK\r\n'

    ser.write('N\r\n')
    s = ser.readline()
    print('Read: {!r}'.format(s))
    assert s == 'N\r\n'
    s = ser.readline()
    assert s == '0\r\n' # CMD_SUCCESS == 0
    l = []
    for i in range(4):
        s = ser.readline()
        l.append(int(s.strip()))
    print([hex(x) for x in l])

main()
