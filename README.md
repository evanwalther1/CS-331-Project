# CS-331-Project
Name: Brandon Chacon

## Password authentication demo

This repository includes a small Flask example that lets you register, sign in,
and sign out. Passwords are hashed with Werkzeug before being stored in the
local `users.db` SQLite database; plaintext passwords are never saved.

To run it:

```bash
python -m pip install -r requirements.txt
python app.py
```

Open <http://127.0.0.1:5000> in your browser. The demo requires passwords to be
at least 8 characters long. It generates a temporary session key when
`FLASK_SECRET_KEY` is not set, so sessions end when the app restarts.

This is an educational, local-only example, not production-ready authentication.
Before deploying an authentication system, add protections such as CSRF
prevention, HTTPS, rate limiting, and a securely managed persistent secret key.