#!/usr/bin/env python3
import socket
import sys
import threading
import datetime


def hexdump(data):
    lines = []
    for i in range(0, len(data), 16):
        chunk = data[i:i + 16]
        hex_part = ' '.join(f'{b:02x}' for b in chunk)
        ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
        lines.append(f'{i:04x}  {hex_part:<48}  {ascii_part}')
    return '\n'.join(lines)


def log(prefix, data, addr=None):
    ts = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]
    src = f' from {addr}' if addr else ''
    print(f'\n[{ts}] {prefix}{src} ({len(data)} bytes)')
    print(hexdump(data))


def tcp_server(host, port):
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((host, port))
    srv.listen(5)
    print(f'TCP listening on {host}:{port}')
    while True:
        conn, addr = srv.accept()
        print(f'\nTCP connection from {addr}')
        threading.Thread(target=handle_tcp, args=(conn, addr), daemon=True).start()


def handle_tcp(conn, addr):
    with conn:
        while True:
            data = conn.recv(4096)
            if not data:
                print(f'TCP connection closed by {addr}')
                return
            log('TCP recv', data, addr)


def udp_server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    print(f'UDP listening on {host}:{port}')
    while True:
        data, addr = sock.recvfrom(4096)
        log('UDP recv', data, addr)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(f'Usage: {sys.argv[0]} <tcp|udp> <port> [bind-ip, default 192.168.0.70]')
        sys.exit(1)
    proto, port = sys.argv[1], int(sys.argv[2])
    host = sys.argv[3] if len(sys.argv) > 3 else '192.168.0.70'
    if proto == 'tcp':
        tcp_server(host, port)
    elif proto == 'udp':
        udp_server(host, port)
    else:
        print('protocol must be tcp or udp')
        sys.exit(1)
