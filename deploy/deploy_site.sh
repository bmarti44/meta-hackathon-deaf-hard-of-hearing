#!/usr/bin/env bash
# Deploys beforetheimplant.com: Muse API Lambda code + static site (S3 + CloudFront).
# Refuses if anything key-like or the upstream API host is in the browser bundle.
set -euo pipefail
cd "$(dirname "$0")/.."
BUCKET=beforetheimplant-com-site
DIST=E34H0K147DZSC0
if grep -rIlE "(Bearer [A-Za-z0-9._-]{20,}|sk-[A-Za-z0-9]{20,}|META_API_KEY|muse-api-key|api\.meta\.ai)" site >/dev/null 2>&1; then
  echo "Refusing: site bundle references a key or the upstream API: $(grep -rIlE "(Bearer [A-Za-z0-9._-]{20,}|sk-[A-Za-z0-9]{20,}|META_API_KEY|muse-api-key|api\.meta\.ai)" site)"; exit 1
fi
if find site -iname "*.wav" -o -iname "*.mp3" -o -iname "*.flac" -o -iname "*.m4a" | grep -q .; then echo "Refusing: audio files in site/"; exit 1; fi
./api/build_lambda.sh
aws lambda update-function-code --function-name beforetheimplant-muse --zip-file fileb://api/lambda.zip --query LastUpdateStatus --output text
aws lambda wait function-updated --function-name beforetheimplant-muse
aws s3 sync site "s3://$BUCKET" --delete --exclude ".DS_Store" --exclude "tools/*" --exclude "*.py" --exclude "index.html" \
  --cache-control "public, max-age=3600"
aws s3 cp site/index.html "s3://$BUCKET/index.html" --content-type "text/html; charset=utf-8" --cache-control "public, max-age=60"
aws cloudfront create-invalidation --distribution-id "$DIST" --paths "/*" --query Invalidation.Id --output text
echo "deployed"
