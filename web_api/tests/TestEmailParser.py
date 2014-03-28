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
        "Thanks,\nAmy\n\n"
        "-- \nAmy Stout\nComputer Science Librarian\n"
        "Massachusetts Institute of Technology\n617.253.4442\nastout@mit.edu"}),
                (32927, {'from': 'jennyqiu@mit.edu',
                         'subject': 'Re: 2 one gallon jugs of tropicana orange juice',
                         'text':
        "claimed!\n\nOn Wed, Aug 4, 2010 at 4:00 PM, Sarah Woodring Bates "
        "<swbates@mit.edu>wrote:\n\n> Hi,\n>\n> I have 2 one gallon jugs full of "
        "tropicana orange juice (unopened)\n> available\n> outside 3-237.\n>\n> "
        "First come first serve (by 5:30pm)\n>\n> ~Sarah Bates\n"
        "> _______________________________________________\n> To sub/unsubscribe or "
        "to see the list rules:\n> http://mailman.mit.edu/mailman/listinfo/reuse\n"
        ">\n\n\n\n-- \nJenny Qiu\nMassachusetts Institute of Technology (MIT)\n"
        "Course 2A - Mechanical Engineering\nClass of 2013"}),
                (34557, {'from': 'jbuz@mit.edu',
                         'subject': 'Re: maps, 54-1721',
                         'text':
                         "I took the bike map\n\n"
                        "On 11/22/2010 11:46 AM, Brian Rose wrote:\n"
                        "> A bunch of old road maps:\n>\n"
                        "> - Eastern Ontario\n"
                        "> - Canada (yes all of it)\n"
                        "> - Atlantic Provinces and Eastern Maine\n"
                        "> - Boston\n"
                        "> - Boston bike map\n"
                        "> - Canoe Routes of Algonquin Provincial Park (Ontario)\n>\n"
                        "> In the mailbox on the door of 54-1721.  "
                        "Don't email me, just take and post.\n>\n"
                        "> ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~\n"
                        "> Brian E.J. Rose, PhD\n"
                        "> Postdoctoral Associate, Climate Dynamics\n"
                        "> Department of Earth, Atmospheric and Planetary Sciences\n"
                        "> Massachusetts Institute of Technology\n"
                        "> office: 54-1721          phone: 617-253-5935\n"
                        "> email:  brose@mit.edu\n"
                        "> ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~\n>\n> "
                        "_______________________________________________\n"
                        "> To sub/unsubscribe or to see the list rules:  "
                        "http://mailman.mit.edu/mailman/listinfo/reuse"
                         })
                ]
