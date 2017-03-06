from cStringIO import StringIO
from qrt import generate

FLAG = "are_triangles_more_secure_than_squares?_%s}"

def get_salt(random):
	return "".join([random.choice("0123456789abcdef") for i in range(8)])

def generate(random):
	salt = get_salt(random)
	im = generate("easyctf{%s}" % (FLAG % salt))
	flag = StringIO()
	im.save(buf, format="PNG")
	return dict(files={
		"flag.png": flag
	})

def grade(random, key):
	salt = get_salt(random)
	if key.find(FLAG % salt) >= 0:
		return True, "Correct!"
	return False, "Nope."