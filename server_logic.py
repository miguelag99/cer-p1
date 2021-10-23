import sched
import time

from databases_utils import elastic_database
from data_utils import get_rand_number,get_numbers_list

TIME_GET_N = 120

def main():

    
    number = get_rand_number()
    #print(number)

    # Guardar en la BBDD local

    database = elastic_database()
    data = {
        "number": number
    }
   
    database.post_info("random_num",data)

    s.enter(TIME_GET_N,1,main)
    
    #i = database.get_info("random_num")
    #print(get_numbers_list(i['hits']['hits']))

    # Guardar en la BBDD de la nube -----------------------------------


if __name__ == "__main__":

    try:
        s = sched.scheduler(time.time, time.sleep)
        s.enter(TIME_GET_N,1,main)
        s.run()
    except KeyboardInterrupt:
        exit()


    
