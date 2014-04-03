from django.test import TestCase
from web_api.models import *
import time

class TestItem(TestCase):   
    
    def setUp(self):
        self.t = EmailThread.objects.create(subject="Thread 1")
        self.p = NewPostEmail.objects.create(subject="Post 1", thread=self.t    )

    def test_item_has_name(self):        
        i = Item.objects.create(name="bobcat", post_email=self.p,
                                thread=self.t)
        
        self.assertEqual(i.name, "bobcat")

    def test_item_has_modification_date(self):
        i = Item.objects.create(name="bobcat", post_email=self.p,
                                thread=self.t)
        mod_time = i.modified
        time.sleep(0.001)
        i.name="big cat"
        i.save()
        self.assertNotEqual(i.modified, mod_time)

    def test_item_has_claimed_field(self):
        i = Item.objects.create(name="bobcat", post_email=self.p,
                                thread=self.t)
        # The field should be False by default
        self.assertFalse(i.claimed)
        i.claimed = True
        i.save()
        self.assertTrue(i.claimed)
        
