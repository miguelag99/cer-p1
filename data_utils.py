import requests
import re
import numpy as np

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


def get_users_info(dict_list):

    if len(dict_list) != 0:

        func = lambda x: x['_source']
        v_func = np.vectorize(func)

        return v_func(dict_list)

    else:
        return []

