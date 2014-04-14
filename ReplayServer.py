import asyncore
import pickle
import socket

class ReplayServer(asyncore.dispatcher):
    def __init__(self, address, buffer):
        asyncore.dispatcher.__init__(self)
        
        self.buffer = buffer
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
            self.replay(handler)
    
    def handle_close(self):
        self.close()

    def replay(self, handler):
        handler.send(self.buffer)
    

class SendHandler(asyncore.dispatcher_with_send):
    
    def __init__(self, connection, outgoing_server):
        asyncore.dispatcher_with_send.__init__(self, connection)
        
        self.outgoing_server = outgoing_server
    
    def handle_close(self):
        asyncore.dispatcher_with_send.handle_close(self)
        self.outgoing_server.remove_client(self)

def run():
    with open("incoming.log") as f:
        data = f.read()

    replay = ReplayServer(('localhost', 7999), data)
    
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
        run()
