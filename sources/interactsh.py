from uuid import uuid4
import requests
import base64
import json
import random
from loguru import logger

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256

class Interactsh:
    def __init__(self, token=None, servers=["interact.sh", "interactsh.com"]):
        rsa = RSA.generate(1024)
        self.public_key = rsa.publickey().exportKey()
        self.private_key = rsa.exportKey()
        self.token = token
        self.servers = servers
        self.headers = {
            "Content-Type": "application/json",
        }
        if self.token:
            self.headers['Authorization'] = self.token
        self.secret = str(uuid4())
        self.encoded = base64.b64encode(self.public_key).decode("utf8")
        guid = uuid4().hex.ljust(33, 'a')
        self.guid = ''.join(i if i.isdigit() else chr(ord(i) + random.randint(0, 20)) for i in guid)

        self.correlation_id = self.guid[:20]

        self.session = requests.session()
        self.session.headers = self.headers
        self.register()

    def deregister(self):
        """
        : deregister token
        """
        data = {
            "secret-key": self.secret,
            "correlation-id": self.correlation_id
        }
        try:
            r = requests.post(f"https://{self.server}/deregister", json=data, headers=self.headers, timeout=1, verify=False)
        except Exception as e:
            logger.error(e)
            return
        #print(f"Interactsh deregister response {r.text}")

    def register(self):
        data = {
            "public-key": self.encoded,
            "secret-key": self.secret,
            "correlation-id": self.correlation_id
        }
        #print(.debug(f"Registering \nKey: {self.encoded}\nSecret: {self.secret}\nHandle: {self.correlation_id}")
        for server in self.servers:
            try:
                res = self.session.post(
                    f"https://{server}/register", headers=self.headers, json=data, timeout=10, verify=False)
                self.server = server
                self.domain = f'{self.guid}.{self.server}'
                # print(.debug(self.domain)
                break
            except Exception as e:
                logger.error(f"Server {server} failed to register, trying the next one: {e}")
                continue

        if 'success' not in res.text:
            logger.error(res.text)

        self.write_handle_logs()

    def write_handle_logs(self):
        pass

    def poll(self):
        result = []
        url = f"https://{self.server}/poll?id={self.correlation_id}&secret={self.secret}"
        res = self.session.get(url, headers=self.headers, verify=False, timeout=30)
        try:
            res = res.json()
        except:
            logger.error('An error occured with the target, maybe a proxy is blocking you ?')
            logger.debug(res.text)
            return None
        aes_key, data_list = res['aes_key'], res['data']
        #print(.debug(res)
        for i in data_list:
            decrypt_data = self.decrypt_data(aes_key, i)
            result.append(self.__parse_log(decrypt_data))
        return result

    def __parse_log(self, log_entry):
        new_log_entry = {"timestamp": log_entry["timestamp"],
                         "host": f'{log_entry["full-id"]}.{self.domain}',
                         "remote_address": log_entry["remote-address"],
                         "raw-request": log_entry["raw-request"],
                         "protocol": log_entry["protocol"]
                         }
        return new_log_entry

    def decrypt_data(self, aes_key, data):
        private_key = RSA.importKey(self.private_key)
        cipher = PKCS1_OAEP.new(private_key, hashAlgo=SHA256)
        aes_plain_key = cipher.decrypt(base64.b64decode(aes_key))
        decode = base64.b64decode(data)
        bs = AES.block_size
        iv = decode[:bs]
        cryptor = AES.new(key=aes_plain_key, mode=AES.MODE_CFB, IV=iv, segment_size=128)
        plain_text = cryptor.decrypt(decode)
        return json.loads(plain_text[16:])

    def get_handle(self):
        return f"http://{self.domain}/"