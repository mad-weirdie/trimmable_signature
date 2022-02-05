"""
Run if you want to make new public/private key pairs
"""

from Crypto.PublicKey import ECC

def make_keys(name):
    key = ECC.generate(curve='P-256')
    private_key = key.export_key(format='PEM')
    public_key = key.public_key().export_key(format='PEM')
    with open(f"keys/{name}_public_key.pem", "w") as f:
        f.write(public_key)
    with open(f"keys/{name}_private_key.pem", "w") as f:
        f.write(private_key)

make_keys("Alice")
make_keys("Bob")