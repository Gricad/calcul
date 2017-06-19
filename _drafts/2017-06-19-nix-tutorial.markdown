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



# Nix packages development

## Create a Nix package
(hello.nix)

## Adding a package to <nixpkgs>

### oned
### advanced : hypre
### Debug
-k
nix-shell + différentes phases
### Pull request
(lien nix manual)

# Nix for HPC (multiuser mode)
