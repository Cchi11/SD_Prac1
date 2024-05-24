import threading
import time
from concurrent import futures

import grpc
import random
# import the generated classes
import private_chat_pb2
import private_chat_pb2_grpc
import name_server_pb2
import name_server_pb2_grpc
import socket

from grpc_server import PrivateChatServicer


class ChatClient:
    def __init__(self, self_name, self_connection):
        self.name = self_name
        self.connection = self_connection


# Connect to NameServer
redis_channel = grpc.insecure_channel('0.0.0.0:50051')
redis_stub = name_server_pb2_grpc.NameServerStub(redis_channel)

self_name = input('Enter your name: ')

self_client = name_server_pb2.ClientNameRequest(client_name=
                                                self_name)
self_client_address = redis_stub.GetClientInfo(self_client)

while True:
    if self_client_address.connectionInfo.client_address_and_port:
        self_client_address = self_client_address.connectionInfo.client_address_and_port
        break
    else:
        self_name = input('Client not found. Enter your name: ')
        self_client = name_server_pb2.ClientNameRequest(client_name=self_name)
        self_client_address = redis_stub.GetClientInfo(self_client)

client = ChatClient(self_name, self_client_address)

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

# get other client address
other_client_name = input('Enter other client_name: ')
other_client = name_server_pb2.ClientNameRequest(client_name=other_client_name)
other_client_grpc = redis_stub.GetClientInfo(other_client)
other_client_address = None
while True:
    if other_client_grpc.connectionInfo.client_address_and_port:
        other_client_address = other_client_grpc.connectionInfo.client_address_and_port
        break
    else:
        other_client_name = input('Client not found. Enter other client_name: ')
        other_client = name_server_pb2.ClientNameRequest(client_name=other_client_name)
        other_client_address = redis_stub.GetClientInfo(other_client)

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
