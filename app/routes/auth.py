from flask import Blueprint, render_template, flash, redirect, url_for, request
from app.forms.register_form import RegistrationForm
from app.models.user import User
from app.utils.security import hash_password
from app import db

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        # Check if username/email exists
        existing_user = User.query.filter((User.username == form.username.data) |
                                          (User.email == form.email.data)).first()
        if existing_user:
            flash('Username or email already exists.', 'danger')
            return render_template('register.html', form=form)

        # Hash password and create new user
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            phone=form.phone.data,
            password_hash=hash_password(form.password.data)
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)

from flask_login import login_user, logout_user, login_required, current_user
from app.forms.login_form import LoginForm
from app.utils.security import verify_password

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.", "info")
        return redirect(url_for('user.profile'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and verify_password(user.password_hash, form.password.data):
            login_user(user)
            flash("Logged in successfully.", "success")
            next_page = request.args.get('next')
            return redirect(next_page or url_for('user.profile'))
        else:
            flash("Invalid email or password.", "danger")

    return render_template("login.html", form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('auth.login'))
