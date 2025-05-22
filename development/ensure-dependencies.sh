#!/bin/bash

DEPS=("python3.9" "poetry")

COLOR_RED='\033[0;31m'
COLOR_YELLOW='\033[1;33m'
COLOR_NC='\033[0m' # No Color

echo "Verifying required dependencies"
echo ""

for d in "${DEPS[@]}"; do
  if [ -n "$(which "$d")" ]; then
    printf "   %-25s: installed\n" $d
  else
    printf "   %-25s: %b\n" $d "${COLOR_RED}NOT INSTALLED${COLOR_NC}"
    exit 1
  fi
done

echo ""
echo "All dependencies installed"
