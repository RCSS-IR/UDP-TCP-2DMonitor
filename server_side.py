import socket
import time
import signal
import sys


debug = False
args = sys.argv
show_help = False
for arg in args[1:]:
    if arg.find('help') != -1 or arg.find('--h') != -1:
        show_help = True
if len(args) not in [1, 4]:
    show_help = True

if show_help:
    print('usage: python *.py ServerIp ServerPort TcpPort')
    exit()

server_ip = '127.0.0.1'
server_port = 6000
tcp_port = 7000
if len(args) > 1:
    server_ip = args[1]
    server_port = int(args[2])
    tcp_port = int(args[3])

msg_size = 100000
udp: socket.socket = None


def reset_udp():
    global udp
    print('Reset UDP - Start')
    if udp:
        udp.close()
    udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    udp.settimeout(0.0001)
    print('Reset UDP - Done')


reset_udp()
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.settimeout(0.0001)
tcp.bind(("127.0.0.1", tcp_port))
tcp_conn: socket.socket = None
tcp_addr = ''


def add_monitor():
    global tcp_conn, tcp_addr
    tcp.listen()

    while True:
        try:
            tcp_conn, tcp_addr = tcp.accept()
            break
        except:
            pass
        time.sleep(1)


add_monitor()


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    tcp.close()
    udp.close()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


monitor_address = ''
server_address = ''
lost_server_count = 0
while True:
    try:
        tcp_conn.settimeout(0.0001)
        tcp_msg = tcp_conn.recvfrom(msg_size)
        tcp_conn.settimeout(0.0001)
        if debug:
            print('From TCP:', tcp_msg)
        if len(tcp_msg[0]) == 0:
            if debug:
                print('Message length is 0')
            add_monitor()
        if str(tcp_msg).find('initmon') >= 0:
            print('receive initmon')
            server_address = ''
            reset_udp()

        if server_address != '':
            udp.sendto(tcp_msg[0], server_address)
        else:
            udp.sendto(tcp_msg[0], (server_ip, server_port))

        if str(tcp_msg[0]).find('dispbye') > 0:
            print('receive dispbye')
            server_address = ''
            reset_udp()
    except Exception as e:
        if str(e.args).find('timed out') == -1:
            print(e.args)
        elif debug:
            print(e.args)
        pass
    try:
        ser_msg = udp.recvfrom(msg_size)
        if debug:
            print('From Server:', ser_msg)
        server_address = ser_msg[1]
        tcp_conn.sendall(ser_msg[0])
    except Exception as e:
        if str(e.args).find('timed out') == -1:
            print(e.args)
        elif debug:
            print(e.args)
        pass
