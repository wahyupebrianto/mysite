#!/usr/bin/env bash
# Local quality gate: build the site exactly like CI does, then check links.
#   bash scripts/check.sh
set -euo pipefail
cd "$(dirname "$0")/.."
JEKYLL_ENV=production bundle exec jekyll build
bundle exec htmlproofer ./_site --disable-external --no-enforce-https
echo "OK: build and internal link check passed."
