import math

from django.test import TestCase

from web_api.models import EmailThread
from web_api.processing import EmailParser


class TestEmailParser(TestCase):
    def test_can_pick_thread(self):
        for id, subj in [(1, "This is the first thread"),
                         (2, "Second thread right here"),
                         (3, "but why not a third?"),
                         (4, "here's another one")]:
            EmailThread.objects.create(id=id, subject=subj)
            
        for id, subj in [(1, "RE: This is the first thread"),
                         (2, "FW: Second thread right here"),
                         (3, "[RE] but why not a third?"),
                         (4, "here's another one"),
                         (None, "something else")]:
            email = {"subject": subj, "text": "", "from": "armadillo@mit.edu"}
            
            parser = EmailParser()
            thread = parser.parse_email_thread(email)
            self.assertEqual(thread,
                             EmailThread.objects.get(id=id) if id else None)
            
    def test_dot_dist(self):
        words1 = list("abcdefg")
        parser = EmailParser()
        for w1, w2, val in [
                            ("abcdefg", "abc", 3./math.sqrt(21)),
                            ("aabbaa", "aba", 1),
                            ("abc", "def", 0)]:
            self.assertEqual(parser.dot_dist(list(w1), list(w2)), val)
        
