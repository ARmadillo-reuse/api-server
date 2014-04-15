import asyncore
import pickle
import socket
import traceback
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
        self.log = open("EmailReceiver.log","a")

    
    def handle_read(self):
        self.buffer += self.recv(8192)
        print len(self.buffer)
        if "\x00" in self.buffer:
            email = self.buffer[:self.buffer.find('\x00')]
            if email:
                try:
                    self.parse_incoming_email(email)
                except Exception as e:
                    self.log.write("\n")
                    self.log.write("parsing '%s'\n" % email)
                    self.log.write(traceback.format_exc(e))
                    self.log.flush()
            self.buffer = self.buffer[(self.buffer.find('\x00')+1):]
    
    def parse_incoming_email(self, email_pickle):
        self.log.write("Parsing incoming")
        email = pickle.loads(email_pickle)
        text = email["data"]
        try:
            self.log.write("subject: %s" % email["subject"])
        except Exception as e:
            pass
        self.log.flush()
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
