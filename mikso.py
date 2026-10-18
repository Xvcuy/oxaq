#!/usr/bin/env python3

"""Builds a bootable El Torito ISO (1.44 MB floppy emulation) from a raw floppy image.

Usage: python3 mkiso.py oxaq12.img oxaq12.iso"""

import struct, sys, time



src, dst = sys.argv[1], sys.argv[2]

img = open(src, 'rb').read()

SEC = 2048

img_secs = (len(img) + SEC - 1) // SEC

PVD, BRVD, TERM, PT_L, PT_M, ROOT, CAT, IMG = 16, 17, 18, 19, 20, 21, 22, 23

total = IMG + img_secs



def both32(v): return struct.pack('<I', v) + struct.pack('>I', v)

def both16(v): return struct.pack('<H', v) + struct.pack('>H', v)

def pad(s, n, c=b' '): return s.ljust(n, c)[:n]



t = time.gmtime()

d7 = bytes([t.tm_year - 1900, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec, 0])

d17 = ('%04d%02d%02d%02d%02d%02d00' % (t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)).encode() + b'\x00'

zero17 = b'0' * 16 + b'\x00'



def dirrec(name, extent, length, flags):

ln = 33 + len(name)

if ln % 2: ln += 1

r = bytes([ln, 0]) + both32(extent) + both32(length) + d7 + bytes([flags, 0, 0]) + both16(1) + bytes([len(name)]) + name

return r.ljust(ln, b'\x00')



p = bytearray(SEC)

p[0] = 1; p[1:6] = b'CD001'; p[6] = 1

p[8:40] = pad(b'OXAQ', 32); p[40:72] = pad(b'OXAQ_SERVER', 32)

p[80:88] = both32(total); p[120:124] = both16(1); p[124:128] = both16(1); p[128:132] = both16(SEC)

p[132:140] = both32(10); p[140:144] = struct.pack('<I', PT_L); p[148:152] = struct.pack('>I', PT_M)

p[156:190] = dirrec(b'\x00', ROOT, SEC, 2)

p[190:702] = pad(b'', 512); p[574:702] = pad(b'OXAQ SERVER 1.0', 128)

p[702:813] = pad(b'', 111)

p[813:830] = d17; p[830:847] = d17; p[847:864] = zero17; p[864:881] = d17; p[881] = 1



b = bytearray(SEC)

b[1:6] = b'CD001'; b[6] = 1

b[7:39] = pad(b'EL TORITO SPECIFICATION', 32, b'\x00')

b[71:75] = struct.pack('<I', CAT)



z = bytearray(SEC); z[0] = 255; z[1:6] = b'CD001'; z[6] = 1



def ptable(big):

e = bytes([1, 0]) + struct.pack('>I' if big else '<I', ROOT) + struct.pack('>H' if big else '<H', 1) + b'\x00\x00'

return e.ljust(SEC, b'\x00')



root = (dirrec(b'\x00', ROOT, SEC, 2) + dirrec(b'\x01', ROOT, SEC, 2) +

dirrec(b'OXAQ.IMG;1', IMG, len(img), 0)).ljust(SEC, b'\x00')



val = bytearray(32); val[0] = 1; val[30] = 0x55; val[31] = 0xAA

val[28:30] = struct.pack('<H', (-sum(struct.unpack('<16H', bytes(val)))) & 0xFFFF)

ent = bytearray(32); ent[0] = 0x88; ent[1] = 2; ent[6:8] = struct.pack('<H', 1); ent[8:12] = struct.pack('<I', IMG)

cat = (bytes(val) + bytes(ent)).ljust(SEC, b'\x00')



iso = bytearray(total * SEC)

def put(sec, data): iso[sec * SEC: sec * SEC + len(data)] = data

put(PVD, p); put(BRVD, b); put(TERM, z); put(PT_L, ptable(False)); put(PT_M, ptable(True))

put(ROOT, root); put(CAT, cat); put(IMG, img)

open(dst, 'wb').write(iso)

print("Built", dst, len(iso), "bytes") 
