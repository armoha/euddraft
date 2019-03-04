import base64
import sys

from OpenSSL import crypto

pubkey = crypto.load_certificate(crypto.FILETYPE_PEM, '''-----BEGIN CERTIFICATE-----
MIICbjCCAdcCAgPoMA0GCSqGSIb3DQEBBQUAMH8xCzAJBgNVBAYTAlVTMRIwEAYD
VQQIDAlNaW5uZXNvdGExEzARBgNVBAcMCk1pbm5ldG9ua2ExEzARBgNVBAoMCm15
IGNvbXBhbnkxGDAWBgNVBAsMD215IG9yZ2FuaXphdGlvbjEYMBYGA1UEAwwPREVT
S1RPUC1LS1U2UDBLMB4XDTE5MDMwNDA2MjE1OVoXDTI5MDMwMTA2MjE1OVowfzEL
MAkGA1UEBhMCVVMxEjAQBgNVBAgMCU1pbm5lc290YTETMBEGA1UEBwwKTWlubmV0
b25rYTETMBEGA1UECgwKbXkgY29tcGFueTEYMBYGA1UECwwPbXkgb3JnYW5pemF0
aW9uMRgwFgYDVQQDDA9ERVNLVE9QLUtLVTZQMEswgZ8wDQYJKoZIhvcNAQEBBQAD
gY0AMIGJAoGBAKSVbFsXkDUMqU1gQLYYu7Lqk1kPYVkQI7b8pO1M6tdjL+IxVc9N
oSGwDbcgK+UWyMKZl6LJzK6taViOtDrmY1eFOXxMqrlfnjtqJSLLqL+trlgMNAqc
7iAYEPU2tg425K3oxbUaEjD5OeOwOMZ8dq7Mfw3E6CjcZim+qcC9R7fPAgMBAAEw
DQYJKoZIhvcNAQEFBQADgYEAJz/8Wa17sEMdZ82Ntn50T/nFcKXDkxVWVayRRq6P
6ETueVkLyD6EOdwo/RWWbgH2hbXSic7o3ij0wDxZhc/N5htuqV+CKcvXVV5PxAGg
dTARv6EP8MowrzIo9Iv63zo90/0CNe1K7gS79M4pcoAhLqp1X8FVpVMYTp2pCmEa
TXI=
-----END CERTIFICATE-----''')

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

def verifyFileSignature(data, sig):
    sig = base64.b64decode(sig.encode('ascii'))
    # crypto.verify throws exception if anything fails.
    try:
        crypto.verify(pubkey, sig, data, "sha256")
        return True
    except:
        return False
