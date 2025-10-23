import threading
import socket
import sys

HOST = '127.0.0.1'
PORT = 12345

def receive_loop(sock):
    """Receive messages from server and print them."""
    try:
        while True:
            data = sock.recv(4096)
            if not data:
                break
            print(data.decode('utf-8'))
    except:
        pass
    finally:
        print("Disconnected by server.")
        sys.exit()

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    threading.Thread(target=receive_loop, args=(sock,), daemon=True).start()

    while True:
        msg = input()
        if msg.lower() == '/quit':
            sock.sendall(msg.encode('utf-8'))
            break
        sock.sendall(msg.encode('utf-8'))

    sock.close()

if __name__ == '__main__':
    main()
