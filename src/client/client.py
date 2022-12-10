#!/usr/bin/python3

import argparse
import socket
import select

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="")
    args = parser.parse_args()

    server_ip = "192.168.0.115"
    server_port = 2222

    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                print("Connecting to server")
                sock.settimeout(None)
                sock.connect((server_ip, server_port))
            except:
                print("Reconnecting...")
                continue

            while True:
                try:
                    data = sock.recv(1024)
                    print(data.decode('utf-8'))
                    sock.sendall(data)
                except:
                    print("Server disconnected")
                    break #reconnect
