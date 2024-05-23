import os

from datetime import datetime
from flask import Flask, redirect, render_template, request, session, flash
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.secret_key = "xin loi moi nguoi luc do minh tre trau qua..."
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///users.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    #check session user 
    if session.get("user_id") is None:
            return redirect("/login")
    else:
        # show date time
        time = datetime.now()
        day_of_week = time.strftime("%A")
        month = time.strftime("%B")
        day_time = time.strftime(f"{day_of_week}, {month}, %d, %Y")
        
        # User reached route via POST (as by submitting a form via POST)
        if request.method == "POST":
            # Ensure diary today was submitted   
            today = request.form.get("today")
            if not today:
                # message if not submit
                flash("You need to write something so you can save it !", "infor")
                return render_template("index.html", day_time=day_time)
            # Query database for insert new dairy 
            db.execute("INSERT INTO diary_time (user_id, text) VALUES (?, ?)", session["user_id"], today)
            return render_template("index.html", day_time=day_time)   
    return render_template("index.html", day_time=day_time)    

@app.route("/login",methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # Ensure username or password was submitted
        if not username or not password:
            flash("Username or password is incorrect", "infor")
            return render_template("login.html")
        # Query database for username
        row = db.execute("SELECT * FROM users WHERE username = ?", username)
        # Ensure username exists and password is correct        
        if len(row) != 1 or not check_password_hash(row[0]["password"],password):
            flash("Username does not exist", "infor")
            return render_template("login.html")
        else:
            # Remember which user has logged in
            session["user_id"] = row[0]["id"]
            # Redirect user to home page
            return redirect("/")       
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        
        if (not username) or (not password) or (not confirm):
            flash("you need login or register", "info")
            return render_template("register.html")
        elif password != confirm:
            flash("Confirm incorrect password", "info")
            return render_template("register.html")
        # hashing password for security
        password_hash = generate_password_hash(password)
        # query database and check username already exists
        check = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(check) != 0:
            flash("Username already exists", "info")
            return render_template("register.html")
        # insert new account in to database
        db.execute("INSERT INTO users (username, password) VALUES (?, ?)", username, password_hash)
        row = db.execute("SELECT * FROM users WHERE username = ?", username)
        # Remember which user has logged in
        session["user_id"] = row[0]["id"]
        return redirect("/")
    return render_template("register.html")
    
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/foryou", methods=["GET", "POST"])
def foryou():
    if session.get("user_id") is None:
        return redirect("/login")
    else:
        time = datetime.now()
        day_of_week = time.strftime("%A")
        month = time.strftime("%B")
        day_time = time.strftime(f"{day_of_week}, {month}, %d, %Y")
        
        if request.method == "POST":   
            today = request.form.get("today")
            name = request.form.get("for_you")
            if not today or not name:
                flash("You need to write something to someone so you can save it !", "infor")
                return render_template("foryou.html", day_time=day_time)
            # save dairy for someone into database
            db.execute("INSERT INTO diary_time (user_id, text, for) VALUES (?, ?, ?)", session["user_id"], today, name)
            return render_template("foryou.html", day_time=day_time)   
    return render_template("foryou.html", day_time=day_time) 

@app.route("/mynote", methods=["GET", "POST"])
def mynote():
    if session.get("user_id") is None:
        return redirect("/login")
    else:
        time = datetime.now()
        day_of_week = time.strftime("%A")
        month = time.strftime("%B")
        day_time = time.strftime(f"{day_of_week}, {month}, %d, %Y")
        
        if request.method == "POST": 
            note = request.form.get("note")
            if not note:
                flash("You need to write something to so you can save it !", "infor")
                return render_template("mynote.html",day_time=day_time)
            # insert new note in to database 
            db.execute("INSERT INTO notes (user_id, note) VALUES (?, ?)", session["user_id"], note)
            return render_template("mynote.html",day_time=day_time)
    return render_template("mynote.html", day_time=day_time)

@app.route("/note-history")
def note_history():
    if session.get("user_id") is None:
        return redirect("/login")
    else:
        row = db.execute("SELECT * FROM notes WHERE user_id = ?", session["user_id"])
        return render_template("note_history.html", row=row)

@app.route("/delete/<int:hang_id>", methods= ["GET", "POST"])
def delete(hang_id):
    if session.get("user_id") is None:
        return redirect("/login")
    else:
        if request.method == "POST":
            # delete note in database when click on delete
            db.execute("DELETE FROM notes WHERE note_id = ?", int(hang_id))
            return redirect("/note-history")
    return redirect("/note-history")

@app.route("/diary-history")
def diary_history():
    if session.get("user_id") is None:
        return redirect("/login")
    else:
        row = db.execute("SELECT * FROM diary_time WHERE user_id = ?", session["user_id"])
        return render_template("diary_history.html", row=row)
    