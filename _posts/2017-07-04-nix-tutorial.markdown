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

Introduction of this tutorial is currently in French, as the following PDF presentation:

[NIX tutorial introduction](https://github.com/Gricad/calcul/raw/master/tuto_nix/media/NixIntroJDEV2017.pdf).


# Using Nix packages manager

> _In this first section, you will learn_:
>
> * _how to **install** nix on your laptop,_
> * _how to **setup** properly your working environment to use nix **profiles**,_
> * _and obviously how to **remove** nix properly and completely._

## Prerequisites
  - Linux (64bits) / Mac OS
  - Be a sudoer or have root access.
  - Bash, curl installed

If this prerequisites are not fullfilled or if you don't want to install nix on your system, you may
try to run this tutorial inside a docker container. Try the following link, wich provides a Dockerfile and some directives :

- *[Optional docker image for this tutorial](https://github.com/Gricad/calcul/tree/master/tuto_nix/docker/debian_nix_tuto).* 

## Install Nix (single user mode)
**Source** : <http://nixos.org/nix/manual/#chap-installation>

In a terminal, run :
```bash
bash <(curl https://nixos.org/nix/install)
```

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

Check their contents and try
```bash
ls -al ~/.nix-profile
ls -al /nix
```

*Remark : If you don't have sudo installed or if you're not a sudoer, before installing nix, run as root :*

`mkdir -m 0755 /nix && chown <your_login> /nix`


## Uninstall Nix
Nix does not spread out all over your system, so you can easily uninstall it completely by doing:
```bash
sudo rm -rf /nix
rm -rf ~/.nix-*
```

## Working with profiles : create several user environments

At this stage, nix is properly installed on your system, but some extra configuration is required, especially to activate the "profiles" feature.

As explained in the introduction of this tutorial, a **profile** is some kind of user-defined environment, where you'll be able to 'install' and use a specific set of your choice of libraries, tools, binaries ...

Consider for instance, the three profiles defined in the table below:

|**profiles**                                                      |    **installed packages**                      |
|------------------------------------------------------------------|------------------------------------------------| 
|**"my soft based on intel compilers" :**                          | intel-devel 2015, mysoft-release-intel         |
|**"my soft based on gnu compilers"** :'                           | gcc-wrapper-6.3.0, mysoft-release-gnu          |
|**"my soft, debug mode, based on gnu compilers' :** 		   | gcc-wrapper-6.3.0, mysoft-debug-gnu, valgrind  |


In that case, assuming you have defined these profiles, you can switch easily between three different setups of the same software (mysoft), without any interference between them.
Notice that each user can have as many profiles as he wants.


To activate this profile feature, we need to copy and update the nix.sh file provided by the installer:
```bash
cp /nix/var/nix/profiles/default/etc/profile.d/nix.sh ~/nix.sh
echo "export PATH=/nix/var/nix/profiles/default/bin:\$PATH" >> ~/nix.sh
echo "export NIX_USER_PROFILE_DIR=/nix/var/nix/profiles/per-user/\$USER " >> ~/nix.sh
# If you are under MACOS, also add:
echo "export NIX_SSL_CERT_FILE=/nix/var/nix/profiles/default/etc/ssl/certs/ca-bundle.crt" >> ~/nix.sh
```

*Notice the environment variable NIX_USER_PROFILE_DIR that  will be used later to define profiles. Under NiXOS or on some properly installed multi-user sites, this variable might be already set properly during install.*



Finally, load nix environment:

```bash
source ~/nix.sh
```
You can safely add this line into the initialization script of your shell (for example ```~/.bashrc```).

The installation and configuration process is over and you're ready to use nix.

Your current profile is defined by the the .nix-profile symbolic link in your home directory.
Nix automaticaly creates your first "default" profile : it's a symbolic link pointing to **/nix/var/nix/profiles/default**.
```bash
ls -l ~/.nix-profile
lrwxr-xr-x  1 <your_login>  staff  29 15 nov  2016 .nix-profile -> /nix/var/nix/profiles/default
```

To create a new profile, use *nix-env* command (remind that NIX_USER_PROFILE_DIR has been set to /nix/var/nix/profiles/per-user/<your_login>), for instance:

```bash
nix-env --switch-profile $NIX_USER_PROFILE_DIR/tuto-jdev
```

and check:

```bash
ls -l ~/.nix-profile
lrwxr-xr-x ... .nix-profile -> /nix/var/nix/profiles/per-user/<your-login>/tuto-jdev
```

Note: *For the moment, this link may point to a non-existent directory as you don't have installed any package yet. The profile directory will be created at the first installation of a package, you'll see that in the next few lines of this tutorial!*

You can now work with differents profiles and switch between them and have as many profiles as you want. That way, you can have many environments. Once you'll be familiar to Nix, you'll see that you'll switch to a new profile each time you're starting something new! And you will miss this on other systems ;-)

> Summary
> * Always create one (or more) profile(s), to organise properly your different environments
> * What is my current profile? 
>   ```ls -al ~/.nix-profile ```
> * Create/switch between profiles?
>   ```nix-env --switch-profile $NIX_USER_PROFILE_DIR/some_name```
> * What are my available profiles?
>   ```ls -al $NIX_USER_PROFILE_DIR ```



# Nix basics

> In this section, you will learn ...
> - how to install, remove, update a package,
> - how to list and find packages,
> - how to check, rollback your profile.

At this point it's important to understand the underlying mechanisms of nix for libraries installation and management.
Nix is made to allow different users to have different configurations and to switch between them but
with *one and only one place where everything is installed* : /nix.

One of the main benefits of using nix is that any user (understand non-root) is allowed to "install"
packages in /nix. These packages will be available in the user environment through some trees of symlink
between /nix and ~/.nix-profile and ready to be used by any other user.

Moreover, thanks to profiles, a single user can easily switch between different configurations.

Let us start using Nix with our new "tuto-jdev" profile. Make sure you're using the right profile :
```bash
nix-env --switch-profile $NIX_USER_PROFILE_DIR/tuto-jdev
```

From that point, every new installed package will be available under this profile. 
The operation above just updates the link between ~/.nix-profile and some directories in /nix

Once again, check your profile and the linked directory:
```bash
ls -altr ~/.nix-profile
```

## Search, install, remove a package with nix

Most of nix operations are carried out using ```nix-env``` command.

To install a package, use ```nix-env -i <somename>```. For instance:
```bash
~$ nix-env -i hello
installing ‘hello-2.10’
...
```

And the 'hello' binary is now available in your path:

```bash
~$ hello
Hello, world!
~$ which hello
/home/<your_login>/.nix-profile/bin/hello
```

Sounds as if 'hello' has been installed in your home directory.
But if you try 

```bash
ls -altr ~/.nix-profile/bin
```

you will get something like

```bash

.nix-profile/bin -> /nix/store/3dlqv87hrrfjynj0brbn4h71g4g4g89z-hello-2.10/bin
```


Indeed, depending on what has been previously done on your system, the ```nix-env -i`` command will either download the corresponding package, install it
in /nix/store and finally create the required links in your profile (.nix-profile/ ...) or just create the links, if the package is already 
in /nix/store (previous install by you or another user).

It means that hello binary is installed "system wide", in /nix/store, although you're not root, which is one of the very interesting features of nix : you do not depend
on some administrator to install and setup your working environment.

To remove a package, once again call ```nix-env``` with 'erase' option:

```bash
nix-env -e hello
uninstalling ‘hello-2.10’
```

hello has disappear from your path:

```bash
hello
-bash: hello: command not found
```

and from your profile

```bash
ls -altr ~/.nix-profile/bin
ls: .nix-profile/bin: No such file or directory
```

But hello is still present in /nix/store:

```bash
ls  /nix/store/*hello*
/nix/store/bh26bk4rcqlxja3chgn6a3jv7yiqshg4-hello-2.10:
bin   share
```

And if you reinstall it, no download or install occurs, it only creates symbolic links in your .nix-profile. Try install and check output:

```bash
~$ nix-env -i hello
installing ‘hello-2.10’
...
```


Well, hello package is very interesting but you're likely to search for a specific package, say for instance boost.

A complete list of all available packages, in the nix store, is returned by the command 
```bash
nix-env -qaP

... **very long list**
```

Note: *qaP : q as query, a as available and P as preserve-installed*

A smarter usage of this command combined it with a grep to target a specific program or library:

```
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


Ok, now you're able to choose the boost version that fits you. Notice on the right column, the complete name of the package and on the left column, the attributes of the package (channel and components name between dots).

As explained in the introduction a **channel** is no more than a "snapshot" of the nixpkgs reference repository.

The **components** attribute is important since it allows you to distinguish different configurations of the same library. Here for example, you can choose between different versions of boost (1.55, 1.59 ...)
or between different configurations of the same version of boost (1.62 with or without python and with python 2 or python 3 bindings).

Notice also that different packages (different by their attributes) may have the same name (e.g. boost-1.62.0).

==> a good pratice : always use install with complete attributes list to avoid confusion and unexpected behavior.


Choose one version and try to install it by calling ```nix-env -i``` followed by the **name** of the package. For instance:

```bash
nix-env -i boost-1.60.0
```


Try also an explicit call, with **attributes**:

```bash
nix-env -iA nixpkgs.boost160
```

Check the consequences of these installations in ~/.nix-profile:

```bash
ls -ld ~/.nix-profile/lib
  .nix-profile/lib -> /nix/store/h4c1bmm3qk0vifhs3xd5p6c8apciv1gq-boost-1.60.0/lib

```

Let us install another library, to populate a bit more our profile:

```bash
nix-env -iA nixpkgs.openblas
```

Now, check again your profile:

```bash
ls -ld ~/.nix-profile/lib
  .nix-profile/lib
```

Since only one package with a lib path was installed, the *lib* directory in your profile was just a link to the same directory in  *boost* package from nix store. But now that we have another package having a *lib* directory too, lib in your profile becomes a real directory, where nix created a bunch of symbolic links to the shared libraries in nix store:

```bash
ls -altr ~/.nix-profile/lib/libboost_atomic.*
  .nix-profile/lib/libboost_atomic.so -> /nix/store/h4c1bmm3qk0vifhs3xd5p6c8apciv1gq-boost-1.60.0/lib/libboost_atomic.so
ls -altr ~/.nix-profile/lib/libopenblas.*
  .nix-profile/lib/libopenblas.so -> /nix/store/jxm1c9ks0bkfzkv40jwgwv4yxg0paxkq-openblas-0.2.19/lib/libopenblas.so
```

Take a look at the dependencies :

```bash
ldd ~/.nix-profile/lib/libboost_atomic.so
# or if you use MAC OS:
otool -L ~/.nix-profile/lib/libboost_atomic.dylib
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
nix-env -qs
```

## Profile rollback and generations

Each time you perform a Nix operation in your profile, it creates a new **generation** of it. 
This concept of generation in profiles allows you to rollback to any previous state:

first check the  entire profile history (called "links generations") :
```bash
nix-env --list-generations
```

and then switch either to the previous step in profile or step to a chosen state:

Back to previous step:
```bash
~$ nix-env -q
boost-1.60.0
hello-2.10
openblas-0.2.19
~$ nix-env --rollback
switching from generation 5 to 4
~$ nix-env -q
boost-1.60.0
hello-2.10
```
As you can see, the last package we installed is no more here.

Back to a chosen step (assuming 3 is an existing stage in your list-generations)

```bash
nix-env --switch-generation 3
```

## Update packages

The following command will update the named package and all its dependencies :
```bash
nix-env -uA the_package_you-re_searching_for
```
And if the new version of the package  does not work, you can allways do a "--rollback"!

## Channel and NIX_PATH
To understand the *channel* concept, it might be useful to understand how the NIX_PATH environment variable is used. Take a look at it:
```bash
echo $NIX_PATH
  nixpkgs=/home/<your_login>/.nix-defexpr/channels/nixpkgs
```
In your default environment, it contains only one *channel* definition, the *nixpkgs* one. It gives a PATH that is actualy a link to the store:

```bash
readlink ~/.nix-defexpr/channels/nixpkgs
  /nix/store/civk55fs0p07kjnvgjqfdvgws2qvxyq2-nixpkgs-17.09pre109811.ce88027294/nixpkgs
```

And this is where the channel currently used lives (remember: *nix-env -iA **nixpkgs**.boost160*). In this directory, you can find all the files (called *expressions*, we'll see that later) with the code of the packages of the *Nixpkgs* distribution, and the code of the builtin tools (builders, patching tools, ...). 
For example, let's search for the code of the hello package:

```bash
find ~/.nix-defexpr/channels/nixpkgs/ -name hello
```
A file is particularily interesting to look at: ```all-packages.nix```. It's the file where the default attributes of the packages are defined (what you put just after *nix-env -iA*). For example:

```bash
grep hello ~/.nix-defexpr/channels/nixpkgs/pkgs/top-level/all-packages.nix
```

This is not necessary to go further at this point, but remember that any time you wonder what is made inside a package, or how packages are called, you can take a look at this directory. 

By the way, notice that the name of the directory can be used to check the version of the nixpkgs channel you are using. In our example it is *17.09pre109811* (*/nix/store/civk55fs0p07kjnvgjqfdvgws2qvxyq2-nixpkgs-**17.09pre109811**.ce88027294/nixpkgs*)

