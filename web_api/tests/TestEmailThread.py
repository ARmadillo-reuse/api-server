from django.test import TestCase
from web_api.models import *

class TestEmailThread(TestCase):
    def setUp(self):
        EmailThread.objects.create(subject="Thread 1")
        EmailThread.objects.create(subject="Thread 2")

    def test_thread_can_have_subject(self):
        e = EmailThread.objects.all()[0]
        e.subject = "blarg"
        e.save()

        self.assertEqual(EmailThread.objects.filter(subject="blarg").count(),1)

        
    def test_thread_can_have_items(self):
        e = EmailThread.objects.all()[0]

        p = NewPostEmail.objects.create(subject="Post 1", thread=e)
        
        item1 = Item.objects.create(name="Item A", thread=e, post_email=p)
        item2 = Item.objects.create(name="Item B", thread=e, post_email=p)

        items = e.item_set.all()
        for i in [item1, item2]:
            self.assertIn(i, items)
            self.assertEqual(i.thread, e)

        self.assertEqual(EmailThread.objects.all()[1].item_set.count(),0)

    def test_thread_can_have_post_emails(self):
        e = EmailThread.objects.all()[0]
        
        p1 = NewPostEmail.objects.create(subject="Post A", thread=e)
        p2 = NewPostEmail.objects.create(subject="Post B", thread=e)

        postEmails = e.newpostemail_set.all()
        for p in [p1, p2]:
            self.assertIn(p, postEmails)
            self.assertEqual(p.thread, e)

        self.assertEqual(EmailThread.objects.all()[1].newpostemail_set.count(),0)
