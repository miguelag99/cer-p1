import numpy as np

def get_numbers_list(dict_list):

    if len(dict_list) != 0:

        func = lambda x: x['_source']['number']
        v_func = np.vectorize(func)

        return v_func(dict_list)

    else:
        return []

