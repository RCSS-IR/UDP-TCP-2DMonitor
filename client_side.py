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
if len(args) not in [1, 3]:
    show_help = True

if show_help:
    print('usage: python *.py TcpPort MonitorPort')
    exit()

monitor_port = 6000
tcp_port = 7000
if len(args) > 1:
    tcp_port = int(args[1])
    monitor_port = int(args[2])

msg_size = 100000
tcp: socket.socket = None


def reset_tcp():
    global tcp
    print('Reset TCP - Start')
    if tcp:
        tcp.close()
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.settimeout(0.0001)
    while True:
        try:
            tcp.connect(('127.0.0.1', tcp_port))
            time.sleep(0.5)
            break
        except Exception as e:
            if debug:
                print(e.args)
            pass
    tcp.settimeout(0.0001)
    print('Reset TCP - Done')


reset_tcp()
udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
udp.settimeout(0.0001)
udp.bind(("127.0.0.1", monitor_port))


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    tcp.close()
    udp.close()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

monitor_address = ''
server_address = ''
tcp.sendall(b'initmon')
while True:
    try:
        mon_msg = udp.recvfrom(msg_size)
        if debug:
            print('monitor', mon_msg)
        tcp.sendall(mon_msg[0])
        monitor_address = mon_msg[1]
    except Exception as e:
        if str(e.args).find('timed out') == -1:
            print(e.args)
        elif debug:
            print(e.args)
        pass
    if monitor_address != '':
        try:
            ser_msg = tcp.recv(msg_size)
            if debug:
                print('server', ser_msg)
            if len(ser_msg) == 0:
                if debug:
                    print('Length of message is 0')
                reset_tcp()

            udp.sendto(ser_msg, monitor_address)
        except Exception as e:
            if str(e.args).find('timed out') == -1:
                print(e.args)
            elif debug:
                print(e.args)
            pass
