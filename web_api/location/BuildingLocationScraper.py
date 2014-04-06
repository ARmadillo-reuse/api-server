'''
Created on Apr 6, 2014

@author: Alex
'''

import json
import urllib2

def run_main():
    print get_all_building_data()

def get_all_building_data():
    building_data = {}
    
    building_names = get_building_names()
    
    for building in building_names:
        building_obj = get_json_obj(building)
        if building_obj:
            data = building_obj[0]
            building_data[building] = {
                                   "name": data["name"],
                                   "lat": data["lat_wgs84"],
                                   "lon": data["long_wgs84"]
                                   }
    
    return building_data
    
def get_building_names():
    b_list = ['1', '2', '3', '4', '5', '6', '6B', '6C', '7', '7A', '8', '9',
            '10', '11', '12', '12A', '13', '14', '16', '17', '18', '24', '26',
            '31', '32', '32P', '33', '34', '35', '36', '37', '38', '39', '41',
            '42', '43', '44', '46', '48', '50', '51', '54', '56', '57', '62',
            'WOOD', '64', 'GOODALE', '66', '68', '76', 'E1', 'E2', 'E14',
            'E15', 'E17', 'E18', 'E19', 'E23', 'E25', 'E33', 'E34', 'E38',
            'E40', 'E51', 'E52', 'E53', 'E55', 'E60', 'E62', 'N4', 'N9', 'N10',
            'N16', 'N16A', 'N16B', 'N16C', 'N51', 'N52', 'N57', 'NW10', 'NW12',
            'NW12A', 'NW13', 'NW14', 'NW15', 'NW16', '(NW16)', 'NW17', '(NW17)',
            'NW20', 'NW21', '(NW21)', 'NW22', '(NW22)', 'NW30', 'NW35', 'NW61',
            'NW86', 'NW86P', 'GARAGE', 'OC1', 'OC1A', 'OC19A', 'OC19B', 'OC19C',
            'OC19D', 'OC19E', 'OC19F', 'OC19G', 'OC19H', 'OC19J', 'STORAGE',
            'OC19K', 'GALLERY', 'OC19L', 'OC19M', 'OC19N', 'OC19Q', 'OC21',
            'OBSERVATORY', 'OC22', '(HAYSTACK)', 'OC23', 'OC25', 'OC26',
            'BUILDING', 'OC31', 'OC31A', 'OC32', 'OC32A', 'OC32B', 'OC33',
            'OC35', 'OC36', 'OC36A', 'W1', 'W2', 'W4', 'W5', 'W7', 'W8', 'W11',
            'W13', 'W15', 'W16', 'W20', 'W31', 'W32', 'W33', 'W34', 'W35',
            'W45', 'W51', 'W51C', 'W53', 'W53A', '(OFFICE)', 'W53B', 'W53C',
            'W53D', 'W56', 'W57', 'W57A', 'W59', 'W61', 'W64', 'W70', 'W71',
            'W79', 'W84', 'W85', 'W89', 'W91', 'W92', 'W98', 'W85DE', 'W85FG',
            'WW15', 'W85ABC', 'W85HJK']
    return set(filter(lambda x: not x.startswith("("), b_list))

def get_json_obj(building_name):
    response = urllib2.urlopen("http://whereis.mit.edu/search?type=query&q=%s"
                                % building_name)
    res_obj = json.loads(response.read())
    return res_obj

if __name__ == '__main__':
    run_main()
    