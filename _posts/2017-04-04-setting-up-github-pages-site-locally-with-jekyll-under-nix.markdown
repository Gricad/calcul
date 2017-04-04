---
layout: post
title:  "Setting up your GitHub Pages site locally with Jekyll under NIX"
date:   2017-04-04 10:42:00 +0200
author: bzizou
categories: jekyll nix
---

[Jekyll][jekyll] is a simple tool to create a static blog-aware website starting from plain text files. A blog post may be a simple mardown file with the date in the filename. Jekyll is the recommended tool for hosting a blog on a [Github Page][github-pages]. 

This post is about setting up, on a [Nix][nix] enabled host (NixOS or Nixpkgs), locally your Jekyll site as if it was served by Github, so that you can test your blog posts before commiting.

Here's what I've done to setup Jekyll for github-pages locally on my NiXOS host:

{% highlight bash %}
 # Check my channel
 [bzizou@bart:~/git/gricad.github.io/calcul/blog]$ nix-channel --list
 nixpkgs https://nixos.org/channels/nixpkgs-unstable

 # Start from a fresh profile
 nix-env --switch-profile nix-profiles/github

 # Install Jekyll, Bundler and some deps
 nix-env -i -A nixpkgs.jekyll
 nix-env --set-flag priority 10 jekyll
 nix-env -i -A nixpkgs.bundler nixpkgs.gnumake nixpkgs.ruby nixpkgs.zlib nixpkgs.gcc6 nixpkgs.nodejs

 # Configure gem to install gems in my user environment (if not already done)
 echo "gem: --user-install" > ~/.gemrc

 # Configure bundler
 bundle config build.nokogiri --with-zlib-dir=/home/bzizou/.nix-profile

{% endhighlight %}

Then, follow [Setting up your GitHub Pages site locally with Jekyll][github-page] from the github help pages.

#### Note: not in a subdirectory
I tried to setup a Jekyll blog inside a sub-directory of a github-pages site, but it seems impossible because of errors relative to the `_includes` directory that should be at the root of the site, but should not be outside of the blog directory if it's pointed by a symlink.

[jekyll]: https://jekyllrb.com/
[github-pages]: https://pages.github.com/
[nix]: https://nixos.org/nix/
[github-page]: https://help.github.com/articles/setting-up-your-github-pages-site-locally-with-jekyll
