#!/usr/bin/env python3
"""Generate a bcrypt hash for ADMIN_PASSWORD_HASH.

Usage:
  python3 scripts/blog-admin-hash.py
  # type your password (hidden), get the hash to paste in .env
"""
import getpass
import sys

try:
    import bcrypt
except ImportError:
    sys.exit("Run inside the container OR `pip install bcrypt` first.")

pw = getpass.getpass("Admin password: ")
pw2 = getpass.getpass("Repeat: ")
if pw != pw2:
    sys.exit("Passwords don't match.")
if len(pw) < 12:
    sys.exit("Use at least 12 characters.")

hashed = bcrypt.hashpw(pw.encode("utf-8"), bcrypt.gensalt(rounds=12)).decode("ascii")
print("\nPaste this into the backend's .env (escape $ as \\$ in shell quoting):\n")
print(f"ADMIN_PASSWORD_HASH={hashed}")
