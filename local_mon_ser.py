import socket


server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
server_socket.settimeout(0.001)
monitor_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
monitor_socket.settimeout(0.001)
monitor_socket.bind(("127.0.0.1", 7000))
monitor_address = ''
server_address = ''
lost_server_count = 0
while True:
    try:
        mon_msg = monitor_socket.recvfrom(100000)
        if server_address != '':
            server_socket.sendto(mon_msg[0], server_address)
        else:
            server_socket.sendto(mon_msg[0], ("127.0.0.1", 6000))
        monitor_address = mon_msg[1]
        if str(mon_msg[0]).find('dispbye') > 0:
            print('###############################')
            server_address = ''
            server_socket.close()
            server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
            server_socket.settimeout(0.001)
        print('monitor', mon_msg)
    except:
        pass
    if monitor_address != '':
        try:
            ser_msg = server_socket.recvfrom(100000)
            lost_server_count = 0
            print('server', ser_msg)
            server_address = ser_msg[1]
            monitor_socket.sendto(ser_msg[0], monitor_address)
            print('server', ser_msg)
        except:
            lost_server_count += 1
            pass
    if lost_server_count > 1000:
        server_address = ''
        server_socket.close()
        server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        server_socket.settimeout(0.001)
        monitor_socket.close()
        monitor_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        monitor_socket.settimeout(0.001)
        monitor_socket.bind(("127.0.0.1", 7000))
        monitor_address = ''
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        lost_server_count = 0
