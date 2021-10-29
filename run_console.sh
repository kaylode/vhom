#!/usr/bin/env bash

SCRIPT_DIR=$(dirname $(realpath $0))
USERNAME=guest

mkdir -p $SCRIPT_DIR/.vscode-server

docker run --rm -it --name web-server \
	-p 5000:5000 \
	--volume $SCRIPT_DIR/src:/home/${USERNAME}/src \
	--volume $SCRIPT_DIR/data:/home/${USERNAME}/data \
	--workdir /home/${USERNAME}/ \
	$1 