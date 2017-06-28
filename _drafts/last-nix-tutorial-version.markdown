---
layout: post
title:  "Nix tutorial"
author: calcul-team
categories: [Nix,Tuto]
---

table of content
* TOC
{:toc}



# Introduction

Introduction of this tutorial is currently in French, as a  [PDF presentation]({{ site.url }}/tuto_nix/media/NixIntroJDEV2017.pdf).


# Using the Nix packages manager
## Prerequisites
  - Linux (64bits) / Mac OS
  - Be a sudoer or have root access.
  - Bash, curl installed

If you need, you can find a Dockerfile to create a Debian basic image with those prerequisites:  
[Docker image for this tutorial]({{site.url }}/tuto_nix/docker/debian_nix_tuto).

## Install Nix (single user mode)
**Source** : http://nixos.org/nix/manual/#chap-installation

From a basic environment you just have to run the following command :
```bash
bash <(curl https://nixos.org/nix/install)
```
**Optionnal** : If you don't have sudo installed or if you're not a sudoer, you have to execute this command as root :

`mkdir -m 0755 /nix && chown <your_login> /nix`

From this point, you should see something like this :

```bash
bash <(curl https://nixos.org/nix/install)
[...]
performing a single-user installation of Nix...
copying Nix to /nix/store...............................
initialising Nix database...
creating /home/<your_login>/.nix-profile
installing ‘nix-1.11.9’
building path(s) ‘/nix/store/7dv1lghxz40rbvv9ffg7fq2as972a4r7-user-environment’
created 6 symlinks in user environment
downloading Nix expressions from ‘https://d3g5gsiof5omrk.cloudfront.net/nixpkgs/nixpkgs-17.09pre106045.7369fd0b51/nixexprs.tar.xz’...
downloading ‘https://d3g5gsiof5omrk.cloudfront.net/nixpkgs/nixpkgs-17.09pre106045.7369fd0b51/nixexprs.tar.xz’... [6977/8550 KiB, 3474.3 KiB/s]
unpacking channels...
created 2 symlinks in user environment

Installation finished!  To ensure that the necessary environment
variables are set, either log in again, or type

  . /home/<your_login>/.nix-profile/etc/profile.d/nix.sh

in your shell.
```


The Nix package manager is now installed on your system and ready to be used.

The installation process only populates the directory `/nix` and creates a symbolic link `~/.nix-profile` in your home directory.

## Uninstall Nix
You can easily uninstall Nix from your system typing :
```bash
sudo rm -rf /nix
rm -rf ~/.nix-*
```

## Activate your Nix environments

The install script tels you to  source the following script to use your new Nix environment : ```~/.nix-profile/etc/profile.d/nix.sh```
This creates a set of variables and configure the PATH variable to point to your default nix profile.

But by default, a single user Nix installation does not set up the "profiles" feature. As we want to use it, we are going to set up a copy of the provided environment file. Actually, we just have to add the path of the default profile that contains the nix package:

```bash
cp /nix/var/nix/profiles/default/etc/profile.d/nix.sh ~/nix.sh
echo "export PATH=/nix/var/nix/profiles/default/bin:\$PATH" >> ~/nix.sh
# If you are under MACOS, also add:
echo "export NIX_SSL_CERT_FILE=/nix/var/nix/profiles/default/etc/ssl/certs/ca-bundle.crt" >> ~/nix.sh
```

Then we can load the Nix environment:
```bash
source ~/nix.sh
```

You can check changes typing :

```bash
env | grep nix

NIX_PATH=nixpkgs=/home/<your_login>/.nix-defexpr/channels/nixpkgs
PATH=/nix/var/nix/profiles/default/bin:/home/<your_login>/.nix-profile/bin:/home/<your_login>/.nix-profile/sbin:/usr/local/bin:/usr/bin:/bin:
```

## Working with profiles: user environment

The Nix package manager provides a "profiles" feature to help users to manage as many environments as needed.
Users can switch between profiles and navigate through the history of each profile.

