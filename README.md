# cld.sh api
runs on pypy v7.3.5

to build
```sh
docker build -t "cld.sh-api" .
docker run -d --net="host" --name="api.cld.sh" "cld.sh-api/latest"
```