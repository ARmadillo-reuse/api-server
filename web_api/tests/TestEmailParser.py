import os
from django.test import TestCase
import web_api.processing

class TestEmailParser(TestCase):
    def test_can_parse_emails(self):
        parser = web_api.processing.EmailParser()
        directory = os.path.dirname(os.path.realpath(__file__)) + "/files"

        for (num, expected) in self.get_emails():
            with open(os.path.realpath("%s/msg.%06d" % (directory, num))) as f:
                text = f.read()

            result = parser.parse(text)
            for key in result.keys():
                self.assertEqual(result[key], expected[key], "'%s' value: expected '%s', got '%s'" % (key, expected[key], result[key]))

    def get_emails(self):
        return [(4496, {'from': 'ddw@mit.edu',
                        'subject': 'Free 4x8 ft chalkboard',
                        'text':
        "Free 4x8 foot slate chalkboard outside room 38-145.  "
        "It is large and heavy,\nyou'll need at least 2 people "
        "to carry it away."}),

                (27666, {'from': 'astout@mit.edu',
                         'subject': 'miscellaneous stuff outside 10-500',
                         'text':
        "Now appearing outside 10-500! (Barker Engineering Library lobby)\n\n"
        "Lots of cellophane sleeves for greeting cards. I used to sell greeting \n"
        "cards, and used these for the packaging.\n\n"
        "1 bicycle helmet circa 1996. Never been in an accident, though.\n\n"
        "1 tattered French-English dictionary.\n\n"
        "1 French grammar book from \"Teach Yourself\" series.\n\n"
        "1 SAT preparation workbook.\n\n"
        "1 harness for medium-sized dog (adjustable).\n\n"
        "Please don't email me -- just come, snag and post!\n\n"
        "Thanks,\nAmy"}),
                (32927, {'from': 'jennyqiu@mit.edu',
                         'subject': 'Re: 2 one gallon jugs of tropicana orange juice',
                         'text':
        "claimed!"}),
                (34557, {'from': 'jbuz@mit.edu',
                         'subject': 'Re: maps, 54-1721',
                         'text':
                         "I took the bike map"
                         }),
                (47576, {'from':'jessmith@mit.edu',
                          'subject': 'chairs and computer extras',
                          'text':
        "There are a bunch of mice, cables, and a couple of chairs available for re-=\n"
        "use outside of 35-338.\n\nPlease come help yourself."}),
                (47571, {'from': 'jenifer.leibrandt@gmail.com',
                         'subject': 'Re: large chunk of green foam',
                         'text': 'Taken'}),
                (47570, {'from': 'heinl@mit.edu',
                         'subject': 'Kimball office furniture work desk top surface to go',
                         'text':
        'Removed a "bullet top" desk surface from one office in W35 in order to reco=\n'
        "nfigure the office and the top needs to leave the building.   Email only to=\n"
        ": heinl@mit.edu<mailto:heinl@mit.edu>  If you want to come by and remove, I=\n"
        " will provide you with the location for pick up in W34.  Good weight to it =\n"
        "-Heavy and solid top, will require a hand truck or dolly to move out and pr=\n"
        "obably two people. Piece is about 10 years old, no legs or hardware-  Color=\n"
        " is honey and approximate dimensions are 6' x 2' 6\".  First come, first ser=\n"
        "ved!"})
                ]
