#!/usr/bin/env bash

SCRIPT_DIR=$(dirname $(realpath $0))

mkdir -p $SCRIPT_DIR/.vscode-server

docker run --rm -it --name web-server \
	-p 5000:5000 \
	$1 
	# --volume $SCRIPT_DIR/workspace:/home/aidata/workspace \
	# --workdir /home/aidata/workspace \
	# --volume $SCRIPT_DIR/.vscode-server:/home/aidata/.vscode-server \
	# --gpus all --shm-size 2g \