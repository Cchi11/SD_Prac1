import grpc
import time
import private_chat_pb2
import private_chat_pb2_grpc
from concurrent import futures


# create a class to define the server functions, derived from
# private_chat_pb2_grpc.PrivateChatServiceServicer
class PrivateChatServicer(private_chat_pb2_grpc.PrivateChatServiceServicer):

    def sendMessage(self, request, context):
        print(request.clientName + ': ' + request.clientMessage)
        response = private_chat_pb2.Empty()
        return response

    def isClientActive(self, request, context):
        response = private_chat_pb2.Empty()
        return response
