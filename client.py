import socket
import select
import sys
import threading
BUFF_SIZE = 4096


def send_msg(srv):
    while True:
        srv.send(bytes(input(), encoding='utf-8'))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('wrong input, please enter ip address and port\n')
        exit(1)
    ip = str(sys.argv[1])
    port = int(sys.argv[2])
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((ip, port))
    # server.setblocking(False)
    input_thread = threading.Thread(target=send_msg, args=[server], daemon=True)
    input_thread.start()
    while True:
        try:
            from_server = server.recv(BUFF_SIZE)
            if not from_server:
                break
            print(str(from_server, encoding='ascii'))
        except:
            continue