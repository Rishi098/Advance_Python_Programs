import threading
import socket

HOST = '0.0.0.0'
PORT = 12345

clients = {}  # map from client socket to username

lock = threading.Lock()

def broadcast(msg, exclude_sock=None):
    """Send msg to all connected clients except exclude_sock."""
    with lock:
        for sock in clients:
            if sock != exclude_sock:
                try:
                    sock.sendall(msg.encode('utf-8'))
                except:
                    pass

def handle_client(client_sock, addr):
    """Thread: handle one connected client."""
    try:
        client_sock.sendall("Enter your username: ".encode('utf-8'))
        username = client_sock.recv(1024).decode('utf-8').strip()
        if not username:
            client_sock.close()
            return
        with lock:
            clients[client_sock] = username
        welcome = f"*** {username} joined the chat ***"
        broadcast(welcome)
        client_sock.sendall("You are connected. Type messages below:\n".encode('utf-8'))
        while True:
            data = client_sock.recv(4096)
            if not data:
                break
            text = data.decode('utf-8').strip()
            if text.lower() == '/quit':
                break
            message = f"[{username}] {text}"
            broadcast(message, exclude_sock=client_sock)
    except Exception as e:
        print("Error:", e)
    finally:
        # cleanup
        with lock:
            if client_sock in clients:
                name = clients.pop(client_sock)
                broadcast(f"*** {name} left the chat ***")
        client_sock.close()

def main():
    """Start the server, accept new connections."""
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((HOST, PORT))
    server_sock.listen(5)
    print(f"Chat server listening on {HOST}:{PORT}")
    try:
        while True:
            client_sock, addr = server_sock.accept()
            print("Connection from", addr)
            threading.Thread(target=handle_client, args=(client_sock, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        server_sock.close()

if __name__ == '__main__':
    main()
