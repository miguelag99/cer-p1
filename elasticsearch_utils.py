import argparse
import json

from elasticsearch import Elasticsearch
#import elasticsearch_dsl

class elastic_database():

    def __init__(self, host = 'localhost', port = 9200):

        self.es = Elasticsearch([{'host': host, 'port': port}])
        self.last_info = {}

    def delete_index(self,index_name):

        self.es.indices.delete(index=index_name, ignore=[400, 404])

    def create_index(self,index_name,conf):

        self.es.indices.create(index=index_name, body=conf)

    def reset_index(self,index_name,conf):

        self.es.indices.delete(index=index_name, ignore=[400, 404])
        self.es.indices.create(index=index_name, body=conf)

    def post_info(self,index_name,doc):

        self.es.index(index = index_name,document = doc)

    def get_info(self,index_name):

        return self.es.search(index=index_name,size = 500)



def conf_database(host = 'localhost', port = 9200):

    es = Elasticsearch([{'host': host, 'port': port}])

    configurations = {
        "settings": {
            "number_of_shards": 1
        },
        "mappings": {
            "properties": {
                 "number": { "type": "float" }
            }
        }     
    }   

    es.indices.create(index="random_num",body = configurations)

    # ## Anadir para user u pass


def reset_database(host = 'localhost', port = 9200):

    es = Elasticsearch([{'host': host, 'port': port}])

    es.indices.delete(index="random_num", ignore=[400, 404])    

    conf_database()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-conf","--configure_local_database",help="Configurar la base de datos local",action="store_true")
    parser.add_argument("-reset","--res_database",help="Eliminar datos de los indices de numeros y users",action="store_true")
    args = parser.parse_args()

    if args.configure_local_database:

        conf_database()

    if args.res_database:

        reset_database()
