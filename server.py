import grpc
import yaml

import name_server_pb2
import name_server_pb2_grpc

import grpc
from concurrent import futures
import redis


class NameServerServicer(name_server_pb2_grpc.NameServerServicer):
    def __init__(self):
        # Conectar a Redis
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)

    def GetClientInfo(self, request, context):
        client_name = request.client_name

        # Obtain from Redis the client address and port
        client_redis = self.redis_client.get(client_name)

        if client_redis is None:
            client_ip_port = name_server_pb2.GetClientInfoResponse(
                errorInfo=name_server_pb2.ErrorInfo(error_message=1)
            )
            return client_ip_port
        else:
            client_ip_port = name_server_pb2.GetClientInfoResponse(
                connectionInfo=name_server_pb2.ClientInfo(
                    client_name=client_name,
                    client_address_and_port=self.redis_client.get(client_name)
                )
            )
            return client_ip_port

    def AddToNameServer(self, request, context):
        client_name = request.client_name
        client_address_and_port = request.client_address_and_port
        self.redis_client.set(client_name, client_address_and_port)

        return name_server_pb2.InfoFromNameServer(accepted=1)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    name_server_pb2_grpc.add_NameServerServicer_to_server(NameServerServicer(), server)
    server.add_insecure_port('0.0.0.0:50051')
    print("Starting server. Listening on port 50051.")
    server.start()
    # Connect to NameServer
    redis_channel = grpc.insecure_channel('0.0.0.0:50051')
    redis_stub = name_server_pb2_grpc.NameServerStub(redis_channel)

    # Leer el archivo YAML
    with open('clients.yaml', 'r') as file:
        data = yaml.safe_load(file)

    for client in data['clients']:
        name = client['name']
        client_ip_address = client['ip'] + ':' + str(client['port'])
        addClient = name_server_pb2.AddClientRequest(client_name=name, client_address_and_port=client_ip_address)
        redis_stub.AddToNameServer(addClient)

    # close connection
    redis_channel.close()

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("Server stopped by user.")
        server.stop(0)
        return


if __name__ == '__main__':
    serve()