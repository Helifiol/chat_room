import threading
import socket

key = input("Enter username >> ")
# server_ip = input("Enter Server IP: ")
# port = input("Enter Port: ")
server_ip = '127.0.0.1'
port = 44101

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((str(server_ip), int(port)))

def client_recv():
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            if msg == 'key?':
                client.send(key.encode('utf-8'))
            else:
                print(msg)
        except:
            print("error!")
            client.close()
            break

def client_send():
    while True:
        msg = f'{key}: {input("")}'
        print(msg)
        client.send(msg.encode('utf-8'))

receive_thread = threading.Thread(target=client_recv)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()