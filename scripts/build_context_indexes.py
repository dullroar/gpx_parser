#!/usr/bin/env python3
"""Keep the original index command available.

Run me when: I use the original index command. It runs build_indexes.py.

Usage: build_context_indexes.py [--check] [ROOT]
"""
import sys

from build_indexes import main


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
