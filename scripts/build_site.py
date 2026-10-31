#!/usr/bin/env python3
"""Copy the publishable site files and generate directory indexes."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from build_directory_indexes import generate_indexes


EXCLUDED_NAMES = {".git", ".github", "__pycache__", "scripts", "_site"}


def ignored_names(_: str, names: list[str]) -> set[str]:
    return set(names) & EXCLUDED_NAMES


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build a static site artifact from a repository checkout."
    )
    parser.add_argument("source", type=Path, help="repository directory to publish")
    parser.add_argument("destination", type=Path, help="directory for the site artifact")
    args = parser.parse_args()

    source = args.source.resolve()
    destination = args.destination.resolve()
    if not source.is_dir():
        parser.error(f"source does not exist or is not a directory: {source}")
    if destination.exists():
        shutil.rmtree(destination)

    shutil.copytree(source, destination, ignore=ignored_names)
    generate_indexes(destination)


if __name__ == "__main__":
    main()