> Summary
> * Search for packages with ```nix-env -qaP |grep ...```
> * Install packages with ```nix-env -i <package_name>``` or ```nix-env -iA <attribute>```
> * List installed packages with ```nix-env -q```
> * Remove packages with ```nix-env -e <package>```
> * Rollback or jump to a specific version of your profile with
> 
>      ```nix-env --rollback``` or ```nix-env --switch-generation <id>```


# Package development

> In this section, you will learn:
> * What is a Nix expression and a Nix derivation
> * How to create a local package
> * How to debug a package and how the native builder works

Under a Nix environment, creating a package is often the best way to install an application. You should not be afraid about that, it is very easy and satisfying. How many times have you installed a software, locally on your home, and when it's been done, you can't remember how you did? If you do this directly by creating a Nix package, you can't forget as everything will be described. Your application is built inside an isolated environment, with no dependency with the system. Furthermore, you can pass your package to a colleague, or to the Nix community! 

## Your first Nix expression: a basic ''hello'' package

A package is  built from a nix "expression". Nix expressions describe the actions to build packages (getting the sources, patching, compiling, installing...).
  
Here is a sample expression for a basic packaging of the ''hello'' program:

```Nix
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
    hardeningDisable = [ "format" ];
    src = fetchurl {
      url = "ftp://ftp.nluug.nl/pub/gnu/hello/${name}.tar.gz";
      sha256 = "c510e3ad0200517e3a14534e494b37dc0770efd733fc35ce2f445dd49c96a7d5";
    };
  };
}
```

