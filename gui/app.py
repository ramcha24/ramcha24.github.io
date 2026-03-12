"""
Local GUI server for editing the academic website.
Run: python app.py  →  open http://localhost:5001
"""

import os, re, shutil, subprocess, json
from datetime import datetime, date
from pathlib import Path
from flask import Flask, render_template, request, jsonify

import frontmatter

app = Flask(__name__)

REPO_ROOT   = Path(__file__).parent.parent
CONTENT_DIR = REPO_ROOT / "content"
PUB_DIR     = CONTENT_DIR / "publication"
ADMIN_FILE  = CONTENT_DIR / "authors" / "admin" / "_index.md"
NEWS_FILE   = CONTENT_DIR / "newslist.dat"
UPLOADS_DIR = REPO_ROOT / "static" / "uploads"

hugo_proc = None


# ── helpers ──────────────────────────────────────────────────────────────────

def _serialize(obj):
    """Make frontmatter metadata JSON-serializable."""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {k: _serialize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_serialize(i) for i in obj]
    return obj


def _load(path):
    post = frontmatter.load(str(path))
    return post


def _save(path, post):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(frontmatter.dumps(post))


# ── profile ───────────────────────────────────────────────────────────────────

@app.route("/api/profile", methods=["GET"])
def get_profile():
    post = _load(ADMIN_FILE)
    return jsonify({"metadata": _serialize(dict(post.metadata)), "content": post.content})


@app.route("/api/profile", methods=["POST"])
def save_profile():
    data = request.json
    post = _load(ADMIN_FILE)
    for k, v in data.get("metadata", {}).items():
        post[k] = v
    post.content = data.get("content", post.content)
    _save(ADMIN_FILE, post)
    return jsonify({"ok": True})


# ── publications ──────────────────────────────────────────────────────────────

@app.route("/api/publications", methods=["GET"])
def list_pubs():
    pubs = []
    for folder in sorted(PUB_DIR.iterdir()):
        idx = folder / "index.md"
        if idx.exists():
            post = _load(idx)
            pubs.append({
                "id":               folder.name,
                "title":            post.get("title", folder.name),
                "date":             _serialize(post.get("date", "")),
                "publication":      post.get("publication", ""),
                "publication_short": post.get("publication_short", ""),
                "featured":         post.get("featured", False),
                "publication_types": post.get("publication_types", ["0"]),
            })
    pubs.sort(key=lambda x: x["date"] or "", reverse=True)
    return jsonify(pubs)


@app.route("/api/publications/<pub_id>", methods=["GET"])
def get_pub(pub_id):
    idx = PUB_DIR / pub_id / "index.md"
    post = _load(idx)
    meta = _serialize(dict(post.metadata))
    # Normalize authors to newline-separated string for the textarea
    authors = meta.get("authors", [])
    if isinstance(authors, list):
        meta["authors"] = "\n".join(authors)
    return jsonify({"metadata": meta, "content": post.content})


@app.route("/api/publications", methods=["POST"])
def create_pub():
    data = request.json
    meta = dict(data.get("metadata", {}))
    _coerce_pub_meta(meta)

    title = meta.get("title", "new-publication")
    date_val = str(meta.get("date", str(datetime.now().year)))[:7]
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", title).strip("-")[:40]
    folder_name = f"{date_val}-{slug}"
    folder = PUB_DIR / folder_name
    folder.mkdir(exist_ok=True)

    post = frontmatter.Post(data.get("content", ""), **meta)
    _save(folder / "index.md", post)
    return jsonify({"ok": True, "id": folder_name})


@app.route("/api/publications/<pub_id>", methods=["PUT"])
def update_pub(pub_id):
    data = request.json
    idx = PUB_DIR / pub_id / "index.md"
    post = _load(idx)
    meta = dict(data.get("metadata", {}))
    _coerce_pub_meta(meta)
    for k, v in meta.items():
        post[k] = v
    post.content = data.get("content", post.content)
    _save(idx, post)
    return jsonify({"ok": True})


