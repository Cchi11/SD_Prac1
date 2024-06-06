# SD_P1: Online Chat Application

## Català
Aquest és un projecte senzill d'una aplicació de xat que utilitza Python, gRPC i RabbitMQ. L'aplicació permet a diversos clients comunicar-se entre ells mitjançant xats privats, subscriure's a xats de grup, descobrir altres clients disponibles i accedir a un canal d'insults.

### Pasos per executar l'aplicació

1. Clona el repositori a la teva màquina local.
2. Instal·la les dependències necessàries executant la comanda `pip install -r requirements.txt`.
3. Executa el script 'start_server.sh' per iniciar el servidor de redis, rabbitmq i el servidor de noms.
4. Executat tants clients com vulguis per terminal amb l'script 'start_client.sh'.

### Funcionament

L'aplicació ofereix les següents funcionalitats:

1. **Xat Privat**: Permet als usuaris connectar-se i intercanviar missatges de forma privada amb altres clients mitjançant gRPC.
2. **Subscripció a Xat de Grup**: Els usuaris poden subscriure's a xats de grup, ja siguin persistents o transients, mitjançant RabbitMQ.
3. **Descoberta de Xat**: Els usuaris poden publicar i respondre a esdeveniments de descoberta per connectar-se amb altres clients disponibles.
4. **Canal d'Insults**: S'ofereix un canal d'insults on els usuaris poden enviar i rebre insults.

## Español

Este es un proyecto simple de una aplicación de chat que utiliza Python, gRPC y RabbitMQ. La aplicación permite a varios clientes comunicarse entre sí mediante chats privados, suscribirse a chats grupales, descubrir otros clientes disponibles y acceder a un canal de insultos.

### Pasos para ejecutar la aplicación

1. Clona el repositorio en tu máquina local.
2. Instala las dependencias necesarias ejecutando el comando `pip install -r requirements.txt`.
3. Ejecuta el script 'start_server.sh' para iniciar el servidor de redis, RabbitMQ y el servidor de nombres.
4. Ejecuta tantos clientes como desees desde la terminal con el script 'start_client.sh'.

### Funcionamiento

La aplicación ofrece las siguientes funcionalidades:

1. **Chat Privado**: Permite a los usuarios conectarse e intercambiar mensajes de forma privada con otros clientes mediante gRPC.
2. **Suscripción a Chat Grupal**: Los usuarios pueden suscribirse a chats grupales, ya sean persistentes o transitorios, mediante RabbitMQ.
3. **Descubrimiento de Chat**: Los usuarios pueden publicar y responder a eventos de descubrimiento para conectarse con otros clientes disponibles.
4. **Canal de Insultos**: Se ofrece un canal de insultos donde los usuarios pueden enviar y recibir insultos.

## English

This is a simple project of a chat application that uses Python, gRPC, and RabbitMQ. The application allows multiple clients to communicate with each other through private chats, subscribe to group chats, discover other available clients, and access an insult channel.

### Steps to run the application

1. Clone the repository to your local machine.
2. Install the necessary dependencies by running the command `pip install -r requirements.txt`.
3. Execute the 'start_server.sh' script to start the redis server, RabbitMQ, and the name server.
4. Run as many clients as you want from the terminal using the 'start_client.sh' script.

### Functionality

The application offers the following features:

1. **Private Chat**: Allows users to connect and exchange messages privately with other clients using gRPC.
2. **Subscription to Group Chat**: Users can subscribe to group chats, whether persistent or transient, using RabbitMQ.
3. **Chat Discovery**: Users can publish and respond to discovery events to connect with other available clients.
4. **Insult Channel**: An insult channel is provided where users can send and receive insults.
