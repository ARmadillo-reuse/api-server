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

from web_api.models import EmailThread


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
        pass
    
    def parse_email_type(self, email):
        """
        Determine the type of object for the given email key-value dictionary.
        """
        pass
        
    
    def parse_email_thread(self, email):
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
    