What is my current profile ?
Nix automaticaly creates your first "default" profile: it's a symbolic link pointing to **/nix/var/nix/profiles/default**.
```bash
ls -l ~/.nix-profile
lrwxr-xr-x  1 <your_login>  staff  29 15 nov  2016 .nix-profile -> /nix/var/nix/profiles/default
```

Here is how to create a new profile and switch to it (please, replace ```<your_login>``` by your real login string):
```bash
nix-env --switch-profile /nix/var/nix/profiles/per-user/<your_login>/tuto-jdev
```

Note: *Under NiXOS or on some properly installed multi-user sites, the environment variable* $NIX_USER_PROFILE_DIR *might be correctly set and may be used to easily find the right path* ```/nix/var/nix/profiles/per-user/<your_login>```.

With this command, Nix creates the "tuto-jdev" profile if it doesn't exist, and switch to it.
You can check the change :
```bash
ls -l ~/.nix-profile
lrwxr-xr-x  1 <your_login>  staff  29 15 nov  2016 .nix-profile -> /nix/var/nix/profiles/per-user/<your_login>/tuto-jdev
```
Note: *For the moment, this link may point to a non-existent directory as you don't have installed any package yet. The profile directory will be created at the first installation of a package, you'll see that in the next few lines of this tutorial!*

You can now work with differents profiles and switch between them.

You can have as many profiles as you want. That way, you can have many environments. Once you'll be familiar to Nix, you'll see that you'll switch to a new profile each time you're starting something new! And this will miss you on other systems ;-)

# Nix basics

At this point it's important to understand the underlying mechanisms of nix for libraries installation and management.
Nix is made to allow different users to have different configurations and to switch between them but
with one and only one place where everything is installed : /nix.
One of the main benefits of using nix is that any user (understand non-root) is allowed to "install"
packages in /nix. But this package will be available in the user environment through some trees of symlink
between /nix and ~/.nix-profile.

Moreover, thanks to profile, a single user can easyly switch between different configurations.

Let's start using Nix with our new "tuto-jdev" profile. Make sure you're using the right profile :
```bash
nix-env --switch-profile /nix/var/nix/profiles/per-user/<your_login>/tuto-jdev
```

From that point, every package you install will be available under this profile.
The operation above just update the link between ~/.nix-profile and some directory in /nix
To check this connection, try:
```bash
ls -altr ~/.nix-profile
```

## Install Nix packages
To install a package we use the ```nix-env -i``` command. For example:
```bash
~$ nix-env -i hello
installing ‘hello-2.10’
~$ hello
Hello, world!
~$ which hello
/home/<your_login>/.nix-profile/bin/hello
```

Let us assume that you need some specific application, say for instance **boost**.
First of all, you need to check if this package is available, if so which is the version number and so on:

The complete list of all available packages can be obtained thanks to the command
```bash
nix-env -qaP

... **very long list**
```
Note: *qaP : q as query, a as available and P as preserve-installed*

combined with grep to target a specific program or library:
```bash
nix-env -qaP | grep boost
nixpkgs.boost155                                                  boost-1.55.0
nixpkgs.boost159                                                  boost-1.59.0
nixpkgs.boost160                                                  boost-1.60.0
nixpkgs.python27Packages.boost                                    boost-1.62.0
nixpkgs.python36Packages.boost                                    boost-1.62.0
nixpkgs.boost                                                     boost-1.62.0
nixpkgs.boost163                                                  boost-1.63.0
nixpkgs.boost-build                                               boost-build-2.0-m12
nixpkgs.boost_process                                             boost-process-0.5
nixpkgs.pianobooster                                              pianobooster-0.6.4b
nixpkgs.python27Packages.xgboost                                  python2.7-xgboost-0.60
nixpkgs.python36Packages.xgboost                                  python3.6-xgboost-0.60
nixpkgs.xgboost                                                   xgboost-0.60
```


Ok, now you're able to choose the boost version that fits you. Notice on the right column, the complete name of the package and on the left column, the attributes of the package (channel and components name between dots). Also notice that a same package may be available with different attributes (for example here boost-1.62.0 is available with python27 or python36 bindings).

Once you've find the package name you want to install, you can do it with the following option (by name) :
```bash
nix-env -i boost-1.60.0
```

