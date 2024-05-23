import socket
import threading

SERVER_HOST = '10.33.14.21'
SERVER_PORT = 1234
MAX_CLIENTS = 10
connected_clients = []

def broadcast_message(client_socket, msg):
    client_socket.sendall(msg.encode())

def handle_client_messages(client_socket, user_name):
    while True:
        msg = client_socket.recv(2048).decode('utf-8')
        if msg:
            formatted_msg = f"{user_name}!{msg}"
            send_to_all_clients(formatted_msg)
        else:
            print(f"Received empty message from {user_name}")

def send_to_all_clients(msg):
    for client in connected_clients:
        broadcast_message(client[1], msg)

def handle_new_client(client_socket):
    while True:
        user_name = client_socket.recv(2048).decode('utf-8')
        if user_name:
            connected_clients.append((user_name, client_socket))
            welcome_msg = f"SERVER!{user_name} has joined the chat!"
            send_to_all_clients(welcome_msg)
            break
        else:
            print("Received empty username")
    
    threading.Thread(target=handle_client_messages, args=(client_socket, user_name)).start()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"Server is running on {SERVER_HOST}:{SERVER_PORT}")
    try:
        server_socket.bind((SERVER_HOST, SERVER_PORT))
    except Exception as e:
        print(f"Failed to bind host and port: {e}")

    server_socket.listen(MAX_CLIENTS)
    
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"New connection from {client_address[0]}:{client_address[1]}")
        threading.Thread(target=handle_new_client, args=(client_socket,)).start()

if __name__ == '__main__':
    start_server()
