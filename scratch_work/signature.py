"""Initial test file"""

from Crypto.PublicKey import ECC
from Crypto.Hash import SHA256
from Crypto.Signature import DSS


"""# key = ECC.import_key(open('privkey.der').read())
key = RSA.generate(1024)
private_key = key.export_key()
public_key = key.public_key().export_key()
print(private_key, public_key)"""

key = ECC.generate(curve='P-256')
private_key = key.export_key(format='PEM')
public_key = key.public_key().export_key(format='PEM')

print()
message = b'Hello Darkness My Old Friend'
long_message = bytes(bytearray([i % 100 for i in range(10000)]))

key = ECC.import_key(private_key)
h = SHA256.new(long_message)
signer = DSS.new(key, 'fips-186-3')
signature = signer.sign(h)
print(signature, len(signature))

received_message = long_message
key = ECC.import_key(public_key)
h = SHA256.new(received_message)
verifier = DSS.new(key, 'fips-186-3')
verifier.verify(h, signature)
