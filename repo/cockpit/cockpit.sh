#!/usr/bin/env bash
set -euo pipefail

# podman volume create portainer_data

podman run -d \
  --name cockpit \
  -p 9090:9090 \
  -v portainer_data:/data \
  quay.io/cockpit/ws:latest