import os
from cs50 import SQL
from flask_session import Session
from flask import Flask, render_template, request, redirect, session, flash, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required


# Initialize Flask app
app = Flask(__name__,static_folder="static")

# Set secret keys for session security
app.secret_key = "mani1234"
app.secret_key = os.getenv("SECRET_KEY", "default_secret")

# Configure session to use the filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure SQLite database
db = SQL("sqlite:///quiz.db")


# Middleware to prevent caching
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route('/')
def main():
    """Redirects to the login page if the user is not authenticated."""
    if not session:
        return redirect('/login')  # Redirects instead of rendering login.html
    return redirect('/home')  # Redirects to dashboard if logged in

# Route for user login
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()  # Clear any existing session

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Validate input
        if not username or not password:
            return apology("must provide username and password", 403)

        # Query database for username
        users = db.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = users[0] if users else None

        # Check password and username validity
        if not user or not check_password_hash(user["hash"], password):
            return apology("invalid username and/or password", 403)

        # Log in the user
        session["user_id"] = user["id"]
        flash("Logged in successfully!", "success")
        return redirect("/")

    # Display login form if GET request
    return render_template("login.html")


# Route for logging out
@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()  # Clear the user's session
    flash("Logged out successfully!", "info")
    return redirect("/")

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

# Route for user registration
@app.route("/index", methods=["GET", "POST"])
def index():
    """Register a new user"""
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Validate inputs
        if not username:
            return apology("must provide username", 400)
        if not email:
            return apology("must provide email", 400)
        if not password:
            return apology("must provide password", 400)

        # Insert user into the database
        try:
            db.execute("INSERT INTO users (username, email, hash) VALUES (?, ?, ?)",
                       username, email, generate_password_hash(password))
        except ValueError:
            return apology("username already exists", 400)
        print("bug")
        # Redirect to login after successful registration
        return redirect("/login")
    else:
        return render_template("index.html")


# Homepage route
@app.route("/home")
@login_required
def home():
    return render_template("home.html")


# Run the application
if __name__ == "__main__":
    app.run(debug=True)
