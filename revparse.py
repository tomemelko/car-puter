maxrevs = 0

for line in open("revs.log"):
	if "41 0C" in line:
		bytes = line[line.index("41 0C")+6:-1].split(' ')
		a = int(bytes[0], 16)
		b = int(bytes[1], 16)
		revs = ((a*256)+b)/4
		if revs > 2000:
			print revs
			if revs > maxrevs:
				maxrevs = revs

print maxrevs