import threading
import time
from concurrent import futures

import grpc
import pika
import yaml
import random

from pika.exceptions import ChannelClosedByBroker

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


def printHeader(string):
    print()
    print("╔" + "═" * 50 + "╗")
    print("║{:50}║".format(string))
    print("╚" + "═" * 50 + "╝")
    print()


def printMenu():
    print()
    print("╔" + "═" * 50 + "╗")
    print("║" + " " * 50 + "║")
    print("║{:^50}║".format(" ██████╗██╗  ██╗ █████╗ ████████╗ "))
    print("║{:^50}║".format("██╔════╝██║  ██║██╔══██╗╚══██╔══╝"))
    print("║{:^50}║".format("██║     ███████║███████║   ██║   "))
    print("║{:^50}║".format("██║     ██╔══██║██╔══██║   ██║   "))
    print("║{:^50}║".format("╚██████╗██║  ██║██║  ██║   ██║   "))
    print("║{:^50}║".format(" ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   "))
    print("║" + " " * 50 + "║")
    print("╠" + "═" * 50 + "╣")
    print("║{:50}║".format(" 1. Connect chat"))
    print("║{:50}║".format(" 2. Subscribe to group chat"))
    print("║{:50}║".format(" 3. Discover chat"))
    print("║{:50}║".format(" 4. Access insult channel"))
    print("║{:50}║".format(" 5. Exit"))
    print("╚" + "═" * 50 + "╝")
    print()


def printMenuGrupalChat():
    try:
        while True:
            print("=" * 45)
            print(f"{'|':<2}{' Group Chat Options ':^41}{'|':>2}")
            print("=" * 45)
            print(f"{'| 1. Persistent Group Chat':<44}{'|':>1}")
            print(f"{'| 2. Transient Group Chat':<44}{'|':>1}")
            print("=" * 45)

            choice = input("Select an option (1 or 2): ")

            if choice in ['1', '2']:
                return choice
            else:
                print("Invalid choice. Please select either 1 or 2.")
    except KeyboardInterrupt:
        return None


def privateChat(user: ChatClient):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    private_chat_pb2_grpc.add_PrivateChatServiceServicer_to_server(
        PrivateChatServicer(), server)

    server.add_insecure_port(user.connection)
    server.start()

    stub = None
    channel = None

    try:
        # Connect to the other client
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
            # Check if the client is active
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
        # Send messages
        while True:
            input_message = input()
            message = private_chat_pb2.clientMessage(clientName=user.name, clientMessage=input_message)
            try:
                response = stub.sendMessage(message)
            # If the other client is offline
            except grpc.RpcError as e:
                print()
                print('Error sending message ' + other_client_name + ', he/she is offline right now.')
                print()
                break
            time.sleep(0.5)

    except KeyboardInterrupt:
        # Return to main menu
        server.stop(0)
        channel.close()
        print()
        print('Exit privateChat with ' + other_client_name + '.')


def GroupChat(user: ChatClient):
    choice = printMenuGrupalChat()

    # persistent group chat
    if choice == '1':
        GroupChatP(user)
    else:
        # transient group chat
        if choice == '2':
            GroupChatT(user)
        else:
            return


def GroupChatT(user: ChatClient):
    try:
        # Connect to RabbitMQ
        connection_params = pika.ConnectionParameters('localhost')
        connection = pika.BlockingConnection(connection_params)
        channel = connection.channel()
        group_name = None
        try:
            while True:
                try:
                    group_name = input('Enter group name: ')
                    channel.exchange_declare(exchange=group_name, exchange_type='fanout', durable=False)
                    break
                except ChannelClosedByBroker:
                    print("There is a persistent group using this name, please try again with another group name")
                    channel = connection.channel()
                    continue
                except KeyboardInterrupt:
                    return
        except KeyboardInterrupt:
            return

        queue_name = user.name + '_' + group_name + '_queue'

        # Declare queue to each member of the group
        result = channel.queue_declare(queue=queue_name, exclusive=True)
        queue_name = result.method.queue

        # Associate each queue to the exchange
        channel.queue_bind(exchange=group_name, queue=queue_name)

        def callback(ch, method, properties, body):
            # Do not print messages twice sent by the same user
            if properties.headers['sender'] != user.name:
                print(body.decode())

        # Configure the consumer
        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        print("=" * 45)
        print(f"{'|':<2}{' Connected to group ' + group_name + ' ':^41}{'|':>2}")
        print(f"{'|':<2}{' Listening to messages right now ':^41}{'|':>2}")
        print(f"{'|':<2}{' Press Ctrl+C to send a message ':^41}{'|':>2}")
        print("=" * 45)

        try:
            while True:

                try:
                    # Receive messages
                    channel.start_consuming()
                except KeyboardInterrupt:
                    # Send messages
                    print()
                    message = input("[" + user.name + "] ")
                    message = '[' + user.name + '] ' + message
                    channel.basic_publish(exchange=group_name, routing_key='', body=message.encode(),
                                          properties=pika.BasicProperties(headers={'sender': user.name}))
                    continue

        except KeyboardInterrupt:
            # Return to main menu
            print()
            print('Exiting GroupChat...')
            connection.close()
            return

    except KeyboardInterrupt:
        return


