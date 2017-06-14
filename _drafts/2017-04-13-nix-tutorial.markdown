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

# How to install Nix package manager :
## Install Nix (single user mode)
**Source** : http://nixos.org/nix/manual/#chap-installation

### Prerequisites :
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

Donner des détails sur le contenu de ces répertoires ? Plus tard ?

## Uninstall Nix
You can easily uninstall Nix from your system typing :
{% highlight bash %}
sudo rm -rf /nix
rm -rf ~/.nix-profile
{% endhighlight %}

# Using Nix basics
## Activate your Nix environment

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
nix-env --switch-profile /nix/var/nix/profiles/tuto-jdev
{% endhighlight %}

With this command, Nix create the "tuto-jdev" profile if it doesn't exist, and switch to it.
Again, you can check changes :
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

## Installing packages

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

### Install my first package with Nix
Let us assume that you need some specific library, say for instance fftw.
First of all, you need to check if this package is available, if so which is
the version number and so on:

The complete list of all available packages can be obtained thanks to the command
{% highlight bash %}
nix-env -qaP

... **very long list**
{% endhighlight %}

combined with grep to target a specific library:
{% highlight bash %}
nix-env -qaP |grep fft
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
nix-env -q

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

## First step : get a local copy of nixpkgs tree :
We are going to get a local copy of a the NixOS nikpkgs tree

`$ git clone git://github.com/NixOS/nixpkgs.git`

<em>Initialized empty Git repository in /home/rochf/nixpkgs/.git/</em>

<em>...
</em>


Then, go to nixpkgs directory :

`cd nixpkgs`

## Second step : find a good location for your package ; place a nix expression for your package under it :
If your package is a library, you will place it under :
pkgs/development/libraries

While a monitoring service will be place under :
pkgs/servers/monitoring

Create a directory for your package :

`mkdir pkgs/development/libraries/libfoo`

Then create the nix expression of your library package, it is usually called default.nix :

`$ emacs pkgs/development/libraries/libfoo/default.nix	`

You can copy/paste the default.nix file of another library and modify it to adapt to your own library.

The list of packages is defined in :
`~/nixpkgs/pkgs/top-level/all-packages.nix `

If you add a new package, you have to add a line for it.

The list of package mainteners is defined in :
`~/nixpkgs/lib/mainteners.nix`

A listing of licence versions is available in :
`~/nixpkgs/lib/licenses.nix`


### Example of "oned" package

The code is available at "http://www.pdc.kth.se:8080/pdc/education/tutorials/mpi/hybrid-lab/oned.c/at_download/file"  

A good place for nix expression of the "oned" package, seems to be : `pkgs/application/science/physics`

{% highlight bash %}
$ mkdir pkgs/applications/science/physics/oned
$ emacs pkgs/applications/science/physics/oned/default.nix
{% endhighlight %}

you can use nix-prefetch-url (or similar nix-prefetch-git) to get the SHA-256 hash of source distributions

`nix-prefetch-url http://www.pdc.kth.se:8080/pdc/education/tutorials/mpi/hybrid-lab/oned.c/at_download/file`

*1585yzy1gkg3bxfg19mh3ag1x7yik2h3lg5kz705d3jk9dhjg03b*

Or, in case you have already downloaded the source code, use `sha256sum`" command to specify the sha256 record

Ex:

`sha256sum oned.tar.gz`

`buildInputs` defines a set of Nix packages dependencies for package build.

`propagatebuilInputs` defines runtime dependencies.

`buildInputs` and `propagatebuilInputs` are `Meta attributes` ; Meta attributes contain informations about the package. You can choose the necessary ones (the list of available meta-attributes is well specified).

Add your maintainer name with your email, respecting the alphabetical order :

`emacs ~/nixpkgs/lib/maintainers.nix`

Declare the package in the list of packages :

`emacs ~/nixpkgs/pkgs/top-level/all-packages.nix`

Add the following line (in the SCIENCE zone, and respecting the alphabetical order) :

`oned = callPackage ../applications/science/physics/oned  { };`

A Derivation for oned :

`cat  ~/nixpkgs/pkgs/applications/science/physics/oned/default.nix`

{% highlight bash %}
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
{% endhighlight %}

Then we can build the Package :

`nix-build -A oned`

And check that all the dynamically loaded libraries are inside the /nix/store directory:

`ldd /nix/store/9bf6yzn9s0lcppr6spl0c12nbrw36p71-oned/bin/oned.exe`

Test the executable :

`oned.exe`

*bash: oned.exe : command not found*

*installing ‘oned’*

`nix-env -f . -iA oned`

<em>building path(s) ‘/nix/store/66rh542l3hnwscgvd39n784qamympv8p-user-environment’</em>

<em>created 67 symlinks in user environment</em>


`nix-env -i ./result`

<em>
replacing old ‘oned’
installing ‘oned’
building path(s) ‘/nix/store/q90hj0l7vxwc23g1h0vhr7b72k0rcicp-user-environment’</em>

<em>created 384 symlinks in user environment</em>


Now we can test the oned program:

`oned.exe 200`

Then a MPI run :

`nix-env -i openmpi`

`mpirun -np 2 /nix/store/9bf6yzn9s0lcppr6spl0c12nbrw36p71-oned/bin/oned.exe 200`

### Example of hypre Package : Adding the hypre library package to nix ; creation of a derivation.  

hypre web page : https://computation.llnl.gov/projects/hypre-scalable-linear-solvers-multigrid-methods

Get the source distribution hash :

`nix-prefetch-url https://computation.llnl.gov/projects/hypre-scalable-linear-solvers-multigrid-methods/download/hypre-2.11.2.tar.gz`

<em>downloading ‘https://computation.llnl.gov/projects/hypre-scalable-linear-solvers-multigrid-methods/download/hypre-2.11.2.tar.gz’.. [6464/7888 KiB, 1207.1 KiB/s]</em>

<em>path is ‘/nix/store/m2xv5bsy7kp8916pd6j5irn8sn828w5s-hypre-2.11.2.tar.gz’</em>

<em>17i6zgywcmgbmr7zxgc7shzqramg64a8kwswpdqkyn8ichic3di5</em>

Fill in all-packages.nix file :

`$  grep -i 'hypre' pkgs/top-level/all-packages.nix`

<em>hypre = callPackage ../development/libraries/hypre { };</em>

A derivation to build hypre package :

`$ cat pkgs/development/libraries/hypre/default.nix`

{% highlight bash %}
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
{% endhighlight %}

`nix-build -A hypre` 		# We observe that ''make test'' operates under /tmp

<em>Making test drivers ...
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
</em>

The test directory is not persistent :

`ls /tmp/nix-build-hypre-2.11.2.drv-0/hypre-2.11.2/src/test`

<em>File not found:  '/tmp/nix-build-hypre-2.11.2.drv-0/hypre-2.11.2/src/test'</em>

`ls -al /nix/store/cmr0hkvq40b29gy5ppsylksg0yk99ypc-hypre-2.11.2/lib/`

<em>-r--r--r-- 1 tuto tuto 18477350 janv.  1  1970 libHYPRE.a</em>

Test building shared libraries with openblas and liblapack :

`./configure --enable-shared --prefix=$out && make && make install && make test`

`cat pkgs/development/libraries/hypre/builder.sh`
{% highlight bash %}
  source $stdenv/setup
  tar -zxvf $src
  cd $name/src
  ./configure --prefix=$out --enable-shared --enable-fortran CXX=mpicxx --with-MPI --with-MPI-include='${openmpi}/include' --with-MPI-lib-dirs='${openmpi}/lib' --with-MPI-libs='mpi' --with-blas-lib-dirs='${openblas}/lib' --with-blas-libs='openblas' --with-lapack-lib='-llapack'
  make
  make install
  make test
{% endhighlight %}

`cat pkgs/development/libraries/hypre/default.nix`
{% highlight bash %}
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
{% endhighlight %}


Note : parler de l'option allowunfree.
By default, unfree package installation are not allowed. We can change this behaviour :

- For `nixos-rebuild` you can set

  `{ nixpkgs.config.allowUnfree = true; }`

in configuration.nix to override this.


- For `nix-env`, `nix-build`, `nix-shell` or any other Nix command you can add

  `{ allowUnfree = true; }`

to ~/.config/nixpkgs/config.nix.

`mkdir .config/nixpkgs`

`emacs .config/nixpkgs/config.nix`

`cat .config/nixpkgs/config.nix`

{% highlight bash %}
{

allowUnfree = true;
allowBroken = true;
permittedInsecurePackages = [
       "libplist-1.12"
       "webkitgtk-2.4.11"
  ];

}
{% endhighlight %}
