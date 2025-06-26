import os
from flask import redirect, render_template, session
from functools import wraps


# Function to display an error message to the user.
def apology(message, code=400):
    """
    Render a custom apology message to the user.

    Args:
        message (str): The error message to display.
        code (int): HTTP status code to return.

    Returns:
        tuple: Rendered apology HTML template and HTTP status code.
    """

    def escape(s):
        """
        Escape special characters in the message to make it safe for HTML.

        Args:
            s (str): The string to escape.

        Returns:
            str: The escaped string.
        """
        for old, new in [
            ("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"), ("%", "~p"),
            ("#", "~h"), ("/", "~s"), ('"', "''")
        ]:
            s = s.replace(old, new)
        return s

    # Render the apology.html template with the escaped message.
    return render_template("apology.html", top=code, bottom=escape(message)), code


# Decorator to require user login for specific routes.
def login_required(f):
    """
    Decorate routes to require login.

    Args:
        f (function): The route function to decorate.

    Returns:
        function: The decorated route function.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if the user is logged in (i.e., has a user_id in the session).
        if session.get("user_id") is None:
            return redirect("/login")  # Redirect to login if not logged in.
        return f(*args, **kwargs)

    return decorated_function
