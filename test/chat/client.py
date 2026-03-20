import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

HOST = "192.168.178.85"
PORT = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

def listen():
    while True:
        data = s.recv(1024)
        if not data:
            break
        chat.insert(tk.END, data.decode() + "\n")

def send_msg():
    target = entry_to.get()
    msg = entry_msg.get()
    s.sendall(f"{target}:{msg}".encode())
    entry_msg.delete(0, tk.END)

root = tk.Tk()
root.title("Chat Client")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

chat = scrolledtext.ScrolledText(frame, width=50, height=20)
chat.pack()

entry_to = tk.Entry(frame, width=20)
entry_to.pack()
entry_msg = tk.Entry(frame, width=40)
entry_msg.pack()

btn = tk.Button(frame, text="Senden", command=send_msg)
btn.pack()

client_id = input("ID: ")
s.sendall(client_id.encode())

threading.Thread(target=listen, daemon=True).start()

root.mainloop()
