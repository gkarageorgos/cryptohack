from pwn import * # pip install pwntools
import json
import base64
import codecs

from Crypto.Util.number import *

# ASCII

ords = [99, 114, 121, 112, 116, 111, 123, 65, 83, 67, 73, 73, 95, 112, 114, 49, 110, 116, 52, 98, 108, 51, 125]
print("Here is the flag for ASCII task:")
print("".join(chr(o) for o in ords))

# Hex

h = "63727970746f7b596f755f77696c6c5f62655f776f726b696e675f776974685f6865785f737472696e67735f615f6c6f747d"
b = bytes.fromhex(h)
print("Here is the flag for Hex task:")
print(b)
# print(bts.hex(), type(bts))

# Base64

h = "72bca9b68fc16ac7beeb8f849dca1d8a783e8acf9679bf9269f7bf"
b = bytes.fromhex(h)
bs64 = base64.b64encode(b)
print("Here is the flag for Base64 task:")
print(bs64)

# Bytes and Big Integers

i = 11515195063862318899931685488813747395775516287289682636499965282714637259206269

h = hex(i)

h = [h[i:i+2] for i in range(0, len(h), 2)]

h = h[1:]
b = []
for i in range(len(h)):
    tmp = bytes.fromhex(h[i])
    b.append(tmp)

# print(b)
ords = []
for i in b:
     tmp = bytes_to_long(i)
     ords.append(tmp)

print("Bytes and Big Integers:")
print("".join(chr(o) for o in ords))


# Encoding Challenge

r = remote('socket.cryptohack.org', 13377, level = 'debug')

def json_recv():
    line = r.recvline()
    return json.loads(line.decode())

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)

def decoded(encoded, encoding):
    if encoding == "base64":
        encoded = bytes(base64.b64decode(encoded)).decode("utf-8")  # wow so encode
    elif encoding == "hex":
        encoded = bytes(bytes.fromhex(encoded)).decode("utf-8")
    elif encoding == "rot13":
        encoded = codecs.decode(encoded, 'rot_13')
    elif encoding == "bigint":
        encoded = bytes(long_to_bytes(int(encoded, 16))).decode("utf-8")
    elif encoding == "utf-8":
        encoded = ''.join(chr(i) for i in encoded)

    return encoded


for i in range(100):
    received = json_recv()
    to_send = {
        "decoded": decoded(received["encoded"], received["type"])
    }
    json_send(to_send)
print(json_recv())

