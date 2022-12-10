#!/usr/bin/python3

import argparse
import socket
import select
from time import sleep
import threading

PING_TIMEOUT=1

def handle_connection(conn, addr):
    while True:
        try:
            msg = "ping"
            conn.sendall(msg.encode('utf-8'))
            data = conn.recv(len(msg)).decode('utf-8')
            print(data)
        except: 
            print("Disconnected")
            conn.close()
            break
        sleep(PING_TIMEOUT)

def start(sock):
    sock.listen()
    while True:
        conn, addr = sock.accept()
        thread = threading.Thread(target=handle_connection, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="")
    args = parser.parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(("192.168.0.115", 2222))
        start(server)