Or (by attributes) :
```bash
nix-env -iA nixpkgs.boost160
```

Check the consequences of these installations in ~/.nix-profile:

```bash
ls -ld ~/.nix-profile/lib
  .nix-profile/lib -> /nix/store/h4c1bmm3qk0vifhs3xd5p6c8apciv1gq-boost-1.60.0/lib

```

Let's install another library, to populate a bit more our profile:

```bash
nix-env -iA nixpkgs.openblas
```

Now, check again your profile:

```bash
ls -ld ~/.nix-profile/lib
  .nix-profile/lib
```

The *lib* directory was actualy a link to the same directory into the *boost* package, as we had only one package installed with a *lib* path. But now that we have another package having a *lib* directory too, it is now a real directory, and nix created a bunch of symbolic links inside:

```bash
ls -altr ~/.nix-profile/lib/libboost_atomic.so
  .nix-profile/lib/libboost_atomic.so -> /nix/store/h4c1bmm3qk0vifhs3xd5p6c8apciv1gq-boost-1.60.0/lib/libboost_atomic.so
ls -altr ~/.nix-profile/lib/libopenblas.so
  .nix-profile/lib/libopenblas.so -> /nix/store/jxm1c9ks0bkfzkv40jwgwv4yxg0paxkq-openblas-0.2.19/lib/libopenblas.so
```

Take a look at the dependencies :

```bash
ldd ~/.nix-profile/lib/libboost_atomic.so
        linux-vdso.so.1 (0x00007fff2c9cd000)
        librt.so.1 => /nix/store/f111ij1fc83965m48bf2zqgiaq88fqv5-glibc-2.25/lib/librt.so.1 (0x00007f2fe05b7000)
        libstdc++.so.6 => /nix/store/xfrkm34sk0a13ha9bpki61l2k5g1v8dh-gcc-5.4.0-lib/lib/libstdc++.so.6 (0x00007f2fe023f000)
        libm.so.6 => /nix/store/f111ij1fc83965m48bf2zqgiaq88fqv5-glibc-2.25/lib/libm.so.6 (0x00007f2fdff2c000)
        libgcc_s.so.1 => /nix/store/f111ij1fc83965m48bf2zqgiaq88fqv5-glibc-2.25/lib/libgcc_s.so.1 (0x00007f2fdfd16000)
        libpthread.so.0 => /nix/store/f111ij1fc83965m48bf2zqgiaq88fqv5-glibc-2.25/lib/libpthread.so.0 (0x00007f2fdfaf6000)
        libc.so.6 => /nix/store/f111ij1fc83965m48bf2zqgiaq88fqv5-glibc-2.25/lib/libc.so.6 (0x00007f2fdf757000)
        /lib64/ld-linux-x86-64.so.2 (0x0000560272cb0000)

```

* libraries for *boost*, *blas*, and the *hello* binary are now available in your local (profile) environment
* this environment (.nix-profile) contains only symbolic links
* everything has been installed in /nix

## List installed packages
To list installed packages in your current profile type :
```bash
nix-env -q
```

## Profile rollback and generations

Each time you do a Nix operation in your profile, it creates a new generation of it. You can switch to every generations of a given profile.

You can undo a **nix-env** command with :
```bash
~$ nix-env -q
boost-1.60.0
hello-2.10
openblas-0.2.19
~$ nix-env --rollback
switching from generation 3 to 2
~$ nix-env -q
boost-1.60.0
hello-2.10
```

As you can see, the last package we installed is no more here.


To view the entire profile history (called "links generations") :
```bash
nix-env --list-generations
```

You can directly return to a specific generation with its Id :
```bash
$nix-env --switch-generation 3
```

## Remove packages

To remove a package from your Nix profile, just type :
```bash
nix-env -e the_package_you-re_searching_for
```

## Update packages

The following command will update the named package and all its dependencies :
```bash
nix-env -uA the_package_you-re_searching_for
```
And if the new version of the package  does not work, you can allways do a "--rollback"!


## Nix easier with Nox
Now we know the basics Nix commands, it could be interesting to install Nox. Nox is a Nix package that helps you to search and install Nix packages.

