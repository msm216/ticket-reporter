"""Pages Blueprint - Static pages (About, Service, Commission)"""

from flask import Blueprint, render_template

from app.utilities import last_commit_time

bp = Blueprint('pages', __name__)


@bp.route('/commission')
def commission_page():
    """Commission page"""
    theme = 'commission'
    print(f"\nTheme of the page: '{theme}'.")
    return render_template('commission/page.html')


@bp.route('/service')
def service_page():
    """Service page"""
    theme = 'service'
    print(f"\nTheme of the page: '{theme}'.")
    return render_template('service/page.html')


@bp.route('/about')
def about_page():
    """About page"""
    theme = 'about'
    print(f"\nTheme of the page: '{theme}'.")
    return render_template('about/page.html', last_update_date=last_commit_time())
