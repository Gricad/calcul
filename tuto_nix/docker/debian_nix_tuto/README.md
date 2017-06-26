Dockerfile for the NIX tutorial
===============================

Very basic image with dependencies for installing Nix.

Usage
-----
    docker build -t nix_tuto .
    docker run -it -u test nix_tuto
    # Start the tutorial
    # (the sudo password is 'test')
