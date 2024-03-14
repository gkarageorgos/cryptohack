from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes

# LATTICES

def add(a, b, n):
    add = []
    for i in range(n):
        add.append(a[i] + b[i])
    return add

def sc_mult(c, a, n):
    mult = []
    for i in range(n):
        mult.append(c * a[i])
    return mult

def in_prod(a, b, n):
    S = 0
    for i in range(n):
        S += a[i] * b[i]
    return S

v = (2, 6, 3)
w = (1, 0, 0)
u = (7, 7, 2)

# 3*(2*v - w) ∙ 2*u
tmp = in_prod(sc_mult(3, add(sc_mult(2, v, 3), sc_mult(-1, w, 3), 3), 3), sc_mult(2, u, 3), 3)
print(tmp)

# Size and Basis

v = (4, 6, 2, 5)
print(in_prod(v, v, 4))

# Gram Schmidt

v = [[4, 1, 3, -1], [2, 1, -3, 4], [1, 0, -2, 7], [6, 2, 9, -5]]
u = [v[0]]
for i in range(1, 4):
    m = [in_prod(v[i], u[j], 4) / in_prod(u[j], u[j], 4) for j in range(i)]
    S = [0, 0, 0, 0]
    for j in range(i):
        S = add(S, sc_mult(-m[j], u[j], 4), 4)
    u.append(add(v[i], S, 4))

print(round(u[3][1], 5))

# What's a Lattice?

P = [[6, 2, -3], [5, 1, 4], [2, 7, 1]]
tmp = 0
for j in range(3):
    i = 0
    tmp += P[0][j] * (P[(i + 1) % 3][(j + 1) % 3] * P[(i + 2) % 3][(j + 2) % 3] - P[(i + 1) % 3][(j + 2) % 3] * P[(i + 2) % 3][(j + 1) % 3])
print(tmp)

# Gaussian Reduction

def gaussian_lattice_reduction(v1, v2):
    while True:
        if in_prod(v1, v1, 2) > in_prod(v2, v2, 2):
            v1, v2 = v2, v1
        m = in_prod(v1, v2, 2) // in_prod(v1, v1, 2)
        if m == 0:
            return v1, v2
        else:
            v2 = add(v2, sc_mult(-m, v1, 2), 2)


v, u = gaussian_lattice_reduction([846835985, 9834798552], [87502093, 123094980])
print(in_prod(v, u, 2))

# Find the Lattice

Encrypted_Flag = 5605696495253720664142881956908624307570671858477482119657436163663663844731169035682344974286379049123733356009125671924280312532755241162267269123486523

def decrypt(q, h, f, g, e):
    a = (f*e) % q
    m = (a*inverse(f, g)) % g
    return m

q, h = 7638232120454925879231554234011842347641017888219021175304217358715878636183252433454896490677496516149889316745664606749499241420160898019203925115292257, 2163268902194560093843693572170199707501787797497998463462129592239973581462651622978282637513865274199374452805292639586264791317439029535926401109074800
u, v = gaussian_lattice_reduction([0, q], [1, h])
f, g = u[0], u[1]

m = decrypt(q, h, f, g, Encrypted_Flag)
FLAG = long_to_bytes(m)
print(FLAG)
