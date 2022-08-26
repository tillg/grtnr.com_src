#!/bin/bash

# Checks that are executed after build, that need to pass, otherwise build is considered failed.

# Check that links are working
bundle exec htmlproofer --disable_external true --enforce_https false --check_internal_hash false --allow_missing_href true ./_site