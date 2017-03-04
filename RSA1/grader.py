from cStringIO import StringIO

flag = "wh3n_y0u_h4ve_p&q_RSA_iz_ez"

def modx(base,exp,mod):
    r = 1;
    while (exp > 0):
        if (exp % 2 == 1):
            r = (r * base) % mod
        base = (base * base) % mod
        exp = exp/2
    return r

def probprime(s):
    while (modx(2,s-1,s) != 1  or  modx(3,s-1,s) != 1  or modx(5,s-1,s) != 1 or modx(7,s-1,s) != 1):
        s += 1
    return(s)

def get_problem(random):
    # add Probable Prime function later
    p = probprime(random.randint(3*10**59,4*10**59))
    q = probprime(random.randint(3*10**59,4*10**59))
    e = 3
    salt = "".join([random.choice("0123456789abcdef") for i in range(8)])
    return (p, q, e, salt)

def generate_ciphertext(random):
    p, q, e, salt = get_problem(random)
    encoded = int(("easyctf{%s_%s}" % (flag, salt)).encode('hex'),16)
    ciphertext =  'p: '+str(p)+'\n'
    ciphertext += 'q: '+str(q)+'\n'
    ciphertext += 'e: '+str(e)+'\n'
    ciphertext += 'c: '+str(pow(encoded, e, p*q))+'\n'

    return StringIO(ciphertext)

def generate(random):
    return dict(files={
        "ciphertext_rsa1.txt": generate_ciphertext
    })

def grade(random, key):
    n, salt = get_problem(random)
    if key.find("%s_%s" % (flag, salt)) >= 0:
        return True, "Correct!"
    return False, "Nope."
