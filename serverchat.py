import socket
from threading import Thread


HOST = 'localhost'
PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clients = set()

# Отправляет сообщения всем, кроме самого отправителя
def broadcast(sender, data):
	print('Broadcasting the message:', data.decode('utf8'))
	for client in clients:
		if client != sender:
			client.sendall(data)

def continue_receive_from(client, address):
	print('New connection', address)
	clients.add(client)
	print('Total connections:', len(clients))
	try:
		while True:
			# Будем слушать вечно (в отдельном потоке)
			# Если клиент оборвал соединение, вернётся 0 байт,
			# выходим в таком случае и удаляем клиента (ниже)
			data = client.recv(PORT)
			if len(data) == 0:
				break
			broadcast(client, data)
	except Exception as e:
		print('Error', e)
	finally:
		clients.remove(client)
		print('Disconnect', address)
		print('Total connections:', len(clients))


def start_server():
	try:
		sock.bind((HOST, PORT))
		sock.listen(5)
		while True:
			# приняли клиента, запустили в новом потоке, слушаем дальше
			# (не самая лучшая идея, создавать потоки, но для примера сойдёт)
			params = sock.accept()
			Thread(target=continue_receive_from, args=params).start()
	except Exception as e:
		print('except', e)
	finally:
		sock.close()

start_server()
print('ok')
