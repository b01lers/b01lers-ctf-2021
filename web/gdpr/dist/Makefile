all: build
run: start exec
debug: start shell

PORT_PREFIX = 10

# Also the challenge number
PORT_POSTFIX = 04
NAME = gdpr
FNAME = $(PORT_POSTFIX)-$(NAME)

build:
	docker build -t $(FNAME) .

start:
	docker run --rm -itd --name $(FNAME) -p $(PORT_PREFIX)$(PORT_POSTFIX):3000 $(FNAME)

exec:
	docker exec -itd $(FNAME) node index.js

shell:
	docker exec -it $(FNAME) /bin/sh

stop:
	docker kill $(FNAME)
