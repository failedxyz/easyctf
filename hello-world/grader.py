fin = open("program_output", "r")

output = fin.read().strip()
print "OK" if output == "Hello, world!" else "FAIL"