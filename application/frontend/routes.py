from frontend.forms import RegistrationForm, LoginForm
from flask import render_template, redirect, url_for, flash, request
import requests
from flask_login import (LoginManager, login_user, UserMixin, login_required, logout_user, current_user)
from frontend.app import app, bcrypt
import frontend.models as models


login_manager = LoginManager(app)


class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id


@login_manager.user_loader
def load_user(user_id: int):
    try:
        user_data = requests.get(f"http://127.0.0.1:8000/api/v1/accounts/accounts/{user_id}")
        if user_data.status_code == 200:
            user_dict = user_data.json()
            user = models.User(id=user_dict["id"], is_active=user_dict["is_active"])
            return user
    except requests.exceptions.ConnectionError as error:
        app.logger.error(f"Connection error while fetching user data: {error}")
        return None
    except requests.exceptions.RequestException as error:
        app.logger.error(f"Request error while fetching user data: {error}")
        return None


@app.route("/")
def index():
    return render_template("index.html")

@login_manager.unauthorized_handler
def guest_callback():
    return redirect(url_for("login"))

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        pwd_hash = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        account_data = {
            "username": form.username.data,
            "email": form.email.data,
            "password": pwd_hash,

        }
        try:
            response = requests.post(
                "http://127.0.0.1:8000/api/v1/accounts/accounts/", json=account_data)
            if response.status_code == 200:
                flash(
                    f'Account created for {account_data["username"]}!', 'success')
                return redirect(url_for('login'))
            else:
                flash('Failed to create account', 'danger')
        except requests.exceptions.RequestException as error:
            flash('An error occurred while communicating with the server', 'danger')

    return render_template('register.html', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            response = requests.get(
                f"http://127.0.0.1:8000/api/v1/accounts/by_email/{form.email.data}"
            )

            if response.status_code == 200:
                user_data = response.json()
                user_id = user_data.get("id")
                user_password = user_data.get("password")
                user_status = user_data.get("is_active")
                if user_data and bcrypt.check_password_hash(
                    user_password, form.password.data
                ):
                    user = models.User(id=user_id, is_active=user_status)
                    login_user(user)
                    return redirect(url_for("start_game"))
                else:
                    flash("Login failed. Check email email and password", "danger")
            else:
                flash(f"User with email: {form.email.data} not found.", "danger")

        except requests.exceptions.RequestException as error:
            flash("Login failed, server error.", "danger")

    return render_template('login.html', form=form)


@app.route("/start_game/", methods=["POST", "GET"])
@login_required
def start_game():
    if request.method == "POST":
        response = requests.post(
            f"http://127.0.0.1:8000/api/v1/game/create/{current_user.id}")
        game_data = response.json()
        game_id = game_data["game_id"]
        return redirect(url_for("play_game", game_id=game_id))

    return render_template("start_game.html")


@app.route("/play_game/<int:game_id>", methods=["GET", "POST"])
@login_required
def play_game(game_id):
    if request.method == "POST":
        letter = request.form["letter"]

        if not isinstance(letter, str) or not letter.isalpha():
            flash("Invalid input: Please enter a valid letter.", "error")
            return redirect(f"/play_game/{game_id}")
        
        lowercase_letter = letter.lower()
        data = {"letter": lowercase_letter}
        response = requests.post(
            f"http://127.0.0.1:8000/api/v1/game/play/{game_id}/", json=data)

        if response.status_code == 200:
            game_data = response.json()
            image_filename = f'images/hangman{game_data["attempts"]}.png'
            return render_template("game.html", game_data=game_data, game_id=game_id, image_filename=image_filename)
        else:
            return "Error playing game"

    else:
        response = requests.get(
            f"http://127.0.0.1:8000/api/v1/game/games/{game_id}")
        if response.status_code == 200:
            game_data = response.json()
            image_filename = f'images/hangman{game_data["attempts"]}.png'
            return render_template("game.html", game_data=game_data, game_id=game_id, image_filename=image_filename)
        else:
            return "Error getting game data"


@app.route("/game_history/", methods=["GET", "POST"])
@login_required
def game_history():
    try:
        response = requests.get(
            f"http://127.0.0.1:8000/api/v1/game/game_history/{current_user.id}")
        if response.status_code == 200:
            games = response.json()
            return render_template("games.html", games=games)
        else:
            error_message = "Error fetching game history"
    except requests.exceptions.RequestException as e:
        error_message = "Error connecting to API"

    return render_template("games.html", error_message=error_message)


@app.route("/player_stats/")
@login_required
def player_stats():
    try:
        response = requests.get(
            f"http://127.0.0.1:8000/api/v1/game/account/{current_user.id}/stats")
        if response.status_code == 200:
            player_stats_data = response.json()
            return render_template("player_stats.html", player_stats=player_stats_data)
        else:
            error_message = "Error fetching player stats"
    except requests.exceptions.RequestException as e:
        error_message = "Error connecting to API"

    return render_template("player_stats.html", error_message=error_message)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'info')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
