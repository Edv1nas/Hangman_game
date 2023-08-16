from forms import RegistrationForm, LoginForm
from flask import Flask, render_template, redirect, url_for, flash
import requests
from flask_login import LoginManager, login_user, UserMixin, login_required, logout_user

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key_here"

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route('/')
def index():
    return "Welcome to the Flask App"


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        account_data = {
            "username": form.username.data,
            "email": form.email.data,
            "password": form.password.data,
        }
        try:
            response = requests.post(
                "http://127.0.0.1:8000/api/v1/accounts", json=account_data)
            if response.status_code == 200:
                flash(
                    f'Account created for {account_data["username"]}!', 'success')
                return redirect(url_for('login'))
            else:
                flash('Failed to create account', 'danger')
        except requests.exceptions.RequestException as e:
            flash('An error occurred while communicating with the server', 'danger')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        try:
            response = requests.get(
                f"http://127.0.0.1:8000/api/v1/accounts/by_email/{email}")
            if response.status_code == 200:
                account = response.json()
                if account and account["password"] == password:
                    user = User(account["id"])
                    login_user(user)
                    flash(
                        f'Login successful for {account["username"]}!', 'success')
                    return redirect(url_for('start_game'))
                else:
                    flash('Invalid username or password', 'danger')
            else:
                flash('An error occurred while communicating with the server', 'danger')
        except requests.exceptions.RequestException as e:
            flash('An error occurred while communicating with the server', 'danger')

    return render_template('login.html', form=form)


@app.route('/start_game')
@login_required
def start_game():
    return render_template('start_game.html')


@app.route('/player_stats')
def player_stats():
    try:
        response = requests.get(
            "http://127.0.0.1:8000/accounts/{current_user.id}")
        if response.status_code == 200:
            account = response.json()
            return render_template('player_stats.html', account=account)
        else:
            flash('An error occurred while fetching player statistics', 'danger')
    except requests.exceptions.RequestException as e:
        flash('An error occurred while communicating with the server', 'danger')

    return redirect(url_for('index'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'info')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)