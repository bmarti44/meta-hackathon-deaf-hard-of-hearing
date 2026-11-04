#!/usr/bin/env bash
# Packages the Muse API Lambda: index.mjs + knowledge.json (no secrets; the AWS SDK comes from the runtime).
set -euo pipefail
cd "$(dirname "$0")"
/tmp/gen9env/bin/python build_knowledge.py
cp index.mjs build/
(cd build && rm -f ../lambda.zip && zip -qr ../lambda.zip index.mjs knowledge.json)
echo "built api/lambda.zip"
