import socket
import threading

HOST = "0.0.0.0"
PORT = 5000

clients = {}

def handle_client(conn):
    client_id = conn.recv(1024).decode()
    if not client_id:
        conn.close()
        return
    clients[client_id] = conn
    while True:
        data = conn.recv(1024)
        if not data:
            break
        target, msg = data.decode().split(":", 1)
        if target in clients:
            clients[target].sendall(f"{client_id}:{msg}".encode())
    conn.close()
    if client_id in clients:
        del clients[client_id]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, _ = s.accept()
        threading.Thread(target=handle_client, args=(conn,), daemon=True).start()
