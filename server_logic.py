import sched
import time

from databases_utils import elastic_database, beebote_database
from data_utils import get_rand_number,get_numbers_list

TIME_GET_N = 120

def main():

    number = get_rand_number()

    # Guardar en la BBDD local

    database = elastic_database()
    data = {
        "number": number
    }
   
    database.post_info("random_num",data)

    # Guardar en la BBDD de la nube 

    cloud_database = beebote_database()
    cloud_database.post_info("Cer_p1","random_n",data=number)

    s.enter(TIME_GET_N,1,main)


if __name__ == "__main__":

    try:
        s = sched.scheduler(time.time, time.sleep)
        s.enter(TIME_GET_N,1,main)
        s.run()
    except KeyboardInterrupt:
        exit()


    
