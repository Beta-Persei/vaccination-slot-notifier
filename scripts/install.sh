#!/bin/sh

apt-get update
apt-get upgrade -y
apt-get install -y  python3 python3-pip postgresql-client -qq --no-install-recommends
