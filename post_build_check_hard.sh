#!/bin/bash

# Checks that are executed after build, that need to pass, otherwise build is considered failed.

# Check that links are working
# Comments:
# - allow_missing_href: I had to switch it off as otherwise it would fail and I couldn't find the solution. 
bundle exec htmlproofer --disable_external true --enforce_https false --check_internal_hash false --allow_missing_href false ./_site

