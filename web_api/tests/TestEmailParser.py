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
        
