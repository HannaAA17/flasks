from flask import Flask, render_template, request, session, redirect, url_for

from models import db, User, Place
from forms import SignupForm, loginForm, AddressForm

# define
app = Flask(__name__, static_folder='static', template_folder='templates')
app.config.from_pyfile('config.py')


# initiate
db.init_app(app)


# routes
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home', methods=['GET', 'POST'])
def home():
    places = []
    my_coordinates = (37.4221, -122.0844)

    if 'email' not in session:
        return redirect(url_for('login'))

    elif request.method == 'GET':
        form = AddressForm()

    if request.method == 'POST':
        form = AddressForm(request.form)
        if form.validate():
            place = Place()

            # get the address
            address = form.address.data

            # query for places around it
            my_coordinates = place.address_to_latlng(address)
            places = place.query(address)

    return render_template(
        'home.html', form=form,
        my_coordinates=my_coordinates, places=places,
    )


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'email' in session:
        return redirect(url_for('home'))

    elif request.method == 'GET':
        form = SignupForm()

    elif request.method == 'POST':
        form = SignupForm(request.form)

        if form.validate():
            email = User.find_email(form.email.data)
            if email:
                form.email.errors.append('This email is used, login instead')
            else:
                newuser = User.from_form(form)

                # add to database
                db.session.add(newuser)
                db.session.commit()

                # save email to the session
                session['email'] = newuser.email

                # redirect to home
                return redirect(url_for('home'))

    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'email' in session:
        return redirect(url_for('home'))

    elif request.method == 'GET':
        form = loginForm()

    elif request.method == 'POST':
        form = loginForm(request.form)

        if form.validate():
            user = User.find_email(form.email.data)
            if user is not None:  # valid email
                if user.check_password(form.password.data):  # correct password
                    session['email'] = form.email.data
                    return redirect(url_for('home'))
                else:  # password is wrong
                    form.password.errors.append('Wrong Password!')
            else:  # incorrect email
                form.email.errors.append('Email not found, signup first')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))


# start
if __name__ == '__main__':
    app.run(debug=True)
