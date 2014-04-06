'''
Created on Apr 6, 2014

@author: Alex
'''

import os
import pickle
from copy import copy

class ItemPostLocator(object):
    '''
    A class for determining the location of items
    '''

    def __init__(self):
        self.building_data = self.get_building_data()
        
    def get_building_data(self):
        directory = os.path.dirname(os.path.realpath(__file__))
        with open(directory + "/buildings.pickle") as f:
            return pickle.loads(f.read())
        
    def get_location(self, location_name):
        for building in self.building_data.keys():
            if (location_name == building or
                (location_name.startswith(building) and
                location_name[len(building)] == '-')):
                return copy(self.building_data[building])
        
        return None
        