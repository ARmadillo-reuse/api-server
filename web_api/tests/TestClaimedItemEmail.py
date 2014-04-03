from django.test import TestCase
from web_api.models import *
import django.utils.timezone
import time

class TestClaimedItemEmail(TestCase):
    def setUp(self):
        self.thread = EmailThread.objects.create(subject="Thread 1")
        self.post = NewPostEmail.objects.create(subject="A", thread = self.thread)
        ClaimedItemEmail.objects.create(subject="Thread 1", thread=self.thread)
        ClaimedItemEmail.objects.create(subject="Thread 2", thread=self.thread)
        self.item = Item.objects.create(name="bacon", thread=self.thread,
                                        post_email=self.post)
        
    def test_claimed_item_email_has_received_time(self):
        c = ClaimedItemEmail.objects.all()[0]
        self.assertTrue(c.received <= django.utils.timezone.now())

    def test_new_post_email_has_modified_time(self):
        c = ClaimedItemEmail.objects.all()[0]
        mod = c.modified
        time.sleep(0.01)
        c.subject="Thread 1.1"
        c.save()
        self.assertTrue(c.modified > mod)

    def test_claimed_item_email_has_items(self):
        c = ClaimedItemEmail.objects.all()[0]
        self.item.claimeditememail_set.add(c)
        self.assertIn(self.item, c.items.all())
