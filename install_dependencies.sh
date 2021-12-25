#!/bin/bash

# INSTALL JOERN
mkdir joern && cd joern # optional
curl -L "https://github.com/joernio/joern/releases/latest/download/joern-install.sh" -o joern-install.sh
chmod u+x joern-install.sh
./joern-install.sh --interactive

cd ..

# INSTALL CHEQUE
# Cheque requires GoLang to be built:
sudo add-apt-repository ppa:longsleep/golang-backports
sudo apt update
sudo apt install golang-go

# Build Cheque
git clone https://github.com/sonatype-nexus-community/cheque.git
cd cheque
sudo go build