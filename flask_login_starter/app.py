from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.username)


app = Flask(__name__)
app.secret_key = 'some_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please login to access this page.'
login_manager.login_message_category = 'error'

users = {'admin': User('admin', 'admin'), 'user': User('user', 'user')}


@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('logged_in'))

    next_page = request.args.get('next')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and user.password == password:
            login_user(user)
            return redirect(next_page or url_for('logged_in'))
        else:
            flash('Invalid username or password.', category='error')
            # return redirect(url_for('login', **request.args))

    # if request.method == 'GET'
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('logged_in'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match.', category='error')
            return render_template('register.html')
        if username in users:
            flash('Username already taken.', category='error')
            return render_template('register.html')

        user = User(username, password)
        users[username] = user

        login_user(user)

        return redirect(url_for('logged_in'))
    else:
        return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/logged-in')
@login_required
def logged_in():
    return render_template('logged-in.html')


if __name__ == '__main__':
    app.run(debug=True)
