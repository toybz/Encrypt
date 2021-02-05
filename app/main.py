import json, requests
import base64
from Crypto.Cipher import DES3
import hashlib
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

#v2 encryption class
class Encrypt(object):
  def __init__(self):
    pass
  
  #encryption key generation block
  def getKey(self,secret_key):
    hashedseckey = hashlib.md5(secret_key.encode("utf-8")).hexdigest()
    hashedseckeylast12 = hashedseckey[-12:]
    seckeyadjusted = secret_key.replace('FLWSECK-', '')
    seckeyadjustedfirst12 = seckeyadjusted[:12]
    return seckeyadjustedfirst12 + hashedseckeylast12
  
  def encryptData(self, key, plainText):
    blockSize = 8
    padDiff = blockSize - (len(plainText) % blockSize)
    cipher = DES3.new(key, DES3.MODE_ECB)
    plainText = "{}{}".format(plainText, "".join(chr(padDiff) * padDiff))
    encrypted = base64.b64encode(cipher.encrypt(plainText))
    return encrypted

  
  def data_encrypt(self, PBFPubKey, sec_key, data):

    # hash the secret key with the get hashed key function
    hashed_sec_key = self.getKey(sec_key)

    # encrypt the hashed secret key and payment parameters with the encrypt function
    encrypt_3DES_key = self.encryptData(hashed_sec_key, json.dumps(data))

    # payment payload
    payload = {
        "PBFPubKey": PBFPubKey,
        "client": encrypt_3DES_key,
        "alg": "3DES-24"
    }
    
    return (payload)

class Req(BaseModel):
    PBFPubKey: str
    sec_key: str
    data: dict

#main encryption endpoint
@app.post('/encrypt')
async def index(payload: Req):
    details = dict(payload)
    public_key = details['PBFPubKey']
    secret_key = details['sec_key']
    data = details['data']

    core = Encrypt()
    return (core.data_encrypt(public_key,secret_key,data))