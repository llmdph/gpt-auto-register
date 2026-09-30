#!/usr/bin/env python3
"""Seed CF temp mail + Sub2API(codex group only) config into webui SQLite."""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from webui import db  # noqa: E402


def _b(name: str, default: str = "") -> str:
    return (os.getenv(name) or default).strip()


def main() -> None:
    db.init_db()

    mail = {
        "mail_source": "cf_temp",
        "cf_api_url": _b("CF_API_URL", "https://temp-api.llmdph.site"),
        "cf_domain": _b("CF_DOMAIN", "llmdph.site"),
        "cf_admin_token": _b("CF_ADMIN_TOKEN") or _b("ADMIN_PASSWORD"),
    }
    if not mail["cf_admin_token"]:
        raise SystemExit("missing CF_ADMIN_TOKEN/ADMIN_PASSWORD")
    db.save_mail_config(mail)

    export = {
        "cpa_enabled": "0",
        "sub2api_enabled": "1",
        "sub2api_url": _b("SUB2API_URL", "http://127.0.0.1:8080"),
        "sub2api_api_key": _b("SUB2API_API_KEY"),
        "sub2api_group_ids": _b("SUB2API_GROUP_IDS", "6"),  # codex
        "sub2api_timeout": _b("SUB2API_TIMEOUT", "30"),
    }
    if not export["sub2api_api_key"]:
        raise SystemExit("missing SUB2API_API_KEY")
    db.save_export_config(export)

    # default proxy for UI convenience
    proxy = _b("PROXY", "http://127.0.0.1:40080")
    if proxy:
        db.set_setting("default_proxy", proxy)

    print("mail:", {k: ("***" if "token" in k else v) for k, v in db.get_mail_config().items()})
    exp = db.get_export_config()
    print("export:", exp)
    print("internal sub2 enabled:", db.get_export_internal_config()["sub2api"]["enabled"],
          "groups:", db.get_export_internal_config()["sub2api"]["sub2api_group_ids"])
    print("proxy default:", db.get_setting("default_proxy", ""))


if __name__ == "__main__":
    main()
