import socket
import threading

HOST = '127.0.0.1'
PORT = 44101

clients = []
aliases = []

try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print("socket listening")
except Exception as err:
    print(f"An error occured: {str(err)}")

def broadcast(msg, exclude=None):
    try:
        for client in clients:
            if client == exclude:
                continue
            else:
                client.send(msg)
    except:
        print('fail broadcast')
    
def receive():
    while True:
        print('server running and listening')
        client, addr = server.accept()
        print(f'connection established with {str(addr)}')
        client.send('key?'.encode('utf-8'))
        key = client.recv(1024).decode('utf-8')
        clients.append(client)
        broadcast(f'{key} has joined the chat'.encode('utf-8'))
        client.send(b'connection sucessuful')
        thread = threading.Thread(target=handel_client, args=(client, key))
        thread.start()

def handel_client(client, key):
    while True:
        try:
            msg = client.recv(1024)
            broadcast(msg, exclude=client)
        except:
            client.close()
            broadcast(f'{str(key)} has left the the chat'.encode('utf-8'))
            break
        
if __name__ == "__main__":
    receive()