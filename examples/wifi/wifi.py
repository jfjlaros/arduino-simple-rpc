from simple_rpc import SocketInterface as Interface

import socket_speed_patch


interface = Interface('socket://192.168.21.53:1025')

for _ in range(50):
    print(interface.ping(10))
