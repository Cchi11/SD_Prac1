import threading
import time
from concurrent import futures

import grpc
import yaml
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


def printMenu():
    print()
    print("+" + "-" * 28 + "+")
    print("|" + " " * 28 + "|")
    print("|      Chat Application      |")
    print("|" + " " * 28 + "|")
    print("+" + "-" * 28 + "+")
    print("| 1. Connect chat            |")
    print("| 2. Subscribe to group chat |")
    print("| 3. Discover chat           |")
    print("| 4. Access insult channel   |")
    print("| 5. Exit                    |")
    print("+" + "-" * 28 + "+")
    print()


def privateChat(user: ChatClient):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # use the generated function `add_InsultingServiceServicer_to_server`
    # to add the defined class to the server
    private_chat_pb2_grpc.add_PrivateChatServiceServicer_to_server(
        PrivateChatServicer(), server)
    # listen on client port
    # print('Starting server. Listening on port: ' + user.connection + '.')
    server.add_insecure_port(user.connection)
    server.start()
    # get other client address
    stub = None
    channel = None

    try:
        while True:
            other_client_name = input('Enter other client_name: ')
            if other_client_name == user.name:
                print()
                print('You cannot chat with yourself')
                print()
                continue

            other_client = name_server_pb2.ClientNameRequest(client_name=other_client_name)
            other_client_grpc = redis_stub.GetClientInfo(other_client)
            other_client_address = None
            if other_client_grpc.connectionInfo.client_address_and_port:
                other_client_address = other_client_grpc.connectionInfo.client_address_and_port

                channel = grpc.insecure_channel(other_client_address)
                stub = private_chat_pb2_grpc.PrivateChatServiceStub(channel)
                empty = private_chat_pb2.Empty()
                try:
                    response = stub.isClientActive(empty)
                    print(f"{'=' * 45}")
                    print(f"{'|':<2}{' Connected to ' + other_client_name + '. ':^41}{'|':>2}")
                    print(f"{'|':<2}{' Start chatting right now! ':^41}{'|':>2}")
                    print(f"{'=' * 45}")
                except grpc.RpcError as e:
                    print()
                    print('Error connecting to ' + other_client_name + ', he/she is offline right now.')
                    print()
                    channel.close()
                    continue
                break

            else:
                print()
                print('Client not found')
                print()
    except KeyboardInterrupt:
        return

    try:
        while True:

            input_message = input()
            message = private_chat_pb2.clientMessage(clientName=user.name, clientMessage=input_message)
            try:
                response = stub.sendMessage(message)
            except grpc.RpcError as e:
                print()
                print('Error sending message ' + other_client_name + ', he/she is offline right now.')
                print()
                break
            time.sleep(0.5)

    except KeyboardInterrupt:
        server.stop(0)
        channel.close()
        print()
        print('Exit privateChat with ' + other_client_name + '.')


def subscribeToGroupChat():
    pass


def discoverChat():
    pass


def accessInsultChannel():
    pass


# -----------------------------------------------------------------------------------------------------------------------
# Main - start code


# Connect to NameServer
redis_channel = grpc.insecure_channel('0.0.0.0:50051')
redis_stub = name_server_pb2_grpc.NameServerStub(redis_channel)

# log in
while True:
    self_name = input('Enter your name: ')
    self_client = name_server_pb2.ClientNameRequest(client_name=self_name)
    self_client_address = redis_stub.GetClientInfo(self_client)

    if self_client_address.connectionInfo.client_address_and_port:
        self_client_address = self_client_address.connectionInfo.client_address_and_port
        break
    else:
        print('Client not found')

# if login successfully, create a ChatClient instance
client = ChatClient(self_name, self_client_address)
option = None

# Main menu
try:
    while option != '5':
        printMenu()
        option = input('Enter option: ')
        print()
        if option == '1':
            privateChat(client)
        elif option == '2':
            print('Subscribe to group chat')
        elif option == '3':
            print('Discover chat')
        elif option == '4':
            print('Access insult channel')
        elif option == '5':
            break
        else:
            print('Invalid option')
except KeyboardInterrupt:
    print('Exiting...')
    exit()
