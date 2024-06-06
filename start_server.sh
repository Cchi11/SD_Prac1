#!/bin/bash

# Function to check if Redis server is running
is_redis_running() {
    if redis-cli ping &> /dev/null; then
        return 0
    else
        return 1
    fi
}

# Start Redis server if not already running
if is_redis_running; then
    echo "Redis server is already running."
else
    echo "Starting Redis server..."
    redis-server &
    sleep 2  # Wait a moment to give Redis time to start
fi

# Start RabbitMQ docker container
echo "Starting RabbitMQ server..."
docker run --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13-management &

# Start the server
python server.py




