from OpenSSL import crypto
import sys
import base64

pubkey = '''\
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA0QkrZPbpJzdbvAlUteLC
6x5YxwhvqHAuhezOUfBFijz4SkGIUSMfN7N9H4/SAbD8thojJqOxNmOtJoE4KNUz
FgL8yCwxGpLflntvw8tnR1EHQggpqXRBEBBJ0pX6j5dOG4ob4ZnIlQDqH+ZVHlAp
1PPnpJVgqjQTWJ0W8AhxWS0pUg9Aalu3Qidw9VUVSsvsmxdDMBMSzL4utJDI9nnL
k/tlF0jSLYXqpwxNPVafiSG4LgomzFUvzi/UNj8B7mzBEed0q9X/4e4D3M15y66p
iilDm9z96lGTI0uDvjPPWYZ084Z0uUQRzjn+qtYPdGAyunOxdGPOCK8oDbOa726X
bQIDAQAB
-----END PUBLIC KEY-----
'''

pkey = None

def _loadPkey():
    global pkey

    if pkey:
        return

    key_file = open('signature/euddraft_priv.pem', 'r')
    key = key_file.read()
    key_file.close()

    pkey = crypto.load_privatekey(crypto.FILETYPE_PEM, key)
    if not pkey.check():
        print('Invalid key')
        sys.exit(-1)

def generateFileSignature(fname):
    _loadPkey()

    data = open(fname, 'rb').read()
    signature = crypto.sign(pkey, data, "sha256")
    return base64.b64encode(signature).decode('ascii')
