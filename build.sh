#!/bin/bash

echo "Building the site in mode $JEKYLL_ENV"

# Building the site
bundle exec jekyll build

## Building with docker
# export JEKYLL_VERSION=4.2.2
# docker run --rm \
#   --volume="$PWD:/srv/jekyll:Z" \
#   -it jekyll/builder:$JEKYLL_VERSION \
#   jekyll build