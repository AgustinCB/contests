import sys

f = open("position.gzip", "bw+")
for l in sys.stdin:
	f.write(bytearray([int(n, 16) for n in l.strip().split(" ")]))
