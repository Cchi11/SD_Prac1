import threading
import time
from concurrent import futures

import grpc
import random
# import the generated classes
import private_chat_pb2
import private_chat_pb2_grpc
import socket

from grpc_server import PrivateChatServicer


class ChatClient:
    def __init__(self, self_name):
        self.name = self_name
        self.port = random.randint(50000, 60000)
        self.address = '0.0.0.0'
        self.connection = self.address + ':' + str(self.port)


self_name = input('Enter your name: ')
client = ChatClient(self_name)

# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

# use the generated function `add_InsultingServiceServicer_to_server`
# to add the defined class to the server
private_chat_pb2_grpc.add_PrivateChatServiceServicer_to_server(
    PrivateChatServicer(), server)

# listen on client port
print('Starting server. Listening on port: ' + client.connection + '.')
server.add_insecure_port(client.connection)
server.start()

other_client_port = input('Enter other client port: ')
other_client_address = '0.0.0.0:' + other_client_port
channel = grpc.insecure_channel(other_client_address)
stub = private_chat_pb2_grpc.PrivateChatServiceStub(channel)

print('Connected to other client. Start chatting!')

try:
    while True:
        input_message = input()
        message = private_chat_pb2.clientMessage(clientName=client.name, clientMessage=input_message)
        stub.sendMessage(message)
        time.sleep(0.5)
except KeyboardInterrupt:
    server.stop(0)
    print('Server stopped')
    exit()
