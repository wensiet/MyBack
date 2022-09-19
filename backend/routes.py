from fastapi.responses import RedirectResponse
from flask import render_template, request, redirect, flash
from flask_login import login_user, login_required, logout_user
import flask_login

from backend import db, flask_app, app
from backend.models import Users, News

from backend.auth import Auth

err_msg = "Oops, something went wrong..."


@flask_app.route('/')
def flask_home():
    news = News.query.order_by(News.reg_date.desc()).all()
    return render_template("home.html", news=news)


# @flask_app.route('/create-user', methods=['POST', 'GET'])
# def create_user():
#     if request.method == "POST":
#         username = request.form['username']  # TODO check if this username exists
#         password = request.form['password']  # TODO make password as hash aes256
#         re_password = request.form['repassword']
#         if username == "" or password == "":
#             return render_template("notifications.html", notif_head="There is a error occurred",
#                                    notif_body="Username or password cannot be empty.")
#         if password != re_password:
#             return "Passwords does not match"  # TODO make flash() message
#         else:
#             # password = Auth.hash_pass(password)
#             user = Users(username=username, password=password)
#             try:
#                 db.session.add(user)
#                 db.session.commit()
#                 return render_template("notifications.html", notif_head="User was successfully created.",
#                                        notif_body='<a href="/flask/show-users" class="btn btn-success">See it</a>')
#             except:
#                 return render_template("notifications.html", notif_head="There is a error occurred",
#                                        notif_body="Cannot upload user to database.")
#     else:
#         return render_template("create-user.html")


@flask_app.route("/show-users")
@login_required
def show_users():
    if flask_login.current_user.is_admin:
        users = Users.query.order_by(Users.username).all()
        if users:
            return render_template("show-users.html", users=users)
        else:
            return render_template("notifications.html", notif_head="Users list is empty",
                                   notif_body='<a href="/create-user" class="btn btn-success">Create new user</a>')
    else:
        return render_template("notifications.html", notif_head="Oops, something went wrong...",
                               notif_body="Only Administrators have access to this page")


@flask_app.route("/show-user/remove/<int:id>")
@login_required
def remove_user(id):
    if flask_login.current_user.is_admin:
        user = Users.query.get_or_404(id)
        try:
            db.session.delete(user)
            db.session.commit()
            return redirect("/show-users")
        except:
            return render_template("notifications.html", notif_head="There is a error occurred",
                                   notif_body="Cannot remove this user from a database")
    else:
        return render_template("notifications.html", notif_head="Oops, something went wrong...",
                               notif_body="Only Administrators have access to this page")


@flask_app.route("/register", methods=['GET', 'POST'])
def register():
    if not flask_login.current_user.is_authenticated:
        if request.method == 'POST':
            users = Users.query.order_by(Users.username).all()
            username = request.form['username']
            password = request.form['password']
            if username and password:
                for user in users:
                    if user.username == username:
                        return render_template("notifications.html",
                                               notif_head="This email address is already registered")
                password = Auth.hash_pass(password)
                try:
                    db.session.add(Users(username=username, password=password))
                    db.session.commit()
                    return render_template("notifications.html", notif_head="You've successfully registered!",
                                           notif_body='<a href="/show-users" class="btn btn-success">See it</a>')
                except:
                    return render_template("notifications.html", notif_head="Oops, something went wrong...",
                                           notif_body="Can't upload data to DB")
            # print(username, password) TODO hash pass and commit to DB
            else:
                return render_template("notifications.html", notif_head="You must sign all forms to register")
            # TODO us, pas, repas: must not be null
        else:
            return render_template("auth.html")
    else:
        return render_template("notifications.html", notif_head="You are already authorized")


@flask_app.route("/login", methods=['GET', 'POST'])
def login():
    if not flask_login.current_user.is_authenticated:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if username and password:
                user = Users.query.filter_by(username=username).first()
                if Auth.check_pass(password, user.password):
                    login_user(user)
                    return redirect("/")
                else:
                    return render_template("notifications.html", notif_head="Login or password are incorrect.")
            else:
                return "username or password is empty"
        else:
            return render_template("auth-login.html")
    else:
        return render_template("notifications.html", notif_head="You are already authorized")


@flask_app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    if request.method == 'POST':
        logout_user()
        flash("You've logged out", "info")
        return redirect("/")
    else:
        return render_template("notifications.html", notif_head="Are you sure you want to log out?",
                               notif_body='<form method="post"><button type="submit" class="btn btn-danger">Yes</button></form>')


@flask_app.route("/show-user/find", methods=['GET', 'POST'])
@login_required
def find_user():
    if flask_login.current_user.is_admin:
        if request.method == 'POST':
            username = request.form['search']
            user = Users.query.filter_by(username=username).first()
            if user is not None:
                return render_template("show-users-find.html", user=user)
            else:
                return render_template("notifications.html", notif_head="Oops, something went wrong...",
                                       notif_body="Cannot get username")
        else:
            return render_template("show-users-find.html")
    else:
        return render_template("notifications.html", notif_head="Oops, something went wrong...",
                               notif_body="Only Administrators have access to this page")


@flask_app.route('/show-user/grant-admin/<int:id>')
@login_required
def grant_admin(id):
    if flask_login.current_user.is_admin:
        user = Users.query.filter_by(id=id).first()
        try:
            user.is_admin = True
            db.session.commit()
            return render_template("notifications.html", notif_head="Admin permissions were successfully granted!")
        except:
            return render_template("notifications.html", notif_head="Error occurred while updating to DB.")
    else:
        return render_template("notifications.html", notif_head="You must be in Administrators list to do this")


@flask_app.route('/show-user/revoke-admin/<int:id>')
@login_required
def revoke_admin(id):
    if flask_login.current_user.is_admin:
        user = Users.query.filter_by(id=id).first()
        try:
            user.is_admin = False
            db.session.commit()
            return render_template("notifications.html", notif_head="Admin permissions were successfully revoked!")
        except:
            return render_template("notifications.html", notif_head="Error occurred while updating to DB.")
    else:
        return render_template("notifications.html", notif_head="You must be in Administrators list to do this")


@flask_app.route('/profile/<int:id>')
@login_required
def profile_info(id):
    if flask_login.current_user.is_authenticated:
        user = Users.query.filter_by(id=id).first()
        return render_template("show-info.html", user=user)
    else:
        return redirect('/')


@flask_app.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    if flask_login.current_user.is_admin:
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            try:
                db.session.add(News(title=title, content=content, author=str(flask_login.current_user.username)))
                db.session.commit()
            except:
                return render_template("notifications.html", notif_head=err_msg,
                                       notif_body="Error occurred while loading post to DB.")
            return render_template("notifications.html", notif_head="Successfully added to posts list.")
        else:
            return render_template("news-creater.html")
    else:
        return render_template("notifications.html", notif_head=err_msg,
                               notif_body="You must be Administrator to do this.")


@flask_app.route('/posts')
@login_required
def show_posts():
    if flask_login.current_user.is_admin:
        return render_template("all-posts.html")
    else:
        return render_template("notifications.html", notif_head=err_msg,
                               notif_body="You must be Administrator to do this.")

# @app.post("/flask/create-user")
# def user_adding(user: GetUser):
#     return GetUser


# @app.get("/")
# def release():
#     return RedirectResponse("/")
