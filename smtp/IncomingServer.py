import asyncore
import pickle
from smtpd import SMTPServer
import socket


class IncomingServer(SMTPServer):

    def __init__(self, outgoing, *args, **kwargs):
        SMTPServer.__init__(self, *args, **kwargs)
        self.outgoing = outgoing
        self.log = open("IncomingServer.log", "w")
    
    def process_message(self, peer, mailfrom, rcpttos, data):
        pickle_data = pickle.dumps({"peer": peer, "mailfrom": mailfrom,
                      "rcpttos": rcpttos, "data": data})
        print "received message"
        self.outgoing.relay(pickle_data)

class OutgoingServer(asyncore.dispatcher):
    def __init__(self, address):
        asyncore.dispatcher.__init__(self)
        
        self.clients = []
        
        self.out_socket = self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(address)
        self.listen(5)
    
    def handle_accept(self):
        pair = self.accept();
        if pair:
            conn = pair[0]
            print 'Incoming connection'
            handler = SendHandler(conn, self)
            self.clients.append(handler)
    
    def handle_close(self):
        self.close()
        
    def relay(self, data):
        print "relaying message"
        for con in self.clients:
            con.send(data)
            # Send the null terminator
            con.send("\x00")
    
    def remove_client(self, client):
        self.clients.remove(client)
    

class SendHandler(asyncore.dispatcher_with_send):
    
    def __init__(self, connection, outgoing_server):
        asyncore.dispatcher_with_send.__init__(self, connection)
        
        self.outgoing_server = outgoing_server
    
    def handle_close(self):
        asyncore.dispatcher_with_send.handle_close(self)
        self.outgoing_server.remove_client(self)

def run():
    outgoing = OutgoingServer(('localhost', 7999))
    incoming = IncomingServer(outgoing, ('0.0.0.0', 25), None)
    
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
        run()
