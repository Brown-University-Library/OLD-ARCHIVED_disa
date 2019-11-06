from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, current_user
from werkzeug.urls import url_parse

from . import auth
from .. import db, models, forms

import datetime
import collections
from operator import itemgetter


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('editor.index_documents'))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('editor.editor_index')
        user.last_login = datetime.datetime.utcnow()
        db.session.add(user)
        db.session.commit()
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.browse'))