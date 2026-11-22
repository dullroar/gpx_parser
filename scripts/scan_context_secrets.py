#!/usr/bin/env python3
"""Keep the original secret scan command available.

Run me when: I use the original secret scan command. It runs scan_secrets.py.

Usage: scan_context_secrets.py [ROOT]
"""
import sys

from scan_secrets import main


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
