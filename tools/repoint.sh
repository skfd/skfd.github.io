#!/usr/bin/env bash
# Rewrite references to repos that moved from skfd to an organisation, in one checkout's
# tracked files. Usage: repoint.sh <checkout> ; prints the files it changed.
set -euo pipefail
cd "$1"
ORG=toronto-maps
NAMES='toronto-2-address-import|toronto-addresses-import|toronto-addresses-layer|toronto-open-poi|toronto-parks-layer|toronto-poster-columns-layer|toronto-streets-layer|toronto-streets-osm|toronto-waterways-layer|toronto-import-beholder|toronto-buildings-3d'
git grep -I -l -E "skfd(\.github\.io)?/($NAMES)" -- . | while IFS= read -r f; do
  NAMES="$NAMES" ORG="$ORG" perl -pi -e 's{skfd(\.github\.io)?/($ENV{NAMES})(?![a-z0-9-])}{$ENV{ORG}.($1//"")."/".$2}ge' "$f"
  echo "$f"
done
