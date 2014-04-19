import math

from django.test import TestCase

from web_api.models import EmailThread, NewPostEmail, Item, ClaimedItemEmail
from web_api.processing import EmailParser
import django.utils.timezone
import datetime


class TestEmailParser(TestCase):
    
    def test_can_pick_thread(self):
        for _id, subj in [(1, "This is the first thread"),
                         (2, "Second thread right here"),
                         (3, "but why not a third?"),
                         (4, "here's another one")]:
            thread = EmailThread.objects.create(id=_id, subject=subj)
            email = NewPostEmail.objects.create(subject=subj, thread=thread)
            
        parser = EmailParser()
        
        for _id, subj in [(1, "RE: This is the first thread"),
                         (2, "FW: Second thread right here"),
                         (3, "[RE] but why not a third?"),
                         (4, "here's another one"),
                         (None, "something else")]:
            email = {"subject": subj, "text": "", "from": "armadillo@mit.edu"}
            
            thread = parser.parse_email_thread(email)
            self.assertEqual(thread,
                             EmailThread.objects.get(id=_id) if _id else None)
    def test_ignores_old_threads(self):
        
        
        EmailThread.objects.create(id=0, subject="some subject here",
                                   modified=django.utils.timezone.now() -
                                   datetime.timedelta(7, 1))
        parser = EmailParser()
        thread = parser.parse_email_thread({"subject": "some subject here",
                                            "text": "",
                                            "from": "armadillo@mit.edu"})
        
        self.assertIsNone(thread)
        
            
    def test_dot_dist(self):
        words1 = list("abcdefg")
        parser = EmailParser()
        for w1, w2, val in [
                            ("abcdefg", "abc", 3./math.sqrt(21)),
                            ("aabbaa", "aba", 1),
                            ("abc", "def", 0)]:
            self.assertEqual(parser.dot_dist(list(w1), list(w2)), val)
    
    def test_parses_email_type(self):
        parser = EmailParser()
        test_texts = [("I took the bike map", ClaimedItemEmail),
                      ("claimed!", ClaimedItemEmail),
                      ("Taken", ClaimedItemEmail),
                      ("There are a bunch of mice, cables, and a couple of "
                       "chairs available for re-use outside of 35-338.",
                                NewPostEmail),
                      ("Free 4x8 foot slate chalkboard outside room 38-145. "
                       "It is large and heavy, you'll need at least 2 people "
                       "to carry it away.", NewPostEmail)]
        
        for text, expected in test_texts:
            email = {'text':text, 'from':'someone@mit.edu', 'subject':'test'}
            ret_type = parser.parse_email_type(email, EmailThread())
            self.assertEqual(expected, ret_type, "expected %s, got %s for '%s'"
                             % (expected, ret_type, text))
        
    def test_parses_post_email(self):
        parser = EmailParser()
        test_emails = [({'subject': "Broken rice cooker",
                         'from': 'vxiao@mit.edu', 'text': "Broken "
                         "black & decker rice cooker. Made about 2-3 cups "
                         "of rice. Won't turn on when plugged in, but maybe "
                         "you could use it for parts?"},
                        {'subject': "Broken rice cooker",
                         'sender': 'vxiao@mit.edu',
                         'text': "Broken "
                         "black & decker rice cooker. Made about 2-3 cups "
                         "of rice. Won't turn on when plugged in, but maybe "
                         "you could use it for parts?",
                         'received': django.utils.timezone.now(),
                         'modified': django.utils.timezone.now(),
                         'thread': {'subject': "Broken rice cooker",
                                    'modified': django.utils.timezone.now()},
                         'location': 'undetermined',
                         'items': [{'lat': '', 'lon': ''}] 
                         }),
                       ({"subject": "pair of shoes",
                         'from': "jsamuels@mit.edu",
                         'text': "Geier Wally loafers, heavy soled black.  "
                                 "Missing buckle but ready to be personalized. "
                                 "Size 40.  Outside 7-238 Rotch Library."},
                        {'subject': "pair of shoes",
                         'sender': "jsamuels@mit.edu",
                         'text': "Geier Wally loafers, heavy soled black.  "
                                "Missing buckle but ready to be personalized. "
                                "Size 40.  Outside 7-238 Rotch Library.",
                         'received': django.utils.timezone.now(),
                         'modified': django.utils.timezone.now(),
                         'thread': {'subject': 'pair of shoes',
                                    'modified': django.utils.timezone.now()},
                         'location': '7-238',
                         'items': [{'lat': '42.35928952', 'lon': '-71.09317868'}],
                         }),
                       ({"subject": "Misc computer cruft in E38 - routers, "
                                    "mice, drives, etc;\n plus music cds",
                         "from": "jjenkins@mit.edu",
                         'text': "Just moved a dusty pile of abandoned components "
                                 "to the lobby of E38. Origin unknown, functionality "
                                 "unknown. Please take and post.\n\ni/o data switch\n"
                                 "wireless mouse\nps/2 mice\nmicrocassette dictation "
                                 "machine\n2 usb desktop video cameras\nLinksys router "
                                 "(wireless-b)\nNetgear router (rm356)\nInternal "
                                 "drives: Zip, CD, CD r/rw, floppy\nLots of cables, "
                                 "drive rails, and case components\nRAM (mostly SIMMs)"},
                        {'location': 'E38'}
                        )
                       ]
        asserts = {datetime.datetime: lambda x,y:
                        self.assertTrue(abs(x-y) < datetime.timedelta(0,2))}
        
        for email, expected in test_emails:
            parsed = parser.parse(email)
            self.assertPropertiesEqual(parsed, expected, asserts)

    def assertPropertiesEqual(self, obj, expected, asserts={}):
        for key, value in expected.iteritems():
            self.assertTrue(hasattr(obj, key),
                            "Expected %s to have property %s" % (str(obj), key))
            if type(value) == dict:
                self.assertPropertiesEqual(getattr(obj, key), value, asserts)
            elif type(value) == list:
                for item, exp in zip(getattr(obj, key), value):
                    self.assertPropertiesEqual(item, exp, asserts)
            elif type(value) in asserts:
                asserts[type(value)](getattr(obj, key), value)
            else:
                self.assertEqual(getattr(obj, key), value)