from django.test import TestCase
from web_api.models import *
import django.utils.timezone
import time

class TestNewPostEmail(TestCase):
    def setUp(self):
        self.thread = EmailThread.objects.create(subject="Thread 1")
        NewPostEmail.objects.create(subject="Thread 1", thread=self.thread)
        NewPostEmail.objects.create(subject="Thread 2", thread=self.thread)
        
    def test_new_post_email_has_received_time(self):
        p = NewPostEmail.objects.all()[0]
        self.assertTrue(p.received <= django.utils.timezone.now())

    def test_new_post_email_has_modified_time(self):
        p = NewPostEmail.objects.all()[0]
        mod = p.modified
        p.subject="Thread 1.1"
        time.sleep(0.001)
        p.save()
        self.assertTrue(p.modified >= mod)

    def test_new_post_email_has_items(self):
        p = NewPostEmail.objects.all()[0]
        i = Item.objects.create(name="bacon", thread=self.thread, post_email=p)

        self.assertIn(i, p.item_set.all())