Let's try it :
```bash
nix-env -i nox
```

Nox provide a command line interface to search and install packages.
For instance, to install the fftw package with nox, you just have to type :
```bash
nox fftw
```
Nox lists the matching packages list. To install a specific version you just have to enter the number of the package in this list.

![Nox search and install]({{ site.url }}/tuto_nix/media/nox_install.png)


# Development environments

## your first nix expression: a basic ''hello'' package

This first example is an introduction to the development of nix packages.

A package is  built from a nix expression. Nix expressions describe the actions to build packages. (Searching the sources, compiling, installing).
  
A nix expression of ''hello'' package:

```
{ pkgs ? import <nixpkgs> {} }:
with pkgs;

let
  inherit stdenv fetchurl perl;
  version = "2.1.1";
in
{
    hello = stdenv.mkDerivation rec {
    name = "hello-${version}";
    buildInputs = [ perl ];
    src = fetchurl {
      url = "ftp://ftp.nluug.nl/pub/gnu/hello/${name}.tar.gz";
      sha256 = "c510e3ad0200517e3a14534e494b37dc0770efd733fc35ce2f445dd49c96a7d5";
    };
  };
}
```


The function "stdenv.mkDerivation" use a nix block as input to build a "derivation" of the "hello" package, by executing for you the standard building operations (configure, make, make install).
Some sets of key/value pairs, called attributes, are passed as environment variables to the build script of "mkDerivation" function. In the above nix expression, (version/2.1.1) is an example of such key/value pair.

The building process of "hello" package needs some tools : a standard development environment (stdenv), a function to download the source code (fetchurl).

### What is a derivation:
A derivation consists of a build script, a set of environment variables and a set of dependencies (source files or other derivations). The Nix language is used to describe such derivations.

Create a test directory and put the nix expression in a hello.nix file:

```
$ mkdir test
$ cd test
$ vi hello.nix
```

Then build the program:

```
$ nix-build hello.nix
```

A new directory ''result'' has been created.

```
$ ls -al result/bin/
total 16
dr-xr-xr-x 2 tuto tuto    19 janv.  1  1970 .
dr-xr-xr-x 4 tuto tuto    30 janv.  1  1970 ..
-r-xr-xr-x 1 tuto tuto 13552 janv.  1  1970 hello

$ ./result/bin/hello
Bonjour, le monde!
```

Now install the hello version 2.1.1 in your environment:
```
$ nix-env -f . -i hello 
installing ‘hello-2.1.1’
building path(s) ‘/nix/store/dqv9d96xmimb7xq4wj1jm3j7w4i9ik49-user-environment’
created 500 symlinks in user environment

$ hello --version
hello - GNU hello 2.1.1

```

Your first nix expression usage was successfull and it's time now to learn how to develop packages for the Nix community.

As you already know, nix expressions describe how to build packages from source,  they are collected in the nixpkgs repository.

The Nix Packages collection (Nixpkgs) is a set of thousands of packages for the Nix package manager, 

## How to add a package to nixpkgs :

### First step : get a local copy of nixpkgs tree

Checkout the Nixpkgs source tree:

```bash
$ git clone git://github.com/NixOS/nixpkgs.git

Initialized empty Git repository in /home/rochf/nixpkgs/.git/
```


Then, go to nixpkgs directory :

```bash
$ cd nixpkgs
```

### Second step : find a good place for your package and write a nix expression for your package under it

You can have a look at the existing Nix expressions in the pkgs/ tree to see how it's done.

If your package is a library, you will place it under :
pkgs/development/libraries

While a monitoring service will be place under :
pkgs/servers/monitoring

For example, if you are developping a package for a "mylib" library, create a new directory for your package:

```bash
mkdir pkgs/development/libraries/mylib
```

Then create the nix expression of your library package, it is usually called default.nix :

```bash
$ emacs pkgs/development/libraries/mylib/default.nix
```

You can copy/paste the default.nix file of another library and modify it to adapt to your own library.

The list of all packages is defined in:
`~/nixpkgs/pkgs/top-level/all-packages.nix`

If you add a new package, add a line for it.
You can use as model one of the other packages ''callPackage'' lines.
Ths line is a call to the function defined in your default.nix  
(See the "oned" example below).

The list of package maintainers is defined in :
`~/nixpkgs/lib/maintainers.nix`

A listing of licenses versions is available in :
`~/nixpkgs/lib/licenses.nix`

The [Nixpkgs Contributors Guide](https://nixos.org/releases/nixpkgs/nixpkgs-17.03pre91272.7e273d9/manual/) can help you.


#### Example of "oned" package derivation
Oned is a program which solve the Poisson equation using Jacobi method.

The code is available at "https://www.pdc.kth.se/education/tutorials/mpi/hybrid-lab/oned.c"  

A good place for nix expression of the "oned" package, seems to be : `pkgs/application/science/physics`

```bash
$ mkdir pkgs/applications/science/physics/oned
$ emacs pkgs/applications/science/physics/oned/default.nix
```

you can use "nix-prefetch-url" command (or similar "nix-prefetch-git" command) to get the SHA-256 hash of source distributions.

```bash
$ nix-prefetch-url https://www.pdc.kth.se/education/tutorials/mpi/hybrid-lab/oned.c
downloading ‘https://www.pdc.kth.se/education/tutorials/mpi/hybrid-lab/oned.c’... [0/0 KiB, 0.0 KiB/s]
path is ‘/nix/store/iw1xyii9wqb1ly5w95ni7rlwsv4q2pp5-oned.c’
1585yzy1gkg3bxfg19mh3ag1x7yik2h3lg5kz705d3jk9dhjg03b

```

*1585yzy1gkg3bxfg19mh3ag1x7yik2h3lg5kz705d3jk9dhjg03b*

Or, in case you have already downloaded the source code, use `sha256sum`" command to specify the sha256 record

Ex:

```bash
sha256sum oned.c
```

`buildInputs` defines a set of Nix packages dependencies for package build.

`propagatebuildInputs` defines runtime dependencies.

`buildInputs` and `propagatebuildInputs` are `Meta attributes` ; Meta attributes contain informations about the package. You can choose the necessary ones (the list of available meta-attributes is well [specified](http://nixos.org/nixpkgs/manual/#chap-meta).

Add your maintainer name with your email, respecting the alphabetical order :

```bash
emacs ~/nixpkgs/lib/maintainers.nix
```

Declare the package in the list of packages :

```bash
emacs ~/nixpkgs/pkgs/top-level/all-packages.nix
```

Add the following line (in the SCIENCE zone, and respecting the alphabetical order) :

`oned = callPackage ../applications/science/physics/oned  { };`


A nix expression for "oned":
```
{ stdenv, fetchurl, openmpi }:

stdenv.mkDerivation rec {
  name = "oned";
  src = fetchurl {
     url = "https://www.pdc.kth.se/education/tutorials/mpi/hybrid-lab/oned.c";
     sha256 = "1585yzy1gkg3bxfg19mh3ag1x7yik2h3lg5kz705d3jk9dhjg03b";
  };

  builder = builtins.toFile "builder.sh"
  "
  source $stdenv/setup
  mpicc -w -o oned.exe $src
  mkdir $out
  mkdir $out/bin
  cp oned.exe $out/bin
  ";

  buildInputs = [ openmpi ];

  meta = {
    description = "JDEV 2017 Nix tutoriel";
    license     = stdenv.lib.licenses.gpl2;
    platforms   = stdenv.lib.platforms.unix;
  };
}
```
In this case, you need to provide your own build script into a "builder" block, because configure and Makefile are not provided. 
The builder starts with "source $stdenv/setup" to setup the environment and process the buidInputs.
The $out variable is the location of the package under Nix store.

## Another derivation for oned :

Here, the sources provide a standard building process (configure, make, make install).
you don't have to write any builder in your nix expression, a generic builder, included in the standard environment (stdenv) do it for you:


```bash
cat  ~/nixpkgs/pkgs/applications/science/physics/oned/default.nix

{ stdenv, fetchgit, openmpi }:

stdenv.mkDerivation {
  name = "oned";

  src = fetchgit {
     url = "https://github.com/pbeys/tuto.git";
     rev = "0628826361cecebe8767307e417077b5ac279381";
     sha256 = "1zw0d0jv98bxk9zhkp22f478hc1c3m8dij329lw014283anyq9p3";
     fetchSubmodules = true;
  };

  buildInputs = [ openmpi ];


  meta = {
    description = "JDEV Nix tutoriel";
    license     = stdenv.lib.licenses.gpl2;
    platforms   = stdenv.lib.platforms.unix;
  };
}
```

### Third step: Building and installing the Package


The build process is started with the nix-build command:
```
$ nix-build -A oned
```

The nix-build command uses the attribute path ''oned'' to find the derivation and build the package.
The "-A attrPath" nix-env option select an attribute from the top-level Nix expression being evaluated.

You can check that all the dynamically loaded libraries are inside the /nix/store directory:

```
$ ldd /nix/store/<hash-code>-oned/bin/oned.exe
```

Test the executable :

```
$ oned.exe
```

*bash: oned.exe : command not found*

The oned program is not available. Your environment path is not yet ready, you have to "install" the package.

*installing ‘oned’*


```
$ nix-env -f . -iA oned
```

<em>building path(s) ‘/nix/store/66rh542l3hnwscgvd39n784qamympv8p-user-environment’</em>

<em>created 67 symlinks in user environment</em>


Now we can test the oned program:

```
$ oned.exe 200
```

Then a MPI run :
We need a mpi environment to be installed:

```
$ nix-env -i openmpi

$ mpirun -np 2 oned.exe 200
```

#### Example of hypre Package : Adding the hypre library package to nixpkgs ; creation of a derivation.  

hypre web page : https://computation.llnl.gov/projects/hypre-scalable-linear-solvers-multigrid-methods

Get the source distribution hash :

```
$ nix-prefetch-url https://computation.llnl.gov/projects/hypre-scalable-linear-solvers-multigrid-methods/download/hypre-2.11.2.tar.gz`

downloading ‘https://computation.llnl.gov/projects/hypre-scalable-linear-solvers-multigrid-methods/download/hypre-2.11.2.tar.gz’..

path is ‘/nix/store/m2xv5bsy7kp8916pd6j5irn8sn828w5s-hypre-2.11.2.tar.gz’

17i6zgywcmgbmr7zxgc7shzqramg64a8kwswpdqkyn8ichic3di5
```

Fill in all-packages.nix file :

```
$  grep -i 'hypre' pkgs/top-level/all-packages.nix`

hypre = callPackage ../development/libraries/hypre { };
```

Here is a derivation to build hypre package :

```
$ cat pkgs/development/libraries/hypre/default.nix


{ stdenv, fetchurl, gfortran, openmpi }:

stdenv.mkDerivation rec {
  version = "2.11.2";
  name = "hypre-${version}";

  src = fetchurl {
    url = "https://computation.llnl.gov/projects/hypre-scalable-linear-solvers-multigrid-methods/download/${name}.tar.gz";
    sha256 = "17i6zgywcmgbmr7zxgc7shzqramg64a8kwswpdqkyn8ichic3di5";
  };

  builder = builtins.toFile "builder.sh" "
    source $stdenv/setup;
    tar -zxvf $src;
    cd $name/src;
    ./configure --prefix=$out && make && make install && make test
  ";

  buildInputs = [ gfortran ];

  doCheck = true;

  enableParallelBuilding = true;

  meta = {
    description = "HYPRE: Scalable Linear Solvers and Multigrid Methods";
    homepage = http://https://computation.llnl.gov/projects/hypre-scalable-linear-solvers-multigrid-methods;
    license = stdenv.lib.licenses.gpl2Plus;
    maintainers = [ stdenv.lib.maintainers.tuto ];
    platforms = stdenv.lib.platforms.all;
  };
}
```

```
$ nix-build -A hypre
```

We have introduced a bug in this nix expression. See [Annexe: Debug](http://...#Debug) to help you correcting this bug.


We can observe that ''make test'' operates under /tmp

```
Making test drivers ...
make[1]: Entering directory '/tmp/nix-build-hypre-2.11.2.drv-0/hypre-2.11.2/src/test'
rm -f *.o
rm -rf pchdir tca.map *inslog*
make[1]: Leaving directory '/tmp/nix-build-hypre-2.11.2.drv-0/hypre-2.11.2/src/test'
make[1]: Entering directory '/tmp/nix-build-hypre-2.11.2.drv-0/hypre-2.11.2/src/test'
gcc -O2 -DHAVE_CONFIG_H -I. -I./.. -I/tmp/nix-build-hypre-2.11.2.drv-0/hypre-2.11.2/src/hypre/include   -DHYPRE_TIMING -DHYPRE_FORTRAN -c ij.c
In file included from ij.c:24:0:
...
-o zboxloop zboxloop.o -L/tmp/nix-build-hypre-2.11.2.drv-0/hypre-2.11.2/src/hypre/lib -lHYPRE  -lmpi        -lmpi -lstdc++ -lm
make[1]: Leaving directory '/tmp/nix-build-hypre-2.11.2.drv-0/hypre-2.11.2/src/test'
/nix/store/r71qdif3gdvpb7rszb6qllb0x9isgawi-hypre-2.11.2
```

The test directory is not persistent :

```
$ ls /tmp/nix-build-hypre-2.11.2.drv-0/hypre-2.11.2/src/test

File not found:  '/tmp/nix-build-hypre-2.11.2.drv-0/hypre-2.11.2/src/test'
```

```
$ ls -al /nix/store/cmr0hkvq40b29gy5ppsylksg0yk99ypc-hypre-2.11.2/lib/`

-r--r--r-- 1 tuto tuto 18477350 janv.  1  1970 libHYPRE.a
```

Test building shared libraries with openblas and liblapack:

Now, we place the builder in a file, in the same directory that the nix expression.

```
$ cat pkgs/development/libraries/hypre/builder.sh`

  source $stdenv/setup
  tar -zxvf $src
  cd $name/src
  ./configure --prefix=$out --enable-shared --enable-fortran CXX=mpicxx --with-MPI --with-MPI-include='${openmpi}/include' --with-MPI-lib-dirs='${openmpi}/lib' --with-MPI-libs='mpi' --with-blas-lib-dirs='${openblas}/lib' --with-blas-libs='openblas' --with-lapack-lib='-llapack'
  make
  make install
  make test
```

The nix expression is now:
```
$ cat pkgs/development/libraries/hypre/default.nix`

{ stdenv, fetchurl, gfortran, openmpi, openblas, liblapack }:

stdenv.mkDerivation rec {
  version = "2.11.2";
  name = "hypre-${version}";

  src = fetchurl {
    url = "https://computation.llnl.gov/projects/hypre-scalable-linear-solvers-multigrid-methods/download/${name}.tar.gz";
    sha256 = "17i6zgywcmgbmr7zxgc7shzqramg64a8kwswpdqkyn8ichic3di5";
  };

  builder = ./builder.sh;

  buildInputs = [ gfortran openmpi openblas liblapack ];

  doCheck = true;

  enableParallelBuilding = true;

  meta = {
    description = "HYPRE: Scalable Linear Solvers and Multigrid Methods";
    homepage = http://https://computation.llnl.gov/projects/hypre-scalable-linear-solvers-multigrid-methods;
    license = stdenv.lib.licenses.gpl2Plus;
    maintainers = [ stdenv.lib.maintainers.tuto ];
    platforms = stdenv.lib.platforms.all;
  };
}
```

At this step, you can use "attributes" to add variants of the package or
to use two differents derivations with two different names (hypre-openmpi and hypre-openmpi-lapack).

For advanced usages, the same nix expression can be used to produce the different versions as shown in this example:

```
{ stdenv, writeText, fetchurl,
  gfortran,
  mpiEnabled ? false,
  openmpEnabled ? false,
  openblasEnabled ? false,
  lapackEnabled ? false,
  openmpi,
  openblas,
  liblapack,
}:

stdenv.mkDerivation rec {
  version = "4.1-b2";
  name = "siesta-${version}";

  src = fetchurl {
    url = "https://launchpad.net/siesta/4.1/${version}/+download/siesta-${version}.tar.gz";
    sha256 = "2b495ae1bef087547444615f1318492e89fa2c00a4303c59f612769b87e73cfc";
  };

  hardeningDisable = [ "format" ];

  enableParallelBuilding = true;

  buildInputs = [ gfortran ]
   ++ (stdenv.lib.optionals mpiEnabled [ openmpi ])
   ++ (stdenv.lib.optionals lapackEnabled [ liblapack ])
   ++ (stdenv.lib.optionals openblasEnabled [ openblas ]);

  builder = if mpiEnabled && openmpEnabled && openblasEnabled
                   then ./builder-mpi-openmp-openblas.sh
            else
            if mpiEnabled && openmpEnabled && !openblasEnabled
                   then ./builder-mpi-openmp.sh
            else
            if mpiEnabled && !openmpEnabled && openblasEnabled && lapackEnabled
                   then ./builder-mpi-openblas.sh
            else
            if mpiEnabled && ! openmpEnabled && !openblasEnabled
                   then ./builder-mpi.sh
            else
                   ./builder-serial.sh;

  meta = {
    description = "A first-principles materials simulation code using DFT";
    longDescription = ''
    SIESTA is both a method and its computer program implementation, to perform efficient electronic structure calculations and ab initio molecular dynamics simulations of molecules and solids.
      '';
    homepage = "http://departments.icmab.es/leem/siesta/";
    license = stdenv.lib.licenses.gpl2;
    platforms = stdenv.lib.platforms.linux;
  };
}

```

For each siesta builder, you have to add a corresponding entry in the nixpkgs/pkgs/top-level/all-packages.nix

For example:

```
 siesta = callPackage ../applications/science/molecular-dynamics/siesta {
  };

  siestaOpenMP = lowPrio (callPackage ../applications/science/molecular-dynamics/siesta {
    mpiEnabled = false;
    openmpEnabled = true;
    openblasEnabled = false;
    lapackEnabled = false;
  });
```

## Adding your package in the nixpkgs main repository

Read the Nixpkgs Contributors Guide to follow the guidelines.
You have now to submit a
patch or pull request to have it accepted into the main Nixpkgs
repository.


## Annexe: Debug
<a name="Debug"></a>

### the nix-build -K option
The -K option of nix-build command keep a trace of the building process in /tmp.

### the builder phases

The generic builder has a number of phases. The major phases are:

    First the environment is set up
    Unpack phase: we unpack the sources in the current directory (remember, Nix changes dir to a temporary directory first)
    Change source root to the directory that has been unpacked
    Configure phase: ./configure
    Build phase: make
    Install phase: make install

### nix-shell

We call nix-shell on a nix expression which returns a derivation, then enter a new bash shell.

```
$ nix-shell . -A hello.nix
```

The nix-shell tool setup the necessary environment variables to handle a derivation, and to execute manually the different phases of the package build, and debug the nix expression.

## Annexe: Tips

By default, unfree package installation are not allowed. We can change this behaviour :

For `nixos-rebuild` you can set

```
{ nixpkgs.config.allowUnfree = true; }
```

in configuration.nix to override this.


For `nix-env`, `nix-build`, `nix-shell` or any other Nix command you can add

```
{ allowUnfree = true; }
```

to your ~/.config/nixpkgs/config.nix.


```
$ mkdir .config/nixpkgs

$ emacs .config/nixpkgs/config.nix
```

Here an example:

```
$ cat .config/nixpkgs/config.nix

{

allowUnfree = true;
allowBroken = true;
permittedInsecurePackages = [
       "libplist-1.12"
       "webkitgtk-2.4.11"
  ];

}
```

When compiling the code, some options of the standard environment provided by Nix, are generating some warnings. This behavior
can be changed, adding this line in your derivation:
```
hardeningDisable = [ "format" ];
```

Adding your name in the maintainers file:
```
~/nixpkgs$ grep tuto lib/maintainers.nix 
  tuto = "Tuto Nix Jdev2017 <tuto@tuto.net>";
```

# Nix for HPC (multiuser mode)
