#!/usr/bin/env python3
"""
Deploy the generated archive site to the GitHub Pages repository.

V8.2 Final Stable Version:
- Content-level deployment control (Blogger feed hash)
- Build-level deployment control
- Fully automated safe deployment pipeline
"""

import shutil
import subprocess
import sys
from pathlib import Path
import hashlib
import json


# =========================================================
# PATHS
# =========================================================

ROOT = Path(__file__).resolve().parent
BUILD_DIR = ROOT / "build"
DEPLOY_DIR = ROOT.parent / "tengkongworld.github.io"

FEED_STATE = ROOT / ".feed_state.json"
STATE_FILE = ROOT / ".deploy_state.json"

REQUIRED_MANUAL_DATA = (
    BUILD_DIR / "data" / "homepage.json",
    BUILD_DIR / "data" / "homepage_tc.json",
)


# =========================================================
# UTIL
# =========================================================


def run(command, cwd=ROOT):
    print("+", " ".join(command))
    subprocess.run(command, cwd=cwd, check=True)


# =========================================================
# SAFETY CHECKS
# =========================================================


def ensure_deploy_repo():
    if not DEPLOY_DIR.exists():
        raise SystemExit(f"Deployment repository not found: {DEPLOY_DIR}")

    if not (DEPLOY_DIR / ".git").exists():
        raise SystemExit(f"Deployment target is not a git repo: {DEPLOY_DIR}")


def ensure_manual_homepage_data():
    missing = [p for p in REQUIRED_MANUAL_DATA if not p.exists()]
    if missing:
        raise SystemExit(
            "Missing manual homepage files:\n" + "\n".join(str(p) for p in missing)
        )


# =========================================================
# V8.2: CONTENT LAYER (Blogger)
# =========================================================


def get_articles_hash():
    file = BUILD_DIR / "data" / "articles.json"
    if not file.exists():
        return ""

    return hashlib.md5(file.read_bytes()).hexdigest()


def should_run_sync():
    current = get_articles_hash()

    if FEED_STATE.exists():
        last = json.loads(FEED_STATE.read_text()).get("hash")
    else:
        last = None

    if current == last:
        print("No Blogger changes → skip pipeline")
        return False

    FEED_STATE.write_text(json.dumps({"hash": current}))
    return True


# =========================================================
# V8.1: BUILD LAYER
# =========================================================


def hash_build():
    h = hashlib.md5()

    if not BUILD_DIR.exists():
        return ""

    for p in sorted(BUILD_DIR.rglob("*")):
        if p.is_file():
            h.update(p.name.encode())
            h.update(p.read_bytes())

    return h.hexdigest()


def should_deploy():
    current = hash_build()

    if STATE_FILE.exists():
        last = json.loads(STATE_FILE.read_text()).get("hash")
    else:
        last = None

    if current == last:
        print("No build changes → skip deploy")
        return False

    STATE_FILE.write_text(json.dumps({"hash": current}))
    return True


# =========================================================
# DEPLOY PIPELINE
# =========================================================


def reset_deploy_repo():
    run(["git", "fetch", "origin"], cwd=DEPLOY_DIR)
    run(["git", "checkout", "main"], cwd=DEPLOY_DIR)
    run(["git", "reset", "--hard", "origin/main"], cwd=DEPLOY_DIR)
    run(["git", "clean", "-fdx"], cwd=DEPLOY_DIR)


def clean_deploy():
    for item in DEPLOY_DIR.iterdir():
        if item.name == ".git":
            continue
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()


def copy_build():
    for item in BUILD_DIR.iterdir():
        if item.name == ".DS_Store":
            continue

        target = DEPLOY_DIR / item.name

        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True)
        else:
            shutil.copy2(item, target)


def commit_push():
    run(["git", "add", "-A"], cwd=DEPLOY_DIR)

    status = subprocess.run(
        ["git", "diff", "--cached", "--quiet"],
        cwd=DEPLOY_DIR,
        check=False,
    )

    if status.returncode == 0:
        print("No deployment changes to commit.")
        return

    run(["git", "commit", "-m", "Auto deploy website"], cwd=DEPLOY_DIR)
    run(["git", "push", "origin", "main"], cwd=DEPLOY_DIR)


# =========================================================
# MAIN (FIXED V8.2 FLOW)
# =========================================================


def main():
    ensure_deploy_repo()
    ensure_manual_homepage_data()

    # 1. Content gate (Blogger)
    if not should_run_sync():
        return

    # 2. Generate content
    run([sys.executable, "scripts/sync.py"], cwd=ROOT)

    # 3. Build gate
    if not should_deploy():
        print("Skip deploy (no build change)")
        return

    # 4. Deploy
    reset_deploy_repo()
    clean_deploy()
    copy_build()
    commit_push()

    print("\nV8.2 Deployment complete.")
    print(f"Source: {ROOT}")
    print(f"Target: {DEPLOY_DIR}")


if __name__ == "__main__":
    main()
