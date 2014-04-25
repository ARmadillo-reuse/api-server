from django.contrib import admin
from web_api.models import Item, UserLogEvent, EmailThread, NewPostEmail, ClaimedItemEmail, GcmUser
# Register your models here.
admin.site.register(Item)
admin.site.register(UserLogEvent)
admin.site.register(EmailThread)
admin.site.register(NewPostEmail)
admin.site.register(ClaimedItemEmail)
admin.site.register(GcmUser)
