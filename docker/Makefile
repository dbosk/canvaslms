VERSION+=	latest

.PHONY: all
all: docker-image

.PHONY: publish
publish: docker-image
	for v in ${VERSION}; do docker push dbosk/canvaslms:$$v; done

.PHONY: docker-image
docker-image:
	docker pull python:3
	docker build --no-cache -t canvaslms .
	for v in ${VERSION}; do docker tag canvaslms dbosk/canvaslms:$$v; done

.PHONY: clean
clean:
	true

.PHONY: distclean
distclean:
	-docker image rm -f canvaslms dbosk/canvaslms
