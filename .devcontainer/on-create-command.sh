#!/bin/bash

set -euo pipefail

export DEBIAN_FRONTEND=noninteractive

sudo apt-get update
sudo apt-get install -y curl python3 python3-pip shellcheck black

curl -sSL https://install.python-poetry.org | python3 -
