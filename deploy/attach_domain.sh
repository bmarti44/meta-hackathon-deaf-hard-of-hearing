#!/usr/bin/env bash
# Once the ACM cert is ISSUED: put beforetheimplant.com + www on the distribution and point Route 53 at it.
set -euo pipefail
DIST=E34H0K147DZSC0; ZONE=Z031443727CBVQM2UB5R
CERT=arn:aws:acm:us-east-1:087630439073:certificate/91ad1661-3ba0-409d-8b92-2c9779fb6742
TMP=$(mktemp -d)
[ "$(aws acm describe-certificate --region us-east-1 --certificate-arn $CERT --query Certificate.Status --output text)" = ISSUED ] || { echo "cert not issued yet"; exit 2; }
aws cloudfront get-distribution-config --id $DIST --output json > $TMP/dc.json
python3 - "$TMP" "$CERT" <<'PY'
import json, sys
t, cert = sys.argv[1], sys.argv[2]; d = json.load(open(f"{t}/dc.json")); c = d["DistributionConfig"]
c["Aliases"] = {"Quantity": 2, "Items": ["beforetheimplant.com", "www.beforetheimplant.com"]}
c["ViewerCertificate"] = {"ACMCertificateArn": cert, "SSLSupportMethod": "sni-only", "MinimumProtocolVersion": "TLSv1.2_2021", "Certificate": cert, "CertificateSource": "acm"}
json.dump(c, open(f"{t}/new.json", "w")); open(f"{t}/etag", "w").write(d["ETag"])
PY
aws cloudfront update-distribution --id $DIST --if-match "$(cat $TMP/etag)" --distribution-config file://$TMP/new.json --query Distribution.Status --output text
CF=$(aws cloudfront get-distribution --id $DIST --query Distribution.DomainName --output text)
python3 - "$CF" > $TMP/rr.json <<'PY'
import json, sys
cf = sys.argv[1]
ch = [{"Action": "UPSERT", "ResourceRecordSet": {"Name": n, "Type": t, "AliasTarget": {"HostedZoneId": "Z2FDTNDATAQYW2", "DNSName": cf, "EvaluateTargetHealth": False}}}
      for n in ("beforetheimplant.com.", "www.beforetheimplant.com.") for t in ("A", "AAAA")]
print(json.dumps({"Comment": "site -> CloudFront", "Changes": ch}))
PY
aws route53 change-resource-record-sets --hosted-zone-id $ZONE --change-batch file://$TMP/rr.json --query ChangeInfo.Status --output text
echo "domain attached"
