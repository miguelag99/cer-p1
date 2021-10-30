import requests
import re
import numpy as np
import os
import base64

from cryptography.fernet import Fernet


def get_rand_number():

    # Web HTML info

    url = requests.get("https://www.numeroalazar.com.ar/")
    htmlcont = url.text

    # Regular expression

    patron = re.compile('[1-9]*[0-9]\.[0-9][0-9]<')

    # Buscar los elementos que se ajustan a la expresion (todos los números generados) y quedarnos con el primero

    match = re.findall(patron,htmlcont)
    random_val = float(match[0][:len(match[0])-1])
    return random_val

def get_numbers_list(dict_list):

    if len(dict_list) != 0:

        func = lambda x: x['_source']['number']
        v_func = np.vectorize(func)

        return v_func(dict_list)

    else:
        return []

def get_cloud_numbers_list(dict_list):

    if len(dict_list) != 0:

        func = lambda x: x['data']
        v_func = np.vectorize(func)

        return v_func(dict_list)

    else:
        return []
        
def get_users_info(dict_list):

    if len(dict_list) != 0:

        func = lambda x: x['_source']
        v_func = np.vectorize(func)

        return v_func(dict_list)

    else:
        return []




class encrypt_object():
    def __init__(self, generate=False):

        if not os.path.exists('./key.key'):

            self.generate_encrypt_key()

        self.load_key()
        self.F = Fernet(self.key)

    def generate_encrypt_key(self):

        key = Fernet.generate_key()
        file = open("key.key", "wb")
        file.write(key)
        file.close()

    def load_key(self):

        file = open("key.key", "rb")
        self.key = file.read()
        file.close()
     
    def encrypt(self,data):
        
        encrypted = base64.b64encode(self.F.encrypt(data.encode()))
        return encrypted.decode('ascii')


    def decrypt(self,data, string = False):

        if string == True:
            data = base64.b64decode(data)

        return self.F.decrypt(data).decode()