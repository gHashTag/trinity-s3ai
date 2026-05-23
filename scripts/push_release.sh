#!/bin/bash
# Push the release tag and create GitHub release
set -e

echo "Pushing tag v1.0-wave14 to origin..."
git push origin v1.0-wave14

echo "Creating GitHub release v1.0-wave14..."
gh release create v1.0-wave14 \
  --title "Wave 14 Release" \
  --notes-file RELEASE_NOTES_v1.0-wave14.md

echo "Release v1.0-wave14 created successfully."
echo "Zenodo will automatically generate a DOI within a few minutes."
