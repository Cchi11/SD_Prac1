import grpc
import name_server_pb2
import name_server_pb2_grpc

import grpc
from concurrent import futures
import redis


class NameServerServicer(name_server_pb2_grpc.NameServerServicer):
    def __init__(self):
        # Conectar a Redis
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)

    def getClientInfo(self, request, context):
        client_name = request.client_name

        # Obtener información de conexión desde Redis
        client_address_and_port = self.redis_client.get(client_name)
        client_ip_port = name_server_pb2.getConnectionInfo(client_name=client_name, client_address_and_port=client_address_and_port)
        return client_ip_port

    def addToNameServer(self, request, context):
        client_name = request.client_name
        client_address_and_port = request.client_address_and_port
        # Añadir información de cliente a Redis
        self.redis_client.set(client_name, client_address_and_port)
        return name_server_pb2.infoFromNameServer(accepted=1)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    name_server_pb2_grpc.add_NameServerServicer_to_server(NameServerServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("Starting server. Listening on port 50051.")
    server.start()
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("Server stopped by user.")
        server.stop(0)


if __name__ == '__main__':
    serve()
