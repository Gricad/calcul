---
layout: post
title:  "Nix tutorial"
author: calcul-team
categories: Nix
---

Here comes the Nix tutorial

# How to install Nix package manager :
## Install Nix (single user mode)
From a basic environment (you will need **_bash_**, **_sudo_** and **_curl_** installed), you just have to enter the following command :
{% highlight bash %}
bash <(curl https://nixos.org/nix/install)
{% endhighlight %}
**Nota** : If you don't have sudo installed or if you're not a sudoer, you have to execute this command as root :
{% highlight bash %}
mkdir -m 0755 /nix && chown your_login /Nix
{% endhighlight %}

From this point, you should see something like this :

{% highlight bash %}
bash <(curl https://Nixos.org/Nix/install)
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

The Nix package manager is now installed on your system.

It only populates these two directories :
`/nix` and `~/.nix-profile/`.

## Uninstall Nix
You can easily uninstall Nix from your system typing :
{% highlight bash %}
sudo rm -rf /nix
rm -rf ~/.nix-profile
{% endhighlight %}

# Using Nix
## Activate your Nix environment

To use your new Nix environment, you have to activate it typing :
{% highlight bash %}
source ~/.nix-profile/etc/profile.d/nix.sh
{% endhighlight %}
## List installed packages

The main command to manage packages with Nix is `nix-env`. You can list all installed packages in your current nix-profile with :
{% highlight bash %}
nix-env -q
{% endhighlight %}
At the beginning, you should see this (only one package is installed : Nix).
{% highlight bash %}
nix-1.11.9
{% endhighlight %}

## Search for packages
There are many packages available via Nix, you can search a package typing :
{% highlight bash %}
nix-env -qaP | grep the_package_you-re_searching_for
{% endhighlight %}

## Install packages
Once you've find the package name you want to install, you can do it with the following option :
{% highlight bash %}
nix-env -i the_package_you-re_searching_for
{% endhighlight %}

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