We can see 3 main blocks:
- In the first block, we basically tell that we are going to import the whole 'nixpkgs' set of builtin functions and packages that are available into your Nix environment. This is where the ```$NIX_PATH``` environment variable seen earlier makes sense.
- In the next block, we are setting up attributes that will be available inside the third block
- The last block consists of the actual creation of the package: the *derivation*. A derivation is the name given by Nix to create something from other stuff. The builtin function *.mkDerivation*, provided by *stdenv*, is used to create a package starting from attributes which are key/value pairs.

Some attributes are required (like *name*). A lot of others are optional. It is the case of *builder* for example, that is not present in this example as we will use the builtin standard builder. The builder is the part of the packaging that creates the executables, typically "configure, make, make install". The *buildInputs* attribute defines a list describing all the other packages required as a dependency for the build. In this example, we need "perl" during the build, so the "perl" package will be available into the build environment during the creation of this hello package. 

Finally, the *src* attribute defines the sources of our program to build. It makes use here of the *fetchurl* builtin function provided by stdenv to get the sources from a url and check the integrity with a provided hash.

### Let's build our package!

Create a test directory and put the nix expression in a hello.nix file:

```
$ mkdir test
$ cd test
$ vi hello.nix
```

Then build the package:

```
$ nix-build hello.nix
```

