from OpenSSL import crypto
import sys
import base64

pubkey = crypto.load_certificate(crypto.FILETYPE_PEM, '''-----BEGIN CERTIFICATE-----
MIIC3DCCAcQCCQCssHkW19B4jzANBgkqhkiG9w0BAQsFADAwMQswCQYDVQQGEwJr
bzEhMB8GCSqGSIb3DQEJARYScGh1NTQzMjFAbmF2ZXIuY29tMB4XDTE4MTAyMDAz
NTM1NFoXDTE4MTExOTAzNTM1NFowMDELMAkGA1UEBhMCa28xITAfBgkqhkiG9w0B
CQEWEnBodTU0MzIxQG5hdmVyLmNvbTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCC
AQoCggEBANEJK2T26Sc3W7wJVLXiwuseWMcIb6hwLoXszlHwRYo8+EpBiFEjHzez
fR+P0gGw/LYaIyajsTZjrSaBOCjVMxYC/MgsMRqS35Z7b8PLZ0dRB0IIKal0QRAQ
SdKV+o+XThuKG+GZyJUA6h/mVR5QKdTz56SVYKo0E1idFvAIcVktKVIPQGpbt0In
cPVVFUrL7JsXQzATEsy+LrSQyPZ5y5P7ZRdI0i2F6qcMTT1Wn4khuC4KJsxVL84v
1DY/Ae5swRHndKvV/+HuA9zNecuuqYopQ5vc/epRkyNLg74zz1mGdPOGdLlEEc45
/qrWD3RgMrpzsXRjzgivKA2zmu9ul20CAwEAATANBgkqhkiG9w0BAQsFAAOCAQEA
PpOG2o8SbBpZOkQeU/Yd/FnmAx+6Y3MIMq4KvJJ9UnnGN0NhRu90MLnuDIY0/WTm
4wXsTvvK+l8aP0dKipGgyBMA5bCYMchlbhY8iryUGOV+YBwW3OiRDlL7CAap2QVg
HM3Y6HBgkOK0/tBMWj2XPEB8rVN7tOBgaD+JGfs8e91akAR+7BEuFRPjkbRYz2pH
3r9ydvAOTeLk8ky0QWLq7UvALzgMIRf03nR9dl6mEo0fQmyT5zUt/qlYjqXL+kOA
wFcG2w7HrqWkgRPwPlzdFL/U6ReGqHYMazQF4C4tIA4iOa5mN1QT0OvsiB7O3yYZ
mZd/fcEi06rmFswNxzOSZQ==
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
