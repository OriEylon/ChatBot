import socket
import threading
import datetime
import logging
import configparser
BUFF_SIZE = 4096


def handler(client, addrs):
    # print('entered client thread\n')
    client.send(bytes('welcome to the chat bot!', 'utf-8'))
    address = addrs[0]+':'+str(addrs[1])
    while True:
        try:
            if client not in connections:
                # client.send(bytes('please enter your name:', 'utf-8'))
                # client_name = str(client.recv(BUFF_SIZE), encoding='ascii')
                client_name = first_time(client, address)
                reg_time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                Register(client, address, client_name, reg_time)
                client.send(bytes(f"registered as {client_name}", 'utf-8'))
            else:
                client_name = connections[client]
            message = str(client.recv(BUFF_SIZE), encoding='ascii')
            received_time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            logger.info(f'{client_name}> {message}, on {received_time}')
            Send(message, connections, received_time)

        except:
            disconnect(client, address)
            break


def first_time(client, address):
    first_time_statement = "please choose a username: press (1) to enter from keyboard or (2) to read from config file"
    username = ''
    while True:
        client.send(bytes(first_time_statement, encoding='utf-8'))
        choice = str(client.recv(BUFF_SIZE), encoding='ascii')
        if choice == '1':
            client.send(bytes("please type your username:", encoding='utf-8'))
            username = str(client.recv(BUFF_SIZE), encoding='ascii')
            break
        elif choice == '2':
            client.send(bytes("please enter path to config file:", encoding='utf-8'))
            config = str(client.recv(BUFF_SIZE), encoding='ascii')
            parser = configparser.ConfigParser()
            parser.read(config)
            username = parser.get('USERNAME', 'username')
            break
        else:
            continue
    return username



def disconnect(client, address):
    client.send(b'bye')
    logger.info(f"timeout {address}")
    connections.pop(client, None)
    client.close()


def Register(client, address, client_name, time):
    connections[client] = client_name
    logger.info(f"Registered {address} as {client_name}, on {time}")


def Send(message, clients, time):
    for client in clients:
        client.send(bytes(message, 'utf-8'))
        logger.info(f'Server> {message} to {addrs[0]+":"+str(addrs[1])}, on {time}')


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logging.basicConfig(filename='logger.log', level=logging.DEBUG)
    logger = logging.getLogger()
    connections = {}
    sock.bind(('0.0.0.0', 9999))
    sock.listen()
    print('server socket: ', sock)
    while True:
        conn, addrs = sock.accept()
        print('accepted connection ', conn, 'from ', addrs)
        logger.info(f'accepted connection {conn} from {addrs} on {datetime.datetime.now()}')
        conn.settimeout(60)
        client_Thread = threading.Thread(target=handler, args=[conn, addrs], daemon=True).start()