The first time you start such a build, you should normally see Nix downloading packages that are required for this operation. Then, the sources of the hello program are fetched, then built. A post-installation script is automatically started to eventually fix the runpath (RPATH) of the binaries and libraries, and fix the interpreter paths of every scripts to ensure that every dependency will be resolved from the /nix store.

Note: *nix-build provides a convenient ```--keep-failed, -K``` option to keep the temporary build directory in case things goes wrong, so you can inspect the logs if any. But we'll see later another powerful tool to debug failures...* 

A new link ''result'' has been created into the current directory. The destination of the link is the directory of the created package into the store.

```
$ ls -al result/bin/
total 16
dr-xr-xr-x 2 tuto tuto    19 janv.  1  1970 .
dr-xr-xr-x 4 tuto tuto    30 janv.  1  1970 ..
-r-xr-xr-x 1 tuto tuto 13552 janv.  1  1970 hello

$ ./result/bin/hello
Bonjour, le monde!
```

Installing the package is simple as:
```
$ nix-env -i ./result
installing ‘hello-2.1.1’
building path(s) ‘/nix/store/dqv9d96xmimb7xq4wj1jm3j7w4i9ik49-user-environment’
created 500 symlinks in user environment

$ hello --version
hello - GNU hello 2.1.1

```

What about trying to build again the same package?

