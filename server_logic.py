import requests
import re

from elasticsearch import Elasticsearch
from flask import Flask

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


def local_database(number):

    es = Elasticsearch()



def main():

    
    number = get_rand_number()
    print(number)

    # Guardar en la BBDD local



    # Guardar en la BBDD de la nube


if __name__ == "__main__":
    main()
