import argparse

from elasticsearch import Elasticsearch
#import elasticsearch_dsl
from beebotte import *

BEEBOTTE_API_YEY = "vXAtkOwObYu9sEq78XnyRO4v"
BEEBOTTE_SECRET_KEY = "m1Ycfq8GTHm211zrrhvjHY3saKLyerIq"


class elastic_database():

    def __init__(self, host='localhost', port=9200):

        self.es = Elasticsearch([{'host': host, 'port': port}])
        self.last_info = {}

    def delete_index(self, index_name):

        self.es.indices.delete(index=index_name, ignore=[400, 404])

    def create_index(self, index_name, conf):

        self.es.indices.create(index=index_name, body=conf)

    def reset_index(self, index_name, conf):

        self.es.indices.delete(index=index_name, ignore=[400, 404])
        self.es.indices.create(index=index_name, body=conf)

    def post_info(self, index_name, doc, _id = None):

        self.es.index(index=index_name, document=doc, id=_id)

    def get_info(self, index_name, q = None):

        aux = self.es.search(index = index_name, query = q ,size = 500)
        return aux['hits']['hits']


class beebote_database():

    def __init__(self):

        self.bclient = BBT(BEEBOTTE_API_YEY,BEEBOTTE_SECRET_KEY)
    

    def post_info(self, channel, resource, data):

        resource = Resource(self.bclient,channel,resource)
        resource.write(data)

    def get_info(self, channel, resource, max_elements = 500):

        resource = Resource(self.bclient,channel,resource)
        return resource.read(max_elements)

    def reset_resource(self,channel,resource):

        self.bclient.deleteResource(channel,resource)

        self.bclient.addResource(channel=channel,name=resource)

    def create_resource(self,channel,resource):

        self.bclient.addResource(channel=channel,name=resource)

    def delete_resource(self,channel,resource):

        self.bclient.deleteResource(channel,resource)



def conf_database(host='localhost', port=9200):

    es = Elasticsearch([{'host': host, 'port': port}])
    bbt = beebote_database()

    configurations = {
        "settings": {
            "number_of_shards": 1
        },
        "mappings": {
            "properties": {
                "number": {"type": "float"}
            }
        }
    }

    es.indices.create(index="random_num", body=configurations)

    configurations = {
        "settings": {
            "number_of_shards": 1
        },
        "mappings": {
            "properties": {
                "username": {"type": "text"},
                "email": {"type": "text"},
                "pass": {"type": "binary"},
                "n_local_acc": {"type": "integer"},
                "n_cloud_acc": {"type": "integer"}
            }
        }
    }

    es.indices.create(index="user_data", body=configurations)

    bbt.create_resource("Cer_p1","random_n")
    bbt.create_resource("Cer_p1","user_data")


def reset_database(host='localhost', port=9200):

    es = Elasticsearch([{'host': host, 'port': port}])

    es.indices.delete(index="random_num", ignore=[400, 404])
    es.indices.delete(index="user_data", ignore=[400, 404])

    bbt = beebote_database()
    try:
        bbt.delete_resource(channel='Cer_p1',resource='user_data')
        bbt.delete_resource(channel='Cer_p1',resource='random_n')
    except:
        pass

    conf_database()

