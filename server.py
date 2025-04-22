from flask import Flask, send_from_directory, request, jsonify
import re

app = Flask(__name__, static_folder="public")

# In-memory storage for banned users
banned_users = set()

# List of valid UC email domains
valid_domains = [
    "@ucla.edu",      # UCLA
    "@berkeley.edu",  # UC Berkeley
    "@ucsd.edu",      # UC San Diego
    "@uci.edu",       # UC Irvine
    "@ucdavis.edu",   # UC Davis
    "@ucsf.edu",      # UC San Francisco
    "@ucr.edu",       # UC Riverside
    "@ucsc.edu",      # UC Santa Cruz
    "@ucmerced.edu"   # UC Merced
]

# Serve the index.html file for the root URL
@app.route("/")
def serve_index():
    return send_from_directory("public", "index.html")

# Serve other static files (CSS, JS, etc.)
@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory("public", path)

# Validate user details
@app.route("/validate-user", methods=["POST"])
def validate_user():
    data = request.json
    email = data.get("email", "")
    name = data.get("name", "")
    pid = data.get("pid", "")

    # Check if the user is banned
    if email in banned_users:
        return jsonify({"success": False, "message": "You are banned from this site."}), 403

    # Validate UC email
    if not any(email.endswith(domain) for domain in valid_domains):
        return jsonify({"success": False, "message": "Invalid UC email address."}), 400

    # Validate name and PID
    if not name or not pid:
        return jsonify({"success": False, "message": "Name and PID are required."}), 400

    # If validation passes
    return jsonify({"success": True, "message": "Welcome to the chat!"})

# Ban a user (for admin use or automated rule enforcement)
@app.route("/ban-user", methods=["POST"])
def ban_user():
    data = request.json
    email = data.get("email", "")
    if email:
        banned_users.add(email)
        return jsonify({"success": True, "message": f"User {email} has been banned."})
    return jsonify({"success": False, "message": "Email is required to ban a user."}), 400

if __name__ == "__main__":
    app.run(port=3000, debug=True)