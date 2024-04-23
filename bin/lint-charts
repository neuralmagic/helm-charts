#!/bin/bash

# From https://stackoverflow.com/a/4774063
REPO_DIR="$( cd -- "$(dirname "$0")/.." >/dev/null 2>&1 ; pwd -P )"

for CHART in $(find "$REPO_DIR/charts" -mindepth 1 -maxdepth 1 -type d); do
  helm lint "$CHART"
done
