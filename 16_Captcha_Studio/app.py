"""
Flask web demo:  python app.py   ->  http://127.0.0.1:5000

Endpoints
---------
GET  /                         web page with the CAPTCHA form
POST /api/captcha              {"difficulty": "hard", "mode": "text"}  -> new challenge (JSON)
GET  /api/captcha/<id>.png     the challenge image
GET  /api/captcha/<id>.wav     audio version (numeric challenges, needs `pip install captcha`)
POST /api/verify               {"id": "...", "answer": "..."}  -> verification result
GET  /api/stats                counters (issued / passed / failed / expired)
"""

from __future__ import annotations

import os

from flask import Flask, Response, abort, jsonify, render_template, request

from captcha_studio import (AudioCaptchaGenerator, CaptchaManager, RateLimitError,
                            VerifyResult, audio_available)

app = Flask(__name__)
secret = os.environ.get("CAPTCHA_SECRET")
manager = CaptchaManager(secret_key=secret.encode() if secret else None,
                         ttl_seconds=120, max_attempts=3)
_images: dict[str, bytes] = {}      # id -> PNG (kept only while the challenge is alive)
_audio = AudioCaptchaGenerator() if audio_available() else None


@app.get("/")
def index():
    return render_template("index.html", audio=_audio is not None)


@app.post("/api/captcha")
def new_captcha():
    body = request.get_json(silent=True) or {}
    try:
        ch = manager.issue(body.get("difficulty", "medium"), body.get("mode", "text"),
                           client_id=request.remote_addr)
    except RateLimitError as e:
        return jsonify(error=str(e)), 429
    except ValueError as e:
        return jsonify(error=str(e)), 400
    # drop images whose challenge no longer exists
    for k in [k for k in _images if manager.attempts_left(k) == 0]:
        _images.pop(k, None)
    _images[ch.id] = ch.image_png
    return jsonify(id=ch.id, image=f"/api/captcha/{ch.id}.png",
                   audio=f"/api/captcha/{ch.id}.wav" if (_audio and ch.audio_digits) else None,
                   expires_in=manager.ttl, attempts=manager.max_attempts)


@app.get("/api/captcha/<cid>.png")
def captcha_image(cid: str):
    png = _images.get(cid)
    if png is None:
        abort(404)
    return Response(png, mimetype="image/png", headers={"Cache-Control": "no-store"})


@app.get("/api/captcha/<cid>.wav")
def captcha_audio(cid: str):
    digits = manager.audio_digits(cid)
    if not (_audio and digits):
        abort(404)
    return Response(_audio.generate_bytes(digits), mimetype="audio/wav",
                    headers={"Cache-Control": "no-store"})


@app.post("/api/verify")
def verify():
    body = request.get_json(silent=True) or {}
    cid, answer = body.get("id", ""), body.get("answer", "")
    result = manager.verify(cid, answer)
    if result is not VerifyResult.WRONG:
        _images.pop(cid, None)
    messages = {
        VerifyResult.OK: "Verified - you are human!",
        VerifyResult.WRONG: f"Wrong answer. {manager.attempts_left(cid)} attempt(s) left.",
        VerifyResult.EXPIRED: "This CAPTCHA expired. Load a new one.",
        VerifyResult.NOT_FOUND: "Unknown or already-used CAPTCHA. Load a new one.",
        VerifyResult.TOO_MANY_ATTEMPTS: "Too many wrong attempts. Load a new one.",
    }
    return jsonify(result=result.value, success=result is VerifyResult.OK,
                   message=messages[result], attempts_left=manager.attempts_left(cid))


@app.get("/api/stats")
def stats():
    return jsonify(manager.stats | {"active": len(manager)})


if __name__ == "__main__":
    app.run(debug=True)
