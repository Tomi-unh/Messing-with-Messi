# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 12:31:20 2024

@author: may7e
"""
import json

data_info = {'base_url':'https://raw.githubusercontent.com/statsbomb/open-data/master/data/',
             'league_id': 11,
             'local_path': '../data/',
             'name': 'Lionel Andrés Messi Cuccittini'}




# Write the global variables to a JSON file
with open("messi_config.json", 'w') as file:
    json.dump(data_info, file)