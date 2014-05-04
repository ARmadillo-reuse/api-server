'''
Created on Mar 28, 2014

@author: Alex Konradi
'''
from collections import Counter
from datetime import timedelta
from math import sqrt
import operator
import re

from django.db.models import Q
import django.utils.timezone
import nltk

from web_api.location.ItemPostLocator import ItemPostLocator
from web_api.models import EmailThread, NewPostEmail, ClaimedItemEmail, Item
from utils.utils import notify_all_users


class EmailParser(object):
    '''
    A class for parsing an email key-value dictionary into an object
    
    The parsed object is one of {NewPostEmail, ClaimedItemEmail} from
    web_api.models
    '''

    def __init__(self, thread_death_timeout=timedelta(7)):
        """
        Construct an EmailParser object with the specified timeout for a thread
        
        @param thread_death_timeout: the amount of time after which a thread is
               considered closed
        """
        self.thread_death_timeout = thread_death_timeout
        self.building_regex = re.compile(r"[ENWOC]{0,2}\d+(-[DG]?\d{2,})?$")
        self.locator = ItemPostLocator()
        pass
    
    def parse(self, email_dict):
        """
        Parse an email dictionary into one of {NewPostEmail, ClaimedItemEmail}
        from web_api.models
        """
        thread = self.parse_email_thread(email_dict)
        eml_type = self.parse_email_type(email_dict, thread)
        if eml_type == ClaimedItemEmail:
            return self.parse_claimed_item_email(email_dict, thread)
        elif eml_type == NewPostEmail:
            return self.parse_new_post_email(email_dict, thread)
    
    def parse_claimed_item_email(self, email, thread):
        if not thread:
            return None
        
        for item in thread.item_set.all():
            item.claimed = True
            item.save()

        notify_all_users()

        claimed_email = ClaimedItemEmail(subject=email["subject"],
                                         thread=thread, text=email["text"])

        claimed_email.save()
        claimed_email.items = thread.item_set.all()
        claimed_email.save()
        return claimed_email
        
    
    def parse_new_post_email(self, email, thread):
        if not thread:
            thread = EmailThread.objects.create(subject=email["subject"], thread_id="")
        
        post_email = NewPostEmail(sender=email["from"],
                                  subject=email["subject"],
                                  text=email["text"],
                                  thread=thread)
        
        item = Item(name=email["subject"], sender=email["from"], description=email["text"],
                    is_email=True)
        
        location = self.get_location_string(email["text"])
        if location:
            post_email.location = location
            item.location = location
            loc = self.locator.get_location(location)
            if loc:
                item.lat, item.lon = (loc["lat"], loc["lon"])
        else:
            post_email.location = "undetermined"
        
        thread.save()
        post_email.save()
        
        item.post_email = post_email
        item.thread = thread
        item.save()

        notify_all_users()
        
        return post_email
    
    
    def get_location_string(self, text):
        sentences = [nltk.word_tokenize(s) for s in nltk.sent_tokenize(text)]
        pos_tagged = (nltk.pos_tag(sentence) for sentence in sentences)
        
        candidates = []
        
        for sentence in pos_tagged:
            for i, (word, pos) in enumerate(sentence):
                if self.building_regex.match(word) and pos in ["CD", "NNP"]:
                    if i > 0 and sentence[i-1][1] == "IN":
                        candidates.append(word)
                        
                    elif i > 1 and sentence[i-1][0].lower() in ["room", "building"] \
                             and sentence[i-2][1] == "IN":
                        candidates.append(word)
                    
                    elif i == 1 and sentence[0][1] == "JJ":
                        candidates.append(word)
        
        if candidates:
            return max(candidates, key=lambda x: len(x))
        else:
            return None
        
    def parse_email_type(self, email, thread):
        """
        Determine the type of object for the given email key-value dictionary.
        """
        if not thread:
            return NewPostEmail
        
        if self.get_location_string(email["text"]):
            return NewPostEmail
                    
        return ClaimedItemEmail
        
    
    def parse_email_thread(self, email):
        """
        Find the thread for a specific email message
        """
        subject = re.sub(r"^\[?(re|fw):?\]?:?", "",
                         email["subject"], flags=re.IGNORECASE).strip()

        subject_words = subject.split()
        query = reduce(lambda x, y: x | y, (Q(subject__contains=word)
                       for word in set(subject_words)))
        time_filter = Q(modified__gt=django.utils.timezone.now()
                        - self.thread_death_timeout)
        
        possible_threads = EmailThread.objects.filter(query & time_filter)
        
        chosen_thread = (0, None)
        for thread in possible_threads:           
            matching_word_pct = self.dot_dist(subject_words,
                                              thread.subject.split())
            
            if matching_word_pct > chosen_thread[0]:
                chosen_thread = (matching_word_pct, thread)
        
        threshold = .9 if re.match(r"^\[?(re|fw):?\]?:?",
                                   email["subject"]) else .6
        if chosen_thread[0] > threshold:
            return chosen_thread[1]
        else:
            return None
    
    def dot_dist(self, words1, words2):
        w1, w2 = [Counter(words1), Counter(words2)]
        num = sum(w1[word] * w2[word] for word in w1)
        
        denom = sqrt(reduce(operator.mul,
                       (sum(x ** 2 for x in w.values())
                       for w in [w1, w2])))
        
        return float(num) / denom
    
