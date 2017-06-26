---
layout: post
title:  "Posting into this blog"
date:   2017-04-04 12:24:00 +0200
author: bzizou
categories: jekyll
---

[Jekyll][jekyll] is a simple tool to create a static blog-aware website starting from plain text files. A blog post may be a simple mardown file with the date in the filename. Jekyll is the recommended tool for hosting a blog on a [Github Page][github-pages]. 

This post is about publishing a new article into this blog.

* First of all, you need a github account and access as a developper into the [Gricad organization][gricad-org]. Please, contact either [Bzizou][bzizou], [Alpitux][alpitux] or [Ltavard][ltavard].
* Clone the gricad/calcul repository:
`git clone https://github.com/Gricad/calcul.git`
* To create a new article, simply create a new file into `_posts`. You can check the other posts to get examples. The filename must start with the date in the format [YYYY-MM-DD].
* Commit your changes and push into the master branch to get your post published.
* It's better to test and check before commiting, so, [follow this help page][testing_localy] or [this post][testing_localy_nix] if you are using Nix.

Shortly, for testing:
  * Install ruby if not already installed
  * `gem install bundler`
  * `cd <repository_of_the_blog>`
  * `bundle install`
  * `bundle exec jekyll serve` 
* You can create drafts into `_drafts`  (optionnaly with a publish date in the futur) and watch the drafts with:
`bundle exec jekyll serve --draft --futur`

[jekyll]: https://jekyllrb.com/
[github-pages]: https://pages.github.com/
[gricad-org]: https://github.com/Gricad
[bzizou]: https://github.com/bzizou
[alpitux]: https://github.com/alpitux
[ltavard]: https://github.com/ltavard
[testing_localy]: https://help.github.com/articles/setting-up-your-github-pages-site-locally-with-jekyll
[testing_localy_nix]: https://gricad.github.io/calcul/jekyll/nix/2017/04/04/setting-up-github-pages-site-locally-with-jekyll-under-nix.html
