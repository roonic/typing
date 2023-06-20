from cs50 import SQL
from flask import Flask, redirect, render_template, session, request
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///typing.db")

def apology(message):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", bottom=escape(message))

@app.route("/")
def index():

    if session:
        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        return render_template("index.html", username=rows[0]["username"])
    return render_template("index.html")

@app.route("/stats")
def stats():

    if session:
        user_id = session["user_id"]
        stats = db.execute("SELECT * FROM user_stats WHERE user_id = ?", user_id)
        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        return render_template("stats.html", stats=stats[0], username=rows[0]["username"])
    else:
        return apology("Log In required for stats")


@app.route("/update")
def updatestats():

    if session:
        user_id = session["user_id"]
        stats = db.execute("SELECT * FROM user_stats WHERE user_id = ?", user_id)
        stats = stats[0]

        stats["wpm_last"] = int(request.args.get('wpm'))
        stats["accuracy_last"] = int(request.args.get('acc'))
        stats["test_count"] += 1

        if stats["accuracy_avg"] == 0 and stats["wpm_avg"] == 0:
            stats["wpm_avg"] = stats["wpm_last"]
            stats["accuracy_avg"] = stats["accuracy_last"]
        else:
            stats["wpm_avg"] = (stats["wpm_avg"] + stats["wpm_last"]) / 2
            stats["accuracy_avg"] = (stats["accuracy_avg"] + stats["accuracy_last"]) / 2

        if stats["wpm_best"] < stats["wpm_last"]:
            stats["wpm_best"] = stats["wpm_last"]

        db.execute("UPDATE user_stats SET wpm_avg = ?, wpm_last = ?, wpm_best = ?, accuracy_avg = ?, accuracy_last = ?, test_count = ? WHERE user_id = ?", round(stats["wpm_avg"]), stats["wpm_last"], stats["wpm_best"], round(stats["accuracy_avg"]), stats["accuracy_last"], stats["test_count"], user_id)
        return


@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/logreg")
def logreg():
    return render_template("logreg.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        username = request.form.get("username")
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        # verify from database the input username is unique
        if not username or len(rows) != 0:
            return apology("invalid username")

        password = request.form.get("password")
        if not password or password != request.form.get("confirmation"):
            return apology("password doesn't match")

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, generate_password_hash(password))
        user_id = db.execute("SELECT id FROM users WHERE username = ?", username)
        db.execute("INSERT INTO user_stats (user_id) VALUES (?)", user_id[0]["id"])

        return redirect("/")
