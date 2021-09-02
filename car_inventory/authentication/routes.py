from flask import Blueprint, render_template, request, redirect,url_for, flash
from flask_login.utils import login_required
from drone_inventory.forms import UserLoginForm 
from drone_inventory.models import User, db

# import issue solved
from werkzeug.security import check_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_reguired

auth = Blueprint('auth', __name__, template_folder = 'auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserLoginForm()


    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data

            print(email,password)

            user = User(email,password=password)

            db.session.add(user)
            db.session.commit()

            flash(f'You have successfully created a user account {email}', 'User-created')

            return redirect(url_for('signup.html'))

    except:
        raise Exception('Invalid Form Data: PLease Check your form')

    return render_template('signup.html', form=form)


@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()
    try:
      if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data

            print(email,password)

            logged_user = User.query.filter(User.email == email.first())
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash(f'You have successfully logged in', 'auth-success')
                return redirect(url_for('site.profile'))
            else:
                flash('Your email/password is incorrect', 'auth-failed')
                return redirect(url_for('auth.signin'))
    except:
        raise Exception('Invalid Form Data: PLease Check your form')

    return render_template('signup.html')

@auth.rout('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))