```bash
rm result
nix-build ./hello.nix
```

Well, as we changed nothing into the source code, the hash of our compiled expression is the same. So, Nix does nothing! It has just re-created the ```./result``` link to the corresponding package into the store. It means that if another user creates the same package as you just did, no re-build is trigged and the binaries will be efficiently shared!  

### Debugging with nix-shell

It's easy when all goes well... but how to deal things when the build process does not work as expected? 

Let's introduce a bug into our expression. Simply comment the line with the buildInputs attribute, to remove the needed dependency with perl:

```Nix
{ pkgs ? import <nixpkgs> {} }:
with pkgs;

let
  inherit stdenv fetchurl perl;
  version = "2.1.1";
in
{
    hello = stdenv.mkDerivation rec {
    name = "hello-${version}";
#    buildInputs = [ perl ];
    hardeningDisable = [ "format" ];
    src = fetchurl {
      url = "ftp://ftp.nluug.nl/pub/gnu/hello/${name}.tar.gz";
      sha256 = "c510e3ad0200517e3a14534e494b37dc0770efd733fc35ce2f445dd49c96a7d5";
    };
  };
}
```

Then, re-build the package:

```bash
nix-build ./hello.nix
```

Now, it should fail with:
```bash
[...]
make[2]: Entering directory '/tmp/nix-build-hello-2.1.1.drv-0/hello-2.1.1/man'
help2man --name="Friendly Greeting Program" ../src/hello >hello.1
/nix/store/wb34dgkpmnssjkq7yj4qbjqxpnapq0lw-bash-4.4-p12/bin/bash: help2man: command not found
make[2]: *** [Makefile:282: hello.1] Error 127
make[2]: Leaving directory '/tmp/nix-build-hello-2.1.1.drv-0/hello-2.1.1/man'
make[1]: *** [Makefile:175: all-recursive] Error 1
make[1]: Leaving directory '/tmp/nix-build-hello-2.1.1.drv-0/hello-2.1.1'
make: *** [Makefile:131: all] Error 2
builder for ‘/nix/store/zsp5846wm86p3fb408knmpa9nfl8k8lr-hello-2.1.1.drv’ failed with exit code 2
error: build of ‘/nix/store/zsp5846wm86p3fb408knmpa9nfl8k8lr-hello-2.1.1.drv’ failed
```

Ok, then, we need to go deeper into the build process to see exactly where it fails. The built-in builder defines several phases executed in a specific order:  *unpackPhase patchPhase configurePhase buildPhase checkPhase installPhase fixupPhase*. Actually, there are more phases, allowing you more control of what is done before each main phase, but let's keep it simple ;-). Those phases are defined as bash functions into the shell executed when you start nix-build. And guess what, you can go into this shell! It's called *nix-shell* and it creates a completely isolated environment, with all the variables configured depending on the attributes you have put into your derivation.

Let's try it:

```bash
nix-shell --pure ./hello.nix
[nix-shell:~/test]$ 
```

From that point, let's check some interesting things. 

```bash
[nix-shell:~/test]$ echo $out
```

