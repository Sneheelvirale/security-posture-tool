from functools import wraps
from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, logout_user, current_user, login_required

from app import db
from app.auth import auth_bp
from app.auth.forms import LoginForm, RegisterForm
from app.models import User, AuditLog


def admin_required(f):
    """Decorator to require admin role."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Admin access required.', 'danger')
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('auth.login'))

        login_user(user, remember=form.remember_me.data)
        AuditLog.log_action(user.id, 'login', target_type='user', target_id=user.id,
                            details={'username': user.username})

        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('main.index')
        return redirect(next_page)

    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    user_id = current_user.id
    username = current_user.username
    logout_user()
    AuditLog.log_action(user_id, 'logout', target_type='user', target_id=user_id,
                        details={'username': username})
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Register new users.

    If no users exist in the system, allow anyone to create the first admin.
    Otherwise, only existing admins can register new users.
    """
    total_users = User.query.count()

    if total_users > 0 and (not current_user.is_authenticated or not current_user.is_admin):
        flash('Only administrators can register new users.', 'warning')
        return redirect(url_for('auth.login'))

    form = RegisterForm()
    if form.validate_on_submit():
        # First user is always an admin
        role = 'admin' if total_users == 0 else form.role.data

        user = User(
            username=form.username.data,
            email=form.email.data,
            role=role,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        AuditLog.log_action(
            current_user.id if current_user.is_authenticated else user.id,
            'register_user',
            target_type='user',
            target_id=user.id,
            details={'username': user.username, 'role': role, 'first_user': total_users == 0},
        )

        flash(f'Account created for {user.username} with role "{role}".', 'success')

        if not current_user.is_authenticated:
            login_user(user)
            return redirect(url_for('main.index'))
        return redirect(url_for('auth.users_list'))

    return render_template('auth/register.html', form=form, first_user=(total_users == 0))


@auth_bp.route('/users')
@login_required
@admin_required
def users_list():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('auth/users.html', users=users)
