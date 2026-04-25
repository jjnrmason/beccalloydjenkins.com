#!/usr/bin/env python3
"""
Generates wwwroot/images/manifest.json from metadata.json + actual folder contents.
Run automatically by MSBuild before each build.
"""

import json
import os
import re
import sys

IMAGES_DIR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "wwwroot", "images")
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}


def natural_sort_key(name: str) -> list:
    """Sort filenames so image10 comes after image9, not after image1."""
    return [int(c) if c.isdigit() else c.lower() for c in re.split(r"(\d+)", name)]


def main():
    metadata_path = os.path.join(IMAGES_DIR, "metadata.json")
    manifest_path = os.path.join(IMAGES_DIR, "manifest.json")

    with open(metadata_path, encoding="utf-8") as f:
        metadata = json.load(f)

    manifest = []
    for folder in metadata:
        name = folder["name"]
        folder_path = os.path.join(IMAGES_DIR, name)

        if not os.path.isdir(folder_path):
            print(f"Warning: folder not found, skipping: {folder_path}", file=sys.stderr)
            continue

        images = sorted(
            [
                entry.name
                for entry in os.scandir(folder_path)
                if entry.is_file()
                and os.path.splitext(entry.name)[1].lower() in IMAGE_EXTENSIONS
                and not entry.name.lower().startswith("thumbnail")
            ],
            key=natural_sort_key,
        )

        manifest.append(
            {
                "name": name,
                "title": folder["title"],
                "thumbnail": folder["thumbnail"],
                "images": images,
            }
        )

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"Manifest written to {manifest_path} ({len(manifest)} folders)")


if __name__ == "__main__":
    main()