def GroupChatP(user: ChatClient):
    try:
        # Connect to RabbitMQ
        connection_params = pika.ConnectionParameters('localhost')
        connection = pika.BlockingConnection(connection_params)
        channel = connection.channel()
        group_name = None
        try:
            while True:
                try:
                    group_name = input('Enter group name: ')
                    channel.exchange_declare(exchange=group_name, exchange_type='fanout', durable=True)
                    break
                except ChannelClosedByBroker:
                    print('There is a transient group using this name, please try again with another group name')
                    continue
                except KeyboardInterrupt:
                    return
        except KeyboardInterrupt:
            return

        queue_name = user.name + '_' + group_name + '_queue'

        # Declare queue to each member of the group
        result = channel.queue_declare(queue=queue_name, durable=True)
        queue_name = result.method.queue

        # Associate each queue to the exchange
        channel.queue_bind(exchange=group_name, queue=queue_name)

        def callback(ch, method, properties, body):
            # Do not print messages twice sent by the same user
            if properties.headers['sender'] != user.name:
                print(body.decode())

        # Configure the consumer
        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        print("=" * 45)
        print(f"{'|':<2}{' Connected to group ' + group_name + ' ':^41}{'|':>2}")
        print(f"{'|':<2}{' Listening to messages right now ':^41}{'|':>2}")
        print(f"{'|':<2}{' Press Ctrl+C to send a message ':^41}{'|':>2}")
        print("=" * 45)

        try:
            while True:
                try:
                    # Receive messages
                    channel.start_consuming()
                except KeyboardInterrupt:
                    # Send messages
                    print()
                    message = input("[" + user.name + "] ")
                    message = '[' + user.name + '] ' + message
                    channel.basic_publish(exchange=group_name, routing_key='', body=message.encode(),
                                          properties=pika.BasicProperties(
                                              headers={'sender': user.name},
                                              delivery_mode=2  # Make message persistent
                                          ))
                    continue
        except KeyboardInterrupt:
            # Return to main menu
            print()
            print('Exiting GroupChat...')
            connection.close()
            return

    except KeyboardInterrupt:
        return


def discoverChat():
    pass


def accessInsultChannel(user_client: ChatClient):
    # Connection RabbitMQ
    connection = None
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        # Declare queue
        channel.queue_declare(queue='insult_queue')

        def callback(ch, method, properties, body):
            print(f"{body.decode()}")

        # Configure consumer
        channel.basic_consume(queue='insult_queue', on_message_callback=callback, auto_ack=True)

        # ESend an insult
        def send_insult(insult):
            channel.basic_publish(exchange='',
                                  routing_key='insult_queue',
                                  body=insult)
            print(f"Sent: {insult}")

        while True:
            print("=" * 45)
            print(f"{'|':<2}{' Select an option:':^41}{'|':>2}")
            print(f"{'|':<2}{' 1. Send insult ':^41}{'|':>2}")
            print(f"{'|':<2}{' 2. Receive insult':^41}{'|':>2}")
            print("=" * 45)
            options = input('Enter option: ')

            if options == '1':
                # Send insult
                insult_string = input('Enter insult: ')
                insult_string = '[' + user_client.name + '] ' + insult_string
                send_insult(insult_string)
            elif options == '2':
                try:
                    # Receive insults
                    print()
                    print("=" * 60)
                    print('Receiving insults. Press Ctrl+C to stop receiving insults')
                    print("=" * 60)
                    channel.start_consuming()
                except KeyboardInterrupt:
                    print()
                    continue
            else:
                print('Invalid option')

        connection.close()
    except KeyboardInterrupt:
        # Return to main menu
        connection.close()
        return


# -----------------------------------------------------------------------------------------------------------------------
# Main - start code


# Connect to NameServer
redis_channel = grpc.insecure_channel('0.0.0.0:50051')
redis_stub = name_server_pb2_grpc.NameServerStub(redis_channel)

# log in
while True:
    printHeader(' LOG IN TO USE CHAT APPLICATION')
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
            printHeader(' PRIVATE CHAT')
            privateChat(client)
        elif option == '2':
            printHeader(' SUBSCRIBE TO GROUP CHAT')
            GroupChat(client)
        elif option == '3':
            print('Discover chat')
        elif option == '4':
            printHeader(' INSULT CHANNEL')
            accessInsultChannel(client)
        elif option == '5':
            break
        else:
            print('Invalid option')
except KeyboardInterrupt:
    print()
    print('Exiting...')
    exit()
