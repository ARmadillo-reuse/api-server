from math import sqrt

from django.test import TestCase

from web_api.location.ItemPostLocator import ItemPostLocator


class TestItemPostLocator(TestCase):
    def test_locate_buildings_only(self):
        test_buildings = {"W20": {'lat': 42.35904262, 'lon': -71.09477492},
                          "10": {'lat': 42.35967402, 'lon': -71.09201372},
                          "W71": {'lat': 42.35471738, 'lon': -71.10191653}}
        
        ipl = ItemPostLocator()
        for building, expected in test_buildings.iteritems():
            received = ipl.get_location(building)
            delta = [expected[x] - received[x] for x in ("lat","lon")]
            dist = sqrt(sum(x*x for x in delta))
            self.assertAlmostEqual(dist, 0)
        
    def test_locate_rooms(self):
        test_rooms = {"32-123": {'lat': 42.36161284, 'lon': -71.09056786},
                      "2-147": {'lat': 42.35881411, 'lon': -71.09018586},
                      "E17-100": {'lat': 42.36148438, 'lon': -71.08788625}}
        
        ipl = ItemPostLocator()
        for room, expected in test_rooms.iteritems():
            received = ipl.get_location(room)
            delta = [expected[x] - received[x] for x in ("lat","lon")]
            dist = sqrt(sum(x*x for x in delta))
            self.assertAlmostEqual(dist, 0)