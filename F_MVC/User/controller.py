from flask import Blueprint, request, render_template, redirect, session

from F_MVC.Trolly.service import get_states
from F_MVC.User.service import check_user

user_routes = Blueprint('app_configs', __name__)


@user_routes.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return redirect('/')
    print("inside login route")
    if not request.form['email']:
        return render_template('Login.html', error="email cant be empty")

    if not request.form['password']:
        return render_template('Login.html', error='password cant be empty')

    email = request.form['email']
    password = request.form['password']
    found, message = check_user(email, password)
    if not found:
        return render_template('Login.html', error=message)

    active_trolleys, max_temperature, min_temperature, total_trolleys = get_states()
    session['email'] = email
    return render_template('Dashboard.html', data={
        'active_trolleys': active_trolleys,
        'max_temperature': max_temperature,
        'min_temperature': min_temperature,
        'total_trolleys': total_trolleys,
        'email': email
    })


@user_routes.route('/logout')
def logout():
    session['email'] = None
    return redirect('/')