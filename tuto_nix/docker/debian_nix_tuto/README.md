Dockerfile for the NIX tutorial
===============================

Very basic image with dependencies for installing Nix.

Usage
-----
    mkdir nix_tuto
    cd nix_tuto
    wget https://raw.githubusercontent.com/Gricad/calcul/master/tuto_nix/docker/debian_nix_tuto/Dockerfile
    docker build -t nix_tuto .
    docker run -it -u test nix_tuto
    # Start the tutorial
    # (the sudo password is 'test')