OK, you've got a variable defining the path of the store where your package will be installed! If you write your own builder, you would probably do something like ```./configure --prefix $out```.

```bash
[nix-shell:~/test]$ echo $PATH
```

What a long list! Yes, this path contains directories of packages needed to build something, like for example a GCC compiler.

```bash
[nix-shell:~/test]$ unpackPhase
```

This magically get the source code and unpack it into your current directory!

```bash
[nix-shell:~/test]$ cd $sourceRoot
[nix-shell:~/test/hello-2.1.1]$ patchPhase
[nix-shell:~/test/hello-2.1.1]$ configurePhase
```

Got it? We are executing, phase by phase, the builtin builder.

Note: *For cmake fans, don't worry: if you put cmake into your buildInputs dependencies, the builder provides a cmakeConfigurePhase and cmakeBuildPhase to start the appropriate build process, and of course, you can provide a cmakeFlags attribute*

And this is where things get wrong:

```bash
[nix-shell:~/test/hello-2.1.1]$ buildPhase
```

If you take a look into the ```man``` directory, you'll see the ```help2man``` script starting with a call to ```perl``` which is why we had *perl* as a buildInput dependency. But actually, here the error is that ```help2man``` is not found. I suppose that this script is used as a fallback when no ```help2man``` command is provided by the system. It might be cleaner to provide help2man instead of a full perl dependency.
So, let's add the nix ```help2man``` package as a dependency to check if it may work.

First, clean and exit from the nix-shell 

```bash
[nix-shell:~/test/hello-2.1.1]$ cd ..
[nix-shell:~/test]$ rm -rf hello-2.1.1/
[nix-shell:~/test]$ exit
```

Then, comment out the line you commented earlier, and replace *perl* by *help2man*:

```Nix
{ pkgs ? import <nixpkgs> {} }:
with pkgs;

let
  inherit stdenv fetchurl help2man;
  version = "2.1.1";
in
{
    hello = stdenv.mkDerivation rec {
    name = "hello-${version}";
    buildInputs = [ help2man ];
    hardeningDisable = [ "format" ];
    src = fetchurl {
      url = "ftp://ftp.nluug.nl/pub/gnu/hello/${name}.tar.gz";
      sha256 = "c510e3ad0200517e3a14534e494b37dc0770efd733fc35ce2f445dd49c96a7d5";
    };
  };
}
```

Then build!

```bash
nix-build  ./hello.nix
```

> Summary
>
> * a package is made by writting a *nix expression* into a file
> * *stdenv.mkDerivation* is a powerful function used to create a new package with a lot of possible attributes. See the [Writing Nix Expressions](http://nixos.org/nix/manual/#chap-writing-nix-expressions) part of the Nix documentation for more informations
> * use ```nix-build``` to build your package
> * use ```nix-shell``` to enter into the environment of your package, check, debug and build manually

# How to add a package to nixpkgs

> In the previous section, you learned how to create what we call (here at the Gricad team) a *local package*. That's a package that is based on the available nixpkgs distribution of your system Nix installation. We will now see how, with very minor differences, a such package could be integrated into the official nixpkgs repository.

## Get a local copy of the nixpkgs tree

We've seen earlier that the packages are described into files located in a directory pointed by the current channel. You can directly get the content of the latest version of this directory by cloning the nixpkgs git repository of NixOS: 

```
$ git clone git://github.com/NixOS/nixpkgs.git

Initialized empty Git repository in /home/rochf/nixpkgs/.git/
```

If this takes too long, you can directly copy your current channel:
```bash
# Alternative solution for this tutorial, preventing git overload...
cp -a ~/.nix-defexpr/channels/nixpkgs/ .
find . -type d -exec chmod 755 {} \; 
```

Then, go to the nixpkgs directory :

```bash
$ cd nixpkgs
```

If you have cloned the Nixos/nixpkgs repository, you should go into a stable branch:
```bash
$ git checkout release-17.03
```

## Find a good place for your package and write a nix expression

You can take a look at the existing Nix expressions in the ```pkgs/``` subtree to see how packages are made. A good start-point is the ```pkgs/top-level/all-packages``` which contains the default calls to all the packages.

For example, if your package is a library, you will probably place it under ```pkgs/development/libraries``` while a monitoring service will be placed under ```pkgs/servers/monitoring```. Let's say your package is called "mylib", then you would create a new ``` pkgs/development/libraries/mylib``` directory.

The nix expression of a package is generally put inside a file called ```default.nix```, so  ```pkgs/development/libraries/mylib/default.nix``` in our example.

Copying the default.nix file of another library and modify it to adapt to your own library, is often a good start.

Once your expression is created, you have to add at least a line into the `pkgs/top-level/all-packages.nix` file to define the call to your package.

For your first package, you may also have to add a line to the `lib/maintainers.nix` file to add your name and e-mail address. You may also have to check the list of available licenses into the `lib/licenses.nix` file.

The [Nixpkgs Contributors Guide](https://nixos.org/nixpkgs/manual/) is the reference you should read to know more about writing Nix packages.


### Example: the "oned" package derivation
Oned is a program which solves the Poisson equation using Jacobi method.

The code is available at [https://www.pdc.kth.se/education/tutorials/mpi/hybrid-lab/oned.c](https://www.pdc.kth.se/education/tutorials/mpi/hybrid-lab/oned.c)

Let's consider the following expression:

```Nix
{ stdenv, fetchurl, openmpi }:

stdenv.mkDerivation rec {
  name = "oned";
  src = fetchurl {
     url = "https://www.pdc.kth.se/education/tutorials/mpi/hybrid-lab/oned.c";
     sha256 = "<HASH_HERE>";
  };

  buildInputs = [ openmpi ];

  builder = builtins.toFile "builder.sh"
  "
  source $stdenv/setup
  mpicc -w -o oned.exe $src
  mkdir $out
  mkdir $out/bin
  cp oned.exe $out/bin
  ";

  meta = {
    description = "JDEV 2017 Nix tutoriel";
    license     = stdenv.lib.licenses.gpl2;
    platforms   = stdenv.lib.platforms.unix;
  };
}
```

A good place for this expression, seems to be : `pkgs/application/science/physics`

```bash
$ mkdir pkgs/applications/science/physics/oned
$ emacs pkgs/applications/science/physics/oned/default.nix
```
First of all, you'll need to compute the SHA-256 hash of your source file, to be sure that your package will always be built from this unique source file. The package built process will put this source file into the NIX store, before actualy building the package. So, to avoid downloading twice, let's use the convenient ```nix-prefetch-url``` command that does the download operation and the hash calculation, both at the same time:

```bash
$ nix-prefetch-url https://www.pdc.kth.se/education/tutorials/mpi/hybrid-lab/oned.c
downloading ‘https://www.pdc.kth.se/education/tutorials/mpi/hybrid-lab/oned.c’... [0/0 KiB, 0.0 KiB/s]
path is ‘/nix/store/iw1xyii9wqb1ly5w95ni7rlwsv4q2pp5-oned.c’
1585yzy1gkg3bxfg19mh3ag1x7yik2h3lg5kz705d3jk9dhjg03b

```

Or, in case you have already downloaded the source code, use the `sha256sum` command:

```bash
sha256sum oned.c
```
Place this hash into the expression, in place of *```<HASH_HERE>```*.

Regarding the expression, an important attribute is `buildInputs` that defines a set of Nix packages dependencies for package build. You may also use `propagatebuildInputs` for the dependencies that also need to be present at runtime.

In this example, we have provided our own build script into a "builder" block, because configure and Makefile are not provided. The builder starts with ```source $stdenv/setup``` to setup the environment and process the buidInputs.
This also set up the ```$out``` variable that gives the location of the package under the Nix store.

Generally, the last part of the expression contains a list of meta attributes.
Meta attributes contain informations about the package, such a description, license, the reference of the maintainer,.... Check the [documentation of meta attributes](http://nixos.org/nixpkgs/manual/#chap-meta) for more information.

Once your expression is written, you have to declare the package in the list of packages :

```bash
emacs ~/nixpkgs/pkgs/top-level/all-packages.nix
```

Add the following line (in the SCIENCE zone, with respect of the alphabetical order) :

`oned = callPackage ../applications/science/physics/oned  { };`

### Another derivation for oned

Here is another example for the same programm, but this time with sources including a standard building process (configure, make, make install) provided as a github repository, using the useful ```fetchgit``` function. So, this time, we do not provide any custom builder, but use the generic one of stdenv.

```Nix
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

## Building and installing the Package


The build process is started with the nix-build command:
```
$ nix-build -A oned
```

This ```nix-build -A``` command uses the attribute path ```oned``` (that you defined into the ```all-packages.nix``` file), to find the derivation and build the package with some eventual options.

As seen earlier with the hello package, the built package is located in the store, in the subdirectory pointed by the ```./result``` link. 

You can check that all the dynamically loaded libraries are inside the /nix/store directory:

```
$ ldd ./result/bin/oned.exe
```

Test the executable :

```
$ oned.exe
bash: oned.exe : command not found
```

The oned program is not available. Your environment path is not yet ready, you have to "install" the package.


```
$ nix-env -f . -iA oned
```

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

## Adding your package in the nixpkgs main repository

Read the [Submitting changes part of the Nixpkgs Contributors Guide](https://nixos.org/nixpkgs/manual/#chap-submitting-changes).
Basically, you have now to create a pull request to have it reviewed and merged into the master branch of the nixpkgs repository. Of course, the previous work has to be made into a local branch of your nixpkgs clone.

>    Summary
>
> In this section, we created another package, this time by including it into a local copy of the nixpkgs distribution. We learned how to import files into the store and getting the corresponding hash with the useful command ```nix-prefetch-url```. Further reading of the Nixpkgs contributors guide is necessary to learn more in details how to submit your changes.

## Apendix: Tips

### Contributing
The [CONTRIBUTING.md file](https://github.com/NixOS/nixpkgs/blob/master/.github/CONTRIBUTING.md) contains guidelines for contributing.

### More with nix-shell

```nix-shell``` can also be used to enter into the environment of one or several existing packages, without even installing them, for example:

```bash
nix-shell -p python27 -p python27Packages.numpy
```
opens a shell in an isolated environment which contains python2.7 with the numpy module:
`
```bash
[nix-shell:~]$ python -i
Python 2.7.13 (default, Dec 17 2016, 20:05:07) 
[GCC 5.4.0] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import numpy
>>> 
```
You can even use nix-shell as the shebang of a script:

```
#! /usr/bin/env nix-shell
#! nix-shell -i python27 python27Packages.numpy

import numpy
...
```

### Unfree packages

By default, unfree packages installation is not allowed. We can change this behaviour :

For `nixos-rebuild` you can set

```Nix
{ nixpkgs.config.allowUnfree = true; }
```

in configuration.nix to override this.


For `nix-env`, `nix-build`, `nix-shell` or any other Nix command you can add

```Nix
{ allowUnfree = true; }
```

to your ~/.config/nixpkgs/config.nix.


```bash
$ mkdir .config/nixpkgs

$ emacs .config/nixpkgs/config.nix
```

Here's an example:

```bash
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

### Warnings treated as errors

When compiling the code, some options of the standard environment provided by Nix makes some warnings to be treated as errors. The best thing to do is to create a patch to remove the warning. But, when you don't have the time to fix, this behavior can be changed, adding this line in your derivation:
```
hardeningDisable = [ "format" ];
```
Then, don't forget to make a patch later...


# Nix for HPC (multiuser mode)

> This part is for system administrators, responsible of an HPC cluster. 
>
> If you're interested, please, check this article that describes the operations to set-up Nix on your Linux HPC system:
> * [NIX on HPC platforms](https://gricad.github.io/calcul/nix/hpc/2017/05/15/nix-on-hpc-platforms.html)

# Authors
This tutorial is the result of a long labour by:
* Frederic Audra
* Philippe Beys
* Bruno Bzeznik
* Franck Perignon
* Francoise Roch
* Laure Tavard

Many thanks also to our testers:
* Pierre-Antoine Bouttier
* Romain Cavagna
* Glenn Cougoulat
* Oliver Henriot
* Albanne Lecointre

If you want to contact us: [gricad-contact at univ-grenoble-alpes.fr](mailto:gricad-contact@univ-grenoble-alpes.fr)
