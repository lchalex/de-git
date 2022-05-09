docker build -t 5017_degit . 
docker run --rm -it -v ${PWD}:/workspace -w /workspace -e RPC_SERVER=http://192.168.8.2:7545 5017_degit bash