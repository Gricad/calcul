---
layout: post
title:  "Nix tutorial"
author: calcul-team
categories: Nix
---

table of content
* TOC
{:toc}


## Introduction

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

# First step : how to install Nix package manager on your laptop ?
## Install Nix (single user mode)
sources : [nix manual](http://nixos.org/nix/manual/#chap-installation)

Prerequisites :
  - Linux (64bits) / Mac OS
  - Be a sudoer or have root access.
  - Bash, curl installed

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
$ bash <(curl https://nixos.org/nix/install)
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

Donner des détails sur le contenu de ces répertoires ? Plus tard ?

## Uninstall Nix
You can easily uninstall Nix from your system typing :
{% highlight bash %}
sudo rm -rf /nix
rm -rf ~/.nix-profile
{% endhighlight %}

# Using Nix basics
## Activate your Nix environment

nix environment must be enable by running: 
{% highlight bash %}
source ~/.nix-profile/etc/profile.d/nix.sh
{% endhighlight %}

This creates a set of variables and configure the PATH variable to point to your nix profile.
It could be safe to put this line into your .bashrc file, for next logins.

{% highlight bash %}
$ env | grep nix
NIX_PATH=nixpkgs=/home/your_login/.nix-defexpr/channels/nixpkgs
PATH=/home/your_login/.nix-profile/bin:/home/your_login/.nix-profile/sbin:/usr/local/bin:/usr/bin:/bin:
{% endhighlight %}

## Installing packages and create user environment.

At this point it's important to understand the underlying mechanisms of nix for libraries installation and management.
Nix is made to allow different users to have different configurations and to switch between them but
with one and only one place where everything is installed : /nix.
One of the main benefits of using nix is that any user (understand non-root) is allowed to "install"
packages in /nix. But this package will be available in the user environment through some trees of symlink
between /nix and ~/.nix-profile.

Moreover, thanks to profile, a single user can easyly switch between different configurations.

It's time to create your first profile :
{% highlight bash %}
nix-env --switch-profile $NIX_USER_PROFILE_DIR/tuto-jdev
{% endhighlight%}

From that point, every package you install will be available under this profile.
The operation above just update the link between ~/.nix-profile and some directory in /nix
To check this connection, try:
{% highlight bash %}
ls -altr ~/.nix-profile
{% endhighlight%}

### Installing my first package with Nix
Let us assume that you need some specific library, say for instance fftw.
First of all, you need to check if this package is available, if so which is
the version number and so on:

The complete list of all available packages can be obtained thanks to the command
{% highlight bash %}
$ nix-env -qaP

... **very long list**
{% endhighlight %}

combined with grep to target a specific library:
{% highlight bash %}
$ nix-env -qaP | grep fft
ciment-channel.fftw                                                      fftw-double-3.3.6-pl1
ciment-channel.fftwLongDouble                                            fftw-long-double-3.3.6-pl1
ciment-channel.fftwFloat                                                 fftw-single-3.3.6-pl1
ciment-channel.python27Packages.pyfftw                                   python2.7-pyfftw-0.10.4
ciment-channel.python35Packages.pyfftw                                   python3.5-pyfftw-0.10.4
{% endhighlight %}

(qaP : q as query, a as available and P as preserve-installed)

Ok, now you're able to choose the fftw version that fits you. Notice
on the right column, the complete name of the package and on the
left column, the channel and component name.

TODO : intro avec précision sur le vocabulaire (channel, package, attribut ...)

Once you've find the package name you want to install, you can do it with the following option :
{% highlight bash %}
nix-env -i fftw-double-3.3.6-pl1
{% endhighlight %}

Let us install another package:

{% highlight bash %}
nix-env -i gmsh-2.12.0
{% endhighlight %}

As you noticed, the main command to manage packages with Nix is `nix-env`. You can list all installed packages in your current nix-profile with :

{% highlight bash %}
$ nix-env -q

gmsh-2.12.0
fftw-double-3.3.6-pl1
{% endhighlight %}

and check the consequences of these installations in ~/.nix-profile:

{% highlight bash %}
ls -altr ~/.nix-profile/bin

gmsh -> /nix/store/cbb4r17irfmzb0a37gc4z0zsrj9cj88b-gmsh-2.12.0/bin/gmsh
{% endhighlight %}

{% highlight bash %}
ls -altr ~/.nix-profile/lib

...
libfftw3.so.3 -> /nix/store/95z1jzxvy0db7jikifvdxn7hz11kjq8x-fftw-double-3.3.6-pl1/lib/libfftw3.so.3*
...
{% endhighlight %}

or
{% highlight bash %}
ldd ~/.nix-profile/

	linux-vdso.so.1 (0x00007fff3b39c000)
	libm.so.6 => /nix/store/68sa3m89shpfaqq1b9xp5p1360vqhwx6-glibc-2.25/lib/libm.so.6 (0x00007fc8a30aa000)
	libc.so.6 => /nix/store/68sa3m89shpfaqq1b9xp5p1360vqhwx6-glibc-2.25/lib/libc.so.6 (0x00007fc8a2d0b000)
	/nix/store/68sa3m89shpfaqq1b9xp5p1360vqhwx6-glibc-2.25/lib64/ld-linux-x86-64.so.2 (0x00007fc8a3745000)
{% endhighlight %}


*. libraries and binaries for fftw and gmsh are now available in your local (profile) environment
* this environment (.nix-profile) contains only symbolic links
* everything has been installed in /nix

Next steps:

* create a new profile, check .nix-profile
* install a new version of fftw (single for instance)
* uninstall/reinstall a package --> no installation just re-create links
* switch between profiles, rollback


### Remove packages

To remove a package from your Nix profile, just type :
{% highlight bash %}
nix-env -e the_package_you-re_searching_for
{% endhighlight %}

### Update packages

The following command will update the named package and all its dependencies :
{% highlight bash %}
nix-env -uA the_package_you-re_searching_for
{% endhighlight %}

### Nix easier with Nox
We recommend to use Nox

Nox facilite la recherche et l'installation de paquet car propose clairement les noms des paquets ainsi que leur attribut.


...

Quelques mots sur le garbage collector, le nix store ...


# Adding a package to nix :

## First step : get a local copy of nixpkgs tree
We are going to get a local copy of a the NixOS nikpkgs tree

```
$ git clone git://github.com/NixOS/nixpkgs.git

Initialized empty Git repository in /home/rochf/nixpkgs/.git/
```




Then, go to nixpkgs directory :

```
$ cd nixpkgs
```

## Second step : find a good location for your package and write a nix expression for your package under it
If your package is a library, you will place it under :
pkgs/development/libraries

While a monitoring service will be place under :
pkgs/servers/monitoring

Create a directory for your package :

```
$ mkdir pkgs/development/libraries/libfoo
```

Then create the nix expression of your library package, it is usually called default.nix :

```
$ emacs pkgs/development/libraries/libfoo/default.nix
```

You can copy/paste the default.nix file of another library and modify it to adapt to your own library.

The list of packages is defined in:
`~/nixpkgs/pkgs/top-level/all-packages.nix` 

If you add a new package, add a line for it.

The list of package mainteners is defined in :
`~/nixpkgs/lib/mainteners.nix`

A listing of licence versions is available in :
`~/nixpkgs/lib/licenses.nix`


### Example of "oned" package derivation

The code is available at "http://www.pdc.kth.se:8080/pdc/education/tutorials/mpi/hybrid-lab/oned.c/at_download/file"  

A good place for nix expression of the "oned" package, seems to be : `pkgs/application/science/physics`

```
$ mkdir pkgs/applications/science/physics/oned
$ emacs pkgs/applications/science/physics/oned/default.nix
```

you can use nix-prefetch-url (or similar nix-prefetch-git) to get the SHA-256 hash of source distributions

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

`propagatebuilInputs` defines runtime dependencies.

`buildInputs` and `propagatebuilInputs` are `Meta attributes` ; Meta attributes contain informations about the package. You can choose the necessary ones (the list of available meta-attributes is well specified).

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

## A few definitions

# profiles

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
![Profiles](/images/nix_arborescence.png)

# derivation:
Derivations are the building blocks of a Nix system, from a file system view point. The Nix language is used to describe such derivations.
''derivation'' is also the name of a built-in function. This important built-in function is used to describe a single derivation (a build action). 
It takes as input a set, the attributes of which specify the inputs of the build.

# attributes:
A derivation is build by the function "derivation", using a set of "attributes" that is a list of key/value pairs (see "oned" derivation with following keys : "name", "version", "src", "builder").

## Step 3: Building and installing the Package


The build process is started with the nix-build command:
```
$ nix-build -A oned
```

The nix-build command uses the attribute path ''oned'' to find the derivation and build the package. 

You can check that all the dynamically loaded libraries are inside the /nix/store directory:

```
$ ldd /nix/store/9bf6yzn9s0lcppr6spl0c12nbrw36p71-oned/bin/oned.exe
```

Test the executable :

```
$ oned.exe
```

*bash: oned.exe : command not found*

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

```
$ nix-env -i openmpi

$ mpirun -np 2 /nix/store/9bf6yzn9s0lcppr6spl0c12nbrw36p71-oned/bin/oned.exe 200
```

### Example of hypre Package : Adding the hypre library package to nix ; creation of a derivation.  

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

  buildInputs = [ gfortran openmpi ];

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

We observe that ''make test'' operates under /tmp

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

# Tips
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

