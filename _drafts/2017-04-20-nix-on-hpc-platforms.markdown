---
layout: post
title:  "Setting up NIX on a multi-users HPC environment"
author: bzizou
categories: nix hpc
---


## Introduction

*At GRICAD, we provide [NIX][nix] as a reproducible and portable computing environment for the users of our High Performance Computing facilities. This post is about how we've set up our computing clusters for supporting NIX and some custom packages not yet pushed or not to be pushed into the upstream Nixpkgs repository. We succeeded this set-up on 2 different platforms: a BullX one (which is actually CentOS based) and a Debian based one.*

What we call an HPC cluster here, is simply a set of interconnected Linux **computing nodes** and one or several **head nodes**. The computing nodes and the head nodes share some common network filesystems, generally NFS or a more performant solution (Lustre, BeeGFS, ...). Users log on the head nodes and submit jobs on the computing nodes by using a special piece of software generally called a *batch scheduler*. So users have no direct access to the nodes, but may do some interactive tasks for preparing the jobs on the head nodes. 

Regarding this Nix installation:
 - on the head nodes: users may set-up nix profiles, install, compile or create nix packages,... 
 - on the computing nodes: users have just an execution context (no need for access to profile/packages management from the computing nodes).
 - on every nodes: a common Nix store is shared, allowing efficient use of the space occupied by the installed packages, even for the custom packages of a given user that he may share with the others.

As a reference, this **[blog post][sandervanderburg]** helped us a lot.

## The /nix store

One of the most important thing to set-up to allow users to use Nix efficiently is a **``/nix``** directory shared on all the computing and head nodes. This path must be exactly ``/nix`` in order to be able to use the official Nix binary caches. It's possible to install the Nix store in another path, but in this case, every package and it's dependencies will need to be recompiled as the pre-compiled binaries will not be useable. Package recompilation is a task that Nix does very well, on the fly, at installation time; but the problem is that it may require quite a lot of time and resources on the head node.

So, for example, set-up a mount on an NFS filesystem on all of your nodes:
{% highlight bash %}
  # fstab entry for NIX
  luke:/home/nix          /nix    nfs     defaults        0       0
{% endhighlight %}

## Install NIX

The second step is to install the Nix command line tools. Download the source tarball from the [Getting Nix page][getting_nix]. **Don't follow the quick way with the install script**, it's not suitable for a multi-users installation. 

In our computing center, we use [environment modules][env_modules] and a software repository shared on all the nodes into the path ``/applis``. Even if it becomes obsolete if you use Nix, it's not incompatible, so we choose to install the nix tools the same way we install other modules. For example, here's how we did (of course, it will not be suitable for you, and you'll have to adapt to your software environment):

{% highlight bash %}
  module load gcc/4.8.2_gcc-4.4.6
  module load curl/7.47.0_gcc_4.4.6
  cd nix-1.11.4
  echo "GLOBAL_LDFLAGS += -lpthread -Wl,-rpath -Wl,/applis/site/stow/gcc_4.4.6/gcc_4.8.2/lib64" >> doc/manual/local.mk
  ./configure --prefix=/applis/site/stow/gcc_4.8.2/nix_1.11
  make -j8
  make install
{% endhighlight %}

Note that there's no need to make this installation as root. You just have to make the nix binaries available to all of your nodes.

So, as a result, we have working nix tools binaries compiled into the path ``/applis/site/stow/gcc_4.8.2/nix_1.11`` and we make them available with:
 
{% highlight bash %}
  export PATH=/applis/site/stow/gcc_4.8.2/nix_1.11.4/bin:$PATH
{% endhighlight %}

Then, try a simple test:

{% highlight bash %}
  [bzizou@froggy1 ~]$ nix-env --version
  nix-env (Nix) 1.11.4
{% endhighlight %}

## Create the build users

Nix will allow the users to automatically build (ie compile) the content of the packages. In a multi-users environment, nix provides a daemon that is responsible of the security of the shared nix store. So, the builds and packages installations are not directly done by the users, but by the ``nix-daemon`` which is using common anonymous users. This principle also allows you (as the system administrator) to have some control over the build process, for example if you want to limit the number of build processes that can be run at the same time. 

The following steps are to be run as root on a head node. If you have several head nodes for one computing cluster, you'll have to do that only on one of your head nodes. Choose a powerful head node, as it will be the one executing the builds. We'll se later how to allow the other head nodes to interact with the nix-daemon to be able to manage installations and builds (but the builds will always run on the node you configured).

Create a group for the nix build users:
{% highlight bash %}
  groupadd -r nixbld
{% endhighlight %}

Then, create 10  build users (still as root on your master head node):
{% highlight bash %}
  for n in $(seq 1 10)
  do
    useradd -c "Nix build user $n" -d /var/empty -g nixbld -G nixbld -M -N -r -s "$(which nologin)" nixbld$n
  done
{% endhighlight %}

Finally, initiate the configuration file and the store:
{% highlight bash %}
  # Initiate the configuration file
  mkdir /etc/nix
  echo "build-users-group = nixbld" >> /etc/nix/nix.conf
  # Initiate the store directories
  mkdir -p /nix/store
  chgrp nixbld /nix/store
  chmod 1775 /nix/store
  mkdir -p -m 1777 /nix/var/nix/profiles/per-user
  mkdir -p -m 1777 /nix/var/nix/gcroots/per-user
{% endhighlight %}

## The multi-users profile script
To use NIX, your users will have to source a shell script into their environment. Here is a simple [nix-multiuser.sh][nix-multiuser.sh] based on the one we are currently using. You might have to add/customize some environement variables.

## Starting the daemon
TBC...

## Testing

## Setting up other head nodes for nix-daemon access through *socat*

## Setting up a local Nix channel

[nix]: https://nixos.org/nix/ 
[sandervanderburg]: http://sandervanderburg.blogspot.fr/2013/06/setting-up-multi-user-nix-installation.html
[getting_nix]: https://nixos.org/nix/download.html
[env_modules]: http://modules.sourceforge.net/
[nix-multiuser.sh]: https://github.com/Gricad/calcul/blob/master/nix/nix-multiuser.sh
