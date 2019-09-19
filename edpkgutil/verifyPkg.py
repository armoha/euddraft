import base64
import sys

from OpenSSL import crypto

pubkey = crypto.load_certificate(
    crypto.FILETYPE_PEM,
    """-----BEGIN CERTIFICATE-----
MIICgDCCAekCAgPoMA0GCSqGSIb3DQEBBQUAMIGHMQswCQYDVQQGEwJLUjEOMAwG
A1UECAwFU2VvdWwxDzANBgNVBAcMBlNvbmdwYTEhMB8GA1UECgwYU3RhckNyYWZ0
IEVEaXRvciBBQ2FkZW15MRowGAYDVQQLDBFUZWFtIFByb2plY3RDZXJlczEYMBYG
A1UEAwwPREVTS1RPUC1LS1U2UDBLMB4XDTE5MDMwNDA3MDEwNVoXDTI5MDMwMTA3
MDEwNVowgYcxCzAJBgNVBAYTAktSMQ4wDAYDVQQIDAVTZW91bDEPMA0GA1UEBwwG
U29uZ3BhMSEwHwYDVQQKDBhTdGFyQ3JhZnQgRURpdG9yIEFDYWRlbXkxGjAYBgNV
BAsMEVRlYW0gUHJvamVjdENlcmVzMRgwFgYDVQQDDA9ERVNLVE9QLUtLVTZQMEsw
gZ8wDQYJKoZIhvcNAQEBBQADgY0AMIGJAoGBAOoI9rIsbYbpYI6Q0bTp38fMMHa4
PtnhIYR7AvZY/MXSthZc3GOEwkWHB4ELCIT4iaKpQSLOlCbPu/Hoquy54bSbOY86
WXjHqI8sk+ZZg0WpQBQM37gPPwRZTRQ3j5j2u85h+U++4Thh1XuJZY34/MZnM30M
ZQQ4sTHoC4JO4hR5AgMBAAEwDQYJKoZIhvcNAQEFBQADgYEAQhtwqDIODwZT5hci
PM8BaFcqFHe+xAs4RlErlT7TLRVRVnhOnQTu1322PHk3mMCYjywKfJs/Q63/CfYN
UGdcndB2AzBBjDnj+NHND7UKmrMI8unNlUM/c3EQDv7bvXGyX/OOiGECes4/cBnY
bEtMPTEWR6UWpQ1W7fzBPjUYhDA=
-----END CERTIFICATE-----""",
)

pkey = None


def _loadPkey():
    global pkey

    if pkey:
        return

    key_file = open("signature/euddraft_priv.pem", "r")
    key = key_file.read()
    key_file.close()

    pkey = crypto.load_privatekey(crypto.FILETYPE_PEM, key)
    if not pkey.check():
        print("Invalid key", file=sys.stderr)
        sys.exit(-1)


def generateFileSignature(fname):
    _loadPkey()

    data = open(fname, "rb").read()
    signature = crypto.sign(pkey, data, "sha256")
    return base64.b64encode(signature).decode("ascii")


def verifyFileSignature(data, sig):
    try:
        sig = base64.b64decode(sig.encode("ascii"))
    except (AttributeError):
        sig = base64.b64decode(sig)
    # crypto.verify throws exception if anything fails.
    try:
        crypto.verify(pubkey, sig, data, "sha256")
        return True
    except:
        return False
