# Wanderlust


## Configuration

* Build docker images:

```bash
docker-compose -f consumers.yml build
docker-compose -f producers.yml build
```

* Update `KAFKA_ADVERTISED_LISTENERS` in `services.yml` with your computer IP:


## Running Demo

* Start services:

```bash
# Replace `up` with `down` for stopping & removing all services
docker-compose -f services.yml up
```

* Start producer:

```bash
docker-compose -f producers.yml up

```

* Start consumer:

```bash
docker-compose -f consumers.yml up

```