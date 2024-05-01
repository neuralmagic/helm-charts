#!/bin/bash

set -e -o pipefail

HELM_DOCS_IMAGE_TAG="jnorwood/helm-docs:latest"

docker pull "$HELM_DOCS_IMAGE_TAG"

# From https://stackoverflow.com/a/4774063
REPO_DIR="$( cd -- "$(dirname "$0")/.." >/dev/null 2>&1 ; pwd -P )"

# helm-docs will only reify templates in directories that include Chart.yaml,
# so create some fake Chart.yaml files to leverage helm-docs to reify some
# other templates.

DIRECTORIES_NEEDING_FAKE_CHART_YAML_FILES=$(\
  find $REPO_DIR \
    -name README.md.gotmpl \
    -type f \
    -execdir test ! -f Chart.yaml \; \
    -execdir pwd \; \
)

for DIRECTORY in $DIRECTORIES_NEEDING_FAKE_CHART_YAML_FILES; do
  touch "$DIRECTORY/Chart.yaml"
done

docker run \
  --rm \
  --user $(id -u) \
  --volume "$REPO_DIR:/helm-docs" \
  "$HELM_DOCS_IMAGE_TAG" \
  --document-dependency-values

for DIRECTORY in $DIRECTORIES_NEEDING_FAKE_CHART_YAML_FILES; do
  rm "$DIRECTORY/Chart.yaml"
done
