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

Basically, this scripts:
 - sets the PATH to nix tools binaries
 - sets the NIX_PATH variable, that may be necessary for some advanced operations and the use of a custom channel. We'll see this later...
 - initializes per-user directories and configuration files
 - sets the NIX_REMOTE variable that is necessary to use the NIX daemon 

Put this file in a convenient place for your users, into a shared directory that is visible from all of your computing nodes and head nodes. For us, it is ``/applis/site/nix.sh``. 

Our users are told to do this, in order to load NIX:

{% highlight bash %}
  source /applis/site/nix.sh
{% endhighlight %}

## Starting the NIX daemon
The daemon must be started as root, after loading the Nix environment multiuser script:
{% highlight bash %}
  luke:~# source /applis/site/nix.sh
  luke:~# nohup nix-daemon&
{% endhighlight %}

Of course, you'll have to place this into a startup-script in a convenient place for your distribution.


## Testing
Now, you should be able to use Nix as a simple user from the head node running the daemon. Let's do some basic operations:
{% highlight bash %}
  bzizou@luke:~$ source /applis/site/nix.sh
  bzizou@luke:~$ nix-env -q aalib
  aalib-1.4rc5
  installing ‘aalib-1.4rc5’
  download-from-binary-cache.pl: still waiting for ‘https://cache.nixos.org/klbqigpkmfss2bag72dfgwgxrraybyc1.narinfo’ after 5 seconds...
  these paths will be fetched (0.11 MiB download, 0.36 MiB unpacked):
    /nix/store/2sgwjml2slrxmzc3n2dz59903dx73cg3-aalib-1.4rc5-doc
    /nix/store/3xfhfx3172g1yrwi3f4i6bpv5xiishch-aalib-1.4rc5-dev
    /nix/store/cb0ajb1njd0lx7yfzslqcz0gnl0xwyks-aalib-1.4rc5-bin
    /nix/store/klbqigpkmfss2bag72dfgwgxrraybyc1-aalib-1.4rc5
  fetching path ‘/nix/store/2sgwjml2slrxmzc3n2dz59903dx73cg3-aalib-1.4rc5-doc’...
  
  *** Downloading ‘https://cache.nixos.org/nar/06i5r8w2c86w3bb27kajpkfr82d0jh60iqzhx1cdrgpim1l2wilk.nar.xz’ to ‘/nix/store/2sgwjml2slrxmzc3n2dz59903dx73cg3-aalib-1.4rc5-doc’...
    % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                   Dload  Upload   Total   Spent    Left  Speed
  100 67900  100 67900    0     0  29073      0  0:00:02  0:00:02 --:--:-- 29066
  
  fetching path ‘/nix/store/klbqigpkmfss2bag72dfgwgxrraybyc1-aalib-1.4rc5’...
  
  *** Downloading ‘https://cache.nixos.org/nar/1qvyszrby2y8dmvzf1qjbvm247kqgwryc9fxfxmx6f5x4cjj73yg.nar.xz’ to ‘/nix/store/klbqigpkmfss2bag72dfgwgxrraybyc1-aalib-1.4rc5’...
    % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                   Dload  Upload   Total   Spent    Left  Speed
  100 31556  100 31556    0     0  14013      0  0:00:02  0:00:02 --:--:-- 14018
  
  fetching path ‘/nix/store/cb0ajb1njd0lx7yfzslqcz0gnl0xwyks-aalib-1.4rc5-bin’...
  
  *** Downloading ‘https://cache.nixos.org/nar/1wr6xbflv433xkzqkzb69yiz58aslbqwwzmhvhpd4sw928vw75v1.nar.xz’ to ‘/nix/store/cb0ajb1njd0lx7yfzslqcz0gnl0xwyks-aalib-1.4rc5-bin’...
    % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                   Dload  Upload   Total   Spent    Left  Speed
  100  7724  100  7724    0     0   4240      0  0:00:01  0:00:01 --:--:--  4239
  
  fetching path ‘/nix/store/3xfhfx3172g1yrwi3f4i6bpv5xiishch-aalib-1.4rc5-dev’...
  
  *** Downloading ‘https://cache.nixos.org/nar/1j399cn5h498kvnyfc7h148rrp5afi9kvv26b393l2za4ww6883q.nar.xz’ to ‘/nix/store/3xfhfx3172g1yrwi3f4i6bpv5xiishch-aalib-1.4rc5-dev’...
    % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                   Dload  Upload   Total   Spent    Left  Speed
  100 10480  100 10480    0     0   3733      0  0:00:02  0:00:02 --:--:--  3732
  
  building path(s) ‘/nix/store/67bk6d6pc97x4i21pyd9rq1dj97jrrn1-user-environment’
  created 1254 symlinks in user environment
  bzizou@luke:~$ which aainfo
  /home/bzizou/.nix-profile/bin/aainfo
  bzizou@luke:~$ aainfo |grep version
  AAlib version:1.4
{% endhighlight %}

The installed packages should also be useable from a computing node. Log on a node (probably using your batch scheduler) and do some tests:

{% highlight bash %}
  bzizou@luke45:~$ source /applis/site/nix.sh   
  bzizou@luke45:~$ aainfo |grep version
  AAlib version:1.4
  bzizou@luke45:~$ which aainfo
  /home/bzizou/.nix-profile/bin/aainfo
{% endhighlight %}

## Setting up other head nodes for nix-daemon access through *socat*
The NIX daemon only listen on a Unix socket. There's no TCP socket. So if you have several head nodes, or if you want packages manipulations (installations, compilations, removal,...) possible from the computing nodes, you can set-up a socat tunnel for example:

  # On the same server that is running the nix-daemon:
  nohup socat TCP-LISTEN:4325,bind=172.28.0.2,reuseaddr,fork,range=172.28.0.0/24 UNIX-CLIENT:/var/run/nix/socket &

TBC...

## Setting up a local Nix channel

[nix]: https://nixos.org/nix/ 
[sandervanderburg]: http://sandervanderburg.blogspot.fr/2013/06/setting-up-multi-user-nix-installation.html
[getting_nix]: https://nixos.org/nix/download.html
[env_modules]: http://modules.sourceforge.net/
[nix-multiuser.sh]: https://github.com/Gricad/calcul/blob/master/nix/nix-multiuser.sh
