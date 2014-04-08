import asyncore

from django.core.management.base import NoArgsCommand

from smtp.EmailReceiver import EmailReceiver


class Command(NoArgsCommand):

    help = "Start the userspace portion of the email receiver"

    option_list = NoArgsCommand.option_list

    def handle_noargs(self, **options):
        receiver = EmailReceiver('localhost', 7999)
        
        try:
            asyncore.loop()
        except KeyboardInterrupt:
            pass
