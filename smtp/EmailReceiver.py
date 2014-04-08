import asyncore
import pickle
import socket
from web_api.processing.EmailPreProcessor import EmailPreProcessor
from web_api.processing.EmailParser import EmailParser


class EmailReceiver(asyncore.dispatcher):
    '''
    Connects to a receiving SMTP server and receives relayed emails
    '''

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        self.buffer = ""
        self.preprocessor = EmailPreProcessor()
        self.parser = EmailParser()
    
    def handle_read(self):
        self.buffer += self.recv(8192)
        print len(self.buffer)
        if "\x00" in self.buffer:
            email = self.buffer[:self.buffer.find('\x00')]
            self.parse_incoming_email(email)
            self.buffer = self.buffer[len(email)+1:]
    
    def parse_incoming_email(self, email_pickle):
        email = pickle.loads(email_pickle)
        text = email["text"]
        processed = self.preprocessor.parse(text)
        parsed = self.parser.parse(processed)
        self.handle_parsed_email(parsed)
    
    def handle_parsed_email(self, parsed):
        parsed.save()


def run():
    receiver = EmailReceiver('localhost', 7999)
    
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
        run()
