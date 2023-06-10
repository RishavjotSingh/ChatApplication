import socket
import threading

HOST = '127.0.0.1'
PORT = 8000

connected_clients = []  # to keep track of the connected clients


def send_message(client_socket, message):
    client_socket.sendall(message.encode())


def broadcast_message_in_chat(message):
    for client in connected_clients:
        send_message(client[1], message)


def receive_client_messages(client_socket, username):
    while True:
        received_message = client_socket.recv(2048).decode('utf-8')

        if received_message is not None and not received_message.strip().isspace():
            broadcast_message = username + "~" + received_message
            broadcast_message_in_chat(broadcast_message)


def handle_client(client_socket):
    # waiting for the new client to choose the username they want to choose for chat
    while True:
        username = client_socket.recv(2048).decode('utf-8')

        if username is not None and not username.strip().isspace():
            connected_clients.append((username, client_socket))
            welcome_message = "SERVER~" + username + ", welcome to the chat"
            broadcast_message_in_chat(welcome_message)
            break

    threading.Thread(target=receive_client_messages, args=(client_socket, username, )).start()


# main function
def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # binding the server to the host and the port
        server_socket.bind((HOST, PORT))
        print('Running server on (', HOST, ",", PORT, ")")
    except:
        print('Something went wrong while binding to the host and port')

    server_socket.listen()

    while True:
        connection, address = server_socket.accept()
        print("User: (" + address[0], ", ", address[1], ") connected in.")

        threading.Thread(target=handle_client, args=(connection,)).start()


if __name__ == '__main__':
    main()