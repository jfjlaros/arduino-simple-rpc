from serial.urlhandler import protocol_socket


protocol_socket.time.sleep = lambda x: None