@app.route("/api/publications/<pub_id>", methods=["DELETE"])
def delete_pub(pub_id):
    folder = PUB_DIR / pub_id
    if folder.is_dir():
        shutil.rmtree(folder)
    return jsonify({"ok": True})


def _coerce_pub_meta(meta):
    """Normalise types coming from the form before writing."""
    # Authors: textarea → list
    if "authors" in meta and isinstance(meta["authors"], str):
        meta["authors"] = [a.strip() for a in meta["authors"].splitlines() if a.strip()]
    # Tags: comma string → list
    if "tags" in meta and isinstance(meta["tags"], str):
        meta["tags"] = [t.strip() for t in meta["tags"].split(",") if t.strip()]
    # publication_types: single string → list
    if "publication_types" in meta and isinstance(meta["publication_types"], str):
        meta["publication_types"] = [meta["publication_types"]]
    # featured: keep as bool
    if "featured" in meta:
        meta["featured"] = bool(meta["featured"])


# ── news ──────────────────────────────────────────────────────────────────────

@app.route("/api/news", methods=["GET"])
def get_news():
    text = NEWS_FILE.read_text(encoding="utf-8")
    items = []
    for line in text.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        m = re.match(r"\*\*\[([^\]]+)\]\*\*\s*(.*)", line)
        if m:
            items.append({"date": m.group(1), "text": m.group(2)})
        else:
            items.append({"date": "", "text": line})
    return jsonify(items)


@app.route("/api/news", methods=["POST"])
def save_news():
    items = request.json
    lines = []
    for item in items:
        d = item.get("date", "").strip()
        t = item.get("text", "").strip()
        if t:
            lines.append(f"**[{d}]** {t}" if d else t)
    NEWS_FILE.write_text("\n\n".join(lines) + "\n", encoding="utf-8")
    return jsonify({"ok": True})


# ── cv upload ─────────────────────────────────────────────────────────────────

@app.route("/api/cv", methods=["POST"])
def upload_cv():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    request.files["file"].save(str(UPLOADS_DIR / "resume.pdf"))
    return jsonify({"ok": True})


# ── hugo preview ──────────────────────────────────────────────────────────────

@app.route("/api/preview/start", methods=["POST"])
def start_preview():
    global hugo_proc
    if hugo_proc and hugo_proc.poll() is None:
        return jsonify({"ok": True})
    hugo_proc = subprocess.Popen(
        ["hugo", "server", "--port=1313", "--bind=127.0.0.1", "--disableFastRender"],
        cwd=str(REPO_ROOT),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return jsonify({"ok": True})


@app.route("/api/preview/stop", methods=["POST"])
def stop_preview():
    global hugo_proc
    if hugo_proc:
        hugo_proc.terminate()
        hugo_proc = None
    return jsonify({"ok": True})


@app.route("/api/preview/status", methods=["GET"])
def preview_status():
    running = hugo_proc is not None and hugo_proc.poll() is None
    return jsonify({"running": running})


# ── git / publish ─────────────────────────────────────────────────────────────

@app.route("/api/git/status", methods=["GET"])
def git_status():
    r = subprocess.run(["git", "status", "--short"], cwd=str(REPO_ROOT), capture_output=True, text=True)
    return jsonify({"status": r.stdout.strip()})


@app.route("/api/publish", methods=["POST"])
def publish():
    data   = request.json or {}
    msg    = data.get("message", f"Update website {datetime.now().strftime('%Y-%m-%d')}")
    output = []

    for cmd in [["git", "add", "-A"], ["git", "commit", "-m", msg], ["git", "push"]]:
        r = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)
        combined = (r.stdout + r.stderr).strip()
        output.append({"cmd": " ".join(cmd), "out": combined, "code": r.returncode})
        # stop on real failure (but "nothing to commit" is harmless)
        if r.returncode != 0 and "nothing to commit" not in combined:
            if cmd[1] in ("add", "push"):
                break

    return jsonify({"output": output})


# ── main ──────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    print("\n  ✦  Academic Website Editor")
    print("  →  Open http://localhost:5001 in your browser\n")
    app.run(port=5001, debug=False)
