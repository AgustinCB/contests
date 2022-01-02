prefix = [int("e2", 16), int("80", 16)]
lotr = open("position", "br")

bytes = list(lotr.read())

print(prefix)
output = []
for i in range(len(bytes)-2):
	if [bytes[i], bytes[i+1]] == prefix and bytes[i+2] != int("99", 16):
		output.append(bytes[i+2] - 139)

result = ""
for i in range(15):
	byte = [str(c) for c in output[i*8:(i+1)*8][4:]]
	result += str(int("".join(byte), 2))
print(result)
