#!/bin/bash

# Checks that are executed after build, but that wouldn't fail the entire process.

# Check that links are working
bundle exec htmlproofer ./_site