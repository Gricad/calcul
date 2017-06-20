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

1. un mot sur le déroulement de la séance
* intro générale sur nix
* comment l'installer sur sa machine
* les bases : utilisation en boîte noire
* utilisateur avancé : créer son paquet nix
* administrateur : installation sur un serveur de calcul
2. slides de Bruno à reprendre : https://ciment.ujf-grenoble.fr/wiki-pub/images/f/f7/NIX_BUX_2016.pdf
Objectifs :
 * que fait nix, dans quelles circonstances est-ce utile?
3. Rappel du contexte de ce tuto : retour d'expérience dans un contexte HPC

## Overview of the differents packages managers
## Bibliography
## Vocabulary


# Using Nix packages manager
## Prerequisites
  - Linux (64bits) / Mac OS
  - Be a sudoer or have root access.
  - Bash, curl installed

## Install Nix (single user mode)
**Source** : http://nixos.org/nix/manual/#chap-installation

From a basic environment you just have to run the following command :
{% highlight bash %}
bash <(curl https://nixos.org/nix/install)
{% endhighlight %}
**Note** : If you don't have sudo installed or if you're not a sudoer, you have to execute this command as root :
{% highlight bash %}
mkdir -m 0755 /nix && chown your_login /nix
{% endhighlight %}

From this point, you should see something like this :

{% highlight bash %}
bash <(curl https://nixos.org/nix/install)
[...]
performing a single-user installation of Nix...
copying Nix to /nix/store...............................
initialising Nix database...
creating /home/your_login/.nix-profile
installing ‘nix-1.11.9’
building path(s) ‘/nix/store/7dv1lghxz40rbvv9ffg7fq2as972a4r7-user-environment’
created 6 symlinks in user environment
downloading Nix expressions from ‘https://d3g5gsiof5omrk.cloudfront.net/nixpkgs/nixpkgs-17.09pre106045.7369fd0b51/nixexprs.tar.xz’...
downloading ‘https://d3g5gsiof5omrk.cloudfront.net/nixpkgs/nixpkgs-17.09pre106045.7369fd0b51/nixexprs.tar.xz’... [6977/8550 KiB, 3474.3 KiB/s]
unpacking channels...
created 2 symlinks in user environment

Installation finished!  To ensure that the necessary environment
variables are set, either log in again, or type

  . /home/your_login/.nix-profile/etc/profile.d/nix.sh

in your shell.
{% endhighlight %}


The Nix package manager is now installed on your system and ready to be used.

The installation process only populates the directory `/nix` and creates a symbolic link `~/.nix-profile` in your home directory.

## Uninstall Nix
You can easily uninstall Nix from your system typing :
{% highlight bash %}
sudo rm -rf /nix
rm -rf ~/.nix-profile
{% endhighlight %}

## Activate your Nix environments

First you have to source the following script to use your new Nix environment :

{% highlight bash %}
source ~/.nix-profile/etc/profile.d/nix.sh
{% endhighlight %}

This create a set of variables and configure the PATH variable to point to your default nix profile.

You can check changes typing :

{% highlight bash %}env | grep nix

NIX_PATH=nixpkgs=/home/your_login/.nix-defexpr/channels/nixpkgs
PATH=/home/your_login/.nix-profile/bin:/home/your_login/.nix-profile/sbin:/usr/local/bin:/usr/bin:/bin:
{% endhighlight %}

## Working with profiles, create user environment

Nix packages manager uses "profiles" to helps users manage as many environments as needed.
Users can switch between each profiles and each profile history levels.

What is my current profile ?
Nix automaticaly create your first "default" profile. It create a symbolic link pointing to **/nix/var/nix/profiles/default**.
{% highlight bash %}ls -l ~/.nix-profile/
lrwxr-xr-x  1 your_login  staff  29 15 nov  2016 .nix-profile -> /nix/var/nix/profiles/default
{% endhighlight %}

To create a new profile and switch to :
{% highlight bash %}
nix-env --switch-profile /nix/var/nix/profiles/per-user/your_login/tuto-jdev
{% endhighlight %}

With this command, Nix create the "tuto-jdev" profile if it doesn't exist, and switch to it.
You can check changes :
{% highlight bash %}ls -l ~/.nix-profile/
lrwxr-xr-x  1 your_login  staff  29 15 nov  2016 .nix-profile -> /nix/var/nix/profiles/tuto-jdev
{% endhighlight %}

You can now work with differents profiles and switch between them.

You can undo a **nix-env** command with :
{% highlight bash %}
nix-env --rollback
{% endhighlight %}

To view the entire profile history (called "links generations") :
{% highlight bash %}
nix-env --list-generations
{% endhighlight %}

You can directly return to a specific generation with its Id :
{% highlight bash %}
nix-env --switch-generation 42
{% endhighlight %}

You can have as much profile as needed. That way, you can have many environments.

# Nix basics

At this point it's important to understand the underlying mechanisms of nix for libraries installation and management.
Nix is made to allow different users to have different configurations and to switch between them but
with one and only one place where everything is installed : /nix.
One of the main benefits of using nix is that any user (understand non-root) is allowed to "install"
packages in /nix. But this package will be available in the user environment through some trees of symlink
between /nix and ~/.nix-profile.

Moreover, thanks to profile, a single user can easyly switch between different configurations.

Let's start using Nix with our new "tuto-jdev" profile. Make sure you're using the right profile :
{% highlight bash %}
nix-env --switch-profile $NIX_USER_PROFILE_DIR/tuto-jdev
{% endhighlight%}

From that point, every package you install will be available under this profile.
The operation above just update the link between ~/.nix-profile and some directory in /nix
To check this connection, try:
{% highlight bash %}
ls -altr ~/.nix-profile
{% endhighlight%}

## Install Nix packages
Let us assume that you need some specific library, say for instance fftw.
First of all, you need to check if this package is available, if so which is the version number and so on:

The complete list of all available packages can be obtained thanks to the command
{% highlight bash %}
nix-env -qaP

... **very long list**
{% endhighlight %}

combined with grep to target a specific library:
{% highlight bash %}
nix-env -qaP | grep fftw
nixpkgs.fftw                                                   fftw-double-3.3.5
nixpkgs.fftwLongDouble                                         fftw-long-double-3.3.5
nixpkgs.fftwFloat                                              fftw-single-3.3.5
nixpkgs.python27Packages.pyfftw                                python2.7-pyfftw-0.10.4
nixpkgs.python35Packages.pyfftw                                python3.5-pyfftw-0.10.4
{% endhighlight %}

(qaP : q as query, a as available and P as preserve-installed)

Ok, now you're able to choose the fftw version that fits you. Notice
on the right column, the complete name of the package and on the
left column, the attributes of the package (channel and components name between dots).

Once you've find the package name you want to install, you can do it with the following option (by name) :
{% highlight bash %}
nix-env -i fftw-double-3.3.5
{% endhighlight %}

Or (by attributes) :
{% highlight bash %}
nix-env -iA nixpkgs.fftw
{% endhighlight %}

Check the consequences of these installations in ~/.nix-profile:

{% highlight bash %}
ls -altr ~/.nix-profile/bin

.nix-profile/bin/fftw-wisdom -> /nix/store/fbfbah2swf6ib9x0vk816y2ymiw648bp-fftw-double-3.3.6-pl1-dev/bin/fftw-wisdom
{% endhighlight %}

Take a look at the dependencies :

{% highlight bash %}
ldd .nix-profile/bin/fftw-wisdom
	linux-vdso.so.1 (0x00007ffc02114000)
	libfftw3_threads.so.3 => /nix/store/95z1jzxvy0db7jikifvdxn7hz11kjq8x-fftw-double-3.3.6-pl1/lib/libfftw3_threads.so.3 (0x00007f9521814000)
	libfftw3.so.3 => /nix/store/95z1jzxvy0db7jikifvdxn7hz11kjq8x-fftw-double-3.3.6-pl1/lib/libfftw3.so.3 (0x00007f952148c000)
	libm.so.6 => /nix/store/68sa3m89shpfaqq1b9xp5p1360vqhwx6-glibc-2.25/lib/libm.so.6 (0x00007f9521179000)
	libpthread.so.0 => /nix/store/68sa3m89shpfaqq1b9xp5p1360vqhwx6-glibc-2.25/lib/libpthread.so.0 (0x00007f9520f5b000)
	libc.so.6 => /nix/store/68sa3m89shpfaqq1b9xp5p1360vqhwx6-glibc-2.25/lib/libc.so.6 (0x00007f9520bbc000)
	/nix/store/68sa3m89shpfaqq1b9xp5p1360vqhwx6-glibc-2.25/lib/ld-linux-x86-64.so.2 => /lib64/ld-linux-x86-64.so.2 (0x00007f9521a1b000)
{% endhighlight %}


* libraries and binaries for fftw are now available in your local (profile) environment
* this environment (.nix-profile) contains only symbolic links
* everything has been installed in /nix

## Remove packages

To remove a package from your Nix profile, just type :
{% highlight bash %}
nix-env -e the_package_you-re_searching_for
{% endhighlight %}

## Update packages

The following command will update the named package and all its dependencies :
{% highlight bash %}
nix-env -uA the_package_you-re_searching_for
{% endhighlight %}

## Nix easier with Nox
Now we know the basics Nix commands, it could be interesting to install Nox. Nox is a Nix package that helps you manage Nix packages.

Let's try it :
{% highlight bash %}
nix-env -i nox
{% endhighlight %}

Nox provide a command line interface to search and install packages.
For instance, to install the fftw package with nox, you just have to type :
```
nox fftw
```
Nox lists the matching packages list. To install a specific version you just have to enter the number of the package in this list.

![Nox search and install]({{ site.url }}/tuto_nix/media/nox_install.png)


# Development environments

## your first ''hello'' basic package

This first example is an introduction to the development of nix packages to install custom libraries without interfering with
other projects.

The source code of this ''hello'' package is:
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
      md5 = "70c9ccf9fac07f762c24f2df2290784d";
    };
  };
}
```

This file is called a nix epression. The function "mkDerivation" use a nix expression block as input to build a derivation of the "hello" package.
You can see some attributes (attributes are set of key/value pairs) like version/2.1.1.
The building process of "hello" program needs some tools : a standard development environment (stdenv), a function to download the source code (fetchurl).
The stdenv.mkDerivation execute the building operations (configure, make, make install, ...).

### derivation:
A derivation from a Nix language view point is simply a set, with some attributes.
Derivations are the building blocks of a Nix system, from a file system view point. The Nix language is used to describe such derivations.
''derivation'' is also the name of a built-in function. This important built-in function is used to describe a single derivation (a build action).
It takes as input a set, the attributes of which specify the inputs of the build.

### attributes:
A derivation is build by the function "mk.Derivation", using a set of "attributes" that is a list of key/value pairs (see "oned" derivation with following keys : "name", "version", "src", "builder").



Nix expressions describe how to build packages from source and are collected in the nixpkgs repository. The Nix Packages collection (Nixpkgs) is a set of thousands of packages for the Nix package manager,

## How to add a package to nixpkgs :

### First step : get a local copy of nixpkgs tree

We are going to get a local copy of a the NixOS nikpkgs tree

```
$ git clone git://github.com/NixOS/nixpkgs.git

Initialized empty Git repository in /home/rochf/nixpkgs/.git/
```


Then, go to nixpkgs directory :

```
$ cd nixpkgs
```

### Second step : find a good location for your package and write a nix expression for your package under it

If your package is a library, you will place it under :
pkgs/development/libraries

While a monitoring service will be place under :
pkgs/servers/monitoring

Create a new directory for your package "mylib":

```
$ mkdir pkgs/development/libraries/mylib
```

Then create the nix expression of your library package, it is usually called default.nix :

```
$ emacs pkgs/development/libraries/mylib/default.nix
```

You can copy/paste the default.nix file of another library and modify it to adapt to your own library.

The list of packages is defined in:
`~/nixpkgs/pkgs/top-level/all-packages.nix`

If you add a new package, add a line for it.

The list of package mainteners is defined in :
`~/nixpkgs/lib/mainteners.nix`

A listing of licence versions is available in :
`~/nixpkgs/lib/licenses.nix`





#### Example of "oned" package derivation
Oned is a program which solve the Poisson equation using Jacobi method.

The code is available at "http://www.pdc.kth.se:8080/pdc/education/tutorials/mpi/hybrid-lab/oned.c/at_download/file"  

A good place for nix expression of the "oned" package, seems to be : `pkgs/application/science/physics`

```
$ mkdir pkgs/applications/science/physics/oned
$ emacs pkgs/applications/science/physics/oned/default.nix
```

you can use "nix-prefetch-url" command (or similar "nix-prefetch-git" command) to get the SHA-256 hash of source distributions.

```
$ nix-prefetch-url http://www.pdc.kth.se:8080/pdc/education/tutorials/mpi/hybrid-lab/oned.c/at_download/file
```

*1585yzy1gkg3bxfg19mh3ag1x7yik2h3lg5kz705d3jk9dhjg03b*

Or, in case you have already downloaded the source code, use `sha256sum`" command to specify the sha256 record

Ex:

```
$ sha256sum oned.tar.gz
```

`buildInputs` defines a set of Nix packages dependencies for package build.

`propagatebuildInputs` defines runtime dependencies.

`buildInputs` and `propagatebuildInputs` are `Meta attributes` ; Meta attributes contain informations about the package. You can choose the necessary ones (the list of available meta-attributes is well [specified](http://nixos.org/nixpkgs/manual/#chap-meta).




Add your maintainer name with your email, respecting the alphabetical order :

```
$ emacs ~/nixpkgs/lib/maintainers.nix
```

Declare the package in the list of packages :

```
$ emacs ~/nixpkgs/pkgs/top-level/all-packages.nix
```

Add the following line (in the SCIENCE zone, and respecting the alphabetical order) :

`oned = callPackage ../applications/science/physics/oned  { };`

A Derivation for oned :

```
$ cat  ~/nixpkgs/pkgs/applications/science/physics/oned/default.nix

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

### A few definitions

#### profiles

A few commands can help you to understand the nix profiles concept:

First install the flex package version 2.5.35 in your own environment:

```
$ nix-env -i flex-2.5.35
```
Have a look to the user-environment links (each default-n-link is a nix profile):

```
$ ls -al /nix/var/nix/profiles/
total 32
drwxr-xr-x. 3 rochf users 4096 13 juin  18:56 .
drwxr-xr-x. 7 rochf users 4096  3 mai   18:30 ..
lrwxrwxrwx. 1 rochf users   14 13 juin  18:56 default -> default-5-link
lrwxrwxrwx. 1 rochf users   60  3 mai   18:30 default-1-link -> /nix/store/7dv1lghxz40rbvv9ffg7fq2as972a4r7-user-environment
lrwxrwxrwx. 1 rochf users   60 13 juin  18:29 default-2-link -> /nix/store/a8vm5sbpry5y1cijdx2c4sygnxnzw10s-user-environment
lrwxrwxrwx. 1 rochf users   60 13 juin  18:30 default-3-link -> /nix/store/cxjbqskymd8k5j15vc17d167cgrxw1y2-user-environment
lrwxrwxrwx. 1 rochf users   60 13 juin  18:34 default-4-link -> /nix/store/q3an4jnmp8qzahb9bcanlinzg3xsvwpx-user-environment
lrwxrwxrwx. 1 rochf users   60 13 juin  18:56 default-5-link -> /nix/store/yalvpxnrlkg79a1mj16snd8lavgc9s23-user-environment
drwxr-xr-x. 3 rochf users 4096  3 mai   18:30 per-user

$ ls -al /nix/var/nix/profiles/default-5-link/bin/flex
lrwxrwxrwx. 1 rochf users 64  1 janv.  1970 /nix/var/nix/profiles/default-5-link/bin/flex -> /nix/store/cwnv702d155b6y3h8zqr2v796bqwcrzd-flex-2.5.35/bin/flex
```
The flex installation was done in the current profile (with a link to the last installed version).
Now install a new flex version:

```
$ nix-env -i flex-2.6.1

$ ls -al /nix/var/nix/profiles/default
lrwxrwxrwx. 1 rochf users 14 13 juin  19:04 /nix/var/nix/profiles/default -> default-6-link

$ ls -al /nix/var/nix/profiles/default-6-link/bin/flex
lrwxrwxrwx. 1 rochf users 63  1 janv.  1970 /nix/var/nix/profiles/default-6-link/bin/flex -> /nix/store/k9ng0zfjf999dp96pphhhlfyazvwxjdd-flex-2.6.1/bin/flex
```
A new environment has been created.
Install now another package:

```
$ nix-env -i fox
$ ls -al /nix/var/nix/profiles/default
lrwxrwxrwx. 1 rochf users 14 13 juin  19:08 /nix/var/nix/profiles/default -> default-7-link
```
Each time you're using the nix-env command, a new environment is created.

As you can see below, both fox and flex links are created in this new environment.

```
$ ls -al /nix/var/nix/profiles/default-7-link/bin/fox-config
lrwxrwxrwx. 1 rochf users 68  1 janv.  1970 /nix/var/nix/profiles/default-7-link/bin/fox-config -> /nix/store/pksh5q16xzikcwwbzjlqdlq5303s2lak-fox-1.7.9/bin/fox-config

$ ls -al /nix/var/nix/profiles/default-7-link/bin/flex
lrwxrwxrwx. 1 rochf users 63  1 janv.  1970 /nix/var/nix/profiles/default-7-link/bin/flex -> /nix/store/k9ng0zfjf999dp96pphhhlfyazvwxjdd-flex-2.6.1/bin/flex
```

Then switch to an older generation of environment:

```
$ nix-env --switch-generation 5
switching from generation 7 to 5

$ ls -al /nix/var/nix/profiles/default
lrwxrwxrwx. 1 rochf users 14 13 juin  19:13 /nix/var/nix/profiles/default -> default-5-link
```
Let's note that ''default'' point to the current generation.

This nice picture illustrates the generation mechanisms:
![Profiles]({{site_url}}/tuto_nix/media/nix_arborescence.png)


### Third step: Building and installing the Package


The build process is started with the nix-build command:
```
$ nix-build -A oned
```

The nix-build command uses the attribute path ''oned'' to find the derivation and build the package.
The "-A attrPath" nix-env option select an attribute from the top-level Nix expression being evaluated.

You can check that all the dynamically loaded libraries are inside the /nix/store directory:

```
$ ldd /nix/store/9bf6yzn9s0lcppr6spl0c12nbrw36p71-oned/bin/oned.exe
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


```
$ nix-env -i ./result

replacing old ‘oned’
installing ‘oned’
building path(s) ‘/nix/store/q90hj0l7vxwc23g1h0vhr7b72k0rcicp-user-environment'

created 384 symlinks in user environment
```

Now we can test the oned program:

```
$ oned.exe 200
```

Then a MPI run :
We need a mpi environment to be installed:

```
$ nix-env -i openmpi

$ mpirun -np 2 /nix/store/9bf6yzn9s0lcppr6spl0c12nbrw36p71-oned/bin/oned.exe 200
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
If you want to install both versions of this package you have to use two differents derivations with two different names (hypre-openmpi and hypre-openmpi-lapack).
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

  #hardeningDisable = [ "format" ];

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



## Annexe: Debug
<a name="Debug"></a>

### the nix-build -K option
The -K option of nix-build command keep a trace of the building process in /tmp.

### the builder phases

The builder has these phases:

    First the environment is set up
    Unpack phase: we unpack the sources in the current directory (remember, Nix changes dir to a temporary directory first)
    Change source root to the directory that has been unpacked
    Configure phase: ./configure
    Build phase: make
    Install phase: make install

The -K option of nix-env command keep a trace of the building process in /tmp.


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

# Nix for HPC (multiuser mode)
