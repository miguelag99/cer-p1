import requests
import re

from datetime import datetime
from elasticsearch import Elasticsearch
from flask import Flask

from elasticsearch_utils import elastic_database
from data_utils import get_numbers_list

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


def online_database(number):
    
    ## Beebote bbdd
    return 1


def main():

    
    number = get_rand_number()
    print(number)

    # Guardar en la BBDD local

    database = elastic_database()

    data = {
        "number": number
    }
    database.post_info("random_num",data)
    
    i = database.get_info("random_num")
    print(get_numbers_list(i['hits']['hits']))

    # Guardar en la BBDD de la nube


if __name__ == "__main__":
    main()
