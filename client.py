import socket
from threading import Thread

PORT = 9999
GREETING = '>>> '
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', PORT))

def print_messages():
	while True:
		data = sock.recv(PORT)
		print('[Message for you]', data.decode('utf8'))
		print(end=GREETING, flush=True)


def put_messages():
	while True:
		message = input(GREETING)
		if len(message):
			sock.send(message.encode('utf8'))

t = Thread(target=print_messages).start()
put_messages()

