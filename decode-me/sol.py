flag = open('encrypted_flag.txt', 'r').read()

while "easyctf" not in flag:
	flag = flag.decode('base64')

print flag
