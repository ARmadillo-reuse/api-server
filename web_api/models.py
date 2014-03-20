from django.db import models

# Create your models here.

class Item(models.Model):
    """
    An item mentioned in a Reuse email
    """

    """The name of this item"""
    name = models.CharField(max_length=256)

    """The NewPostEmail in which this Item was first mentioned"""
    post_email = models.ForeignKey('NewPostEmail')

    """Whether or not this item has been claimed already (default False)"""
    claimed = models.BooleanField(default=False)

    """The thread to which this item belongs"""
    thread = models.ForeignKey('EmailThread', null=True)

    """The last time this item was updated"""
    modified = models.DateTimeField(auto_now=True)


class AbstractEmail(models.Model):
    class Meta:
        abstract = True

    """The email address of the person who sent this email"""
    sender = models.CharField(max_length=64)

    """The subject of the email"""
    subject = models.CharField(max_length=256)

    """The complete text of the email"""
    text = models.TextField()

    # The auto_now_add parameter declares that the value of the received field
    # is set to the time the object was created.
    """When the email was received by the server"""
    received = models.DateTimeField(auto_now_add=True)

    # The auto_now parameter declares that the value of the updated field is set
    # to the time the object was last updated.
    """When the email was last updated"""
    modified = models.DateTimeField(auto_now=True)

    """The thread this email is a part of"""
    thread = models.ForeignKey('EmailThread')

    

class NewPostEmail(AbstractEmail):
    """
    An email with a list of items that have been posted on Reuse
    """

    """
    Where the posted item(s) is(are) located.
    Can be a room number, an address, or something else
    """
    location = models.CharField(max_length=256)

    
class ClaimedItemEmail(AbstractEmail):
    """An email that lists some items as claimed"""
    
    """The items which this email marked as claimed"""
    items = models.ManyToManyField('Item')


class EmailThread(models.Model):
    """
    A group of one or more emails in the same conversation/thread and the
    associated items
    """
    
    """The subject of the email thread"""
    subject = models.CharField(max_length=256)
