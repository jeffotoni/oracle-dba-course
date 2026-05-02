#!/usr/bin/env bash
set -euo pipefail

podman run -d \
  --name cloudbeaver \
  -p 8978:8978 \
  --restart=always \
  -v cloudbeaver-data:/opt/cloudbeaver/workspace \
  dbeaver/cloudbeaver:24.3.0
