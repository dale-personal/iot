docker-compose up -d
docker exec -d openhab /bin/chmod o+rw /dev/ttyACM0
docker exec -d openhab adduser openhab tty
