build:
	docker-compose pull
	docker-compose build

stack-full-refresh:
	docker-compose build --no-cache --pull
	docker-compose up -d

help:
	./dockercmd.sh "--help"

dev-bash:
	docker-compose run --rm --entrypoint /bin/bash dev

drill-bash:
	docker exec -ti eaglealpha_drill_1 /bin/bash

create-s3-bucket:
	docker-compose run --rm dev create-s3-bucket

upload-files-to-s3:
	docker-compose run --rm dev load-file-to-s3

create-s3-storage-plugin:
	docker-compose run --rm dev create-s3-storage-plugin

query-drill:
	docker-compose run --rm dev query-drill

setup-drill:
	docker-compose run --rm dev setup-drill

fix-malformed-jl:
	docker-compose run --rm dev fix-malformed-jl