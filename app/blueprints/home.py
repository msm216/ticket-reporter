"""Home Blueprint - Home page and common routes"""

from flask import Blueprint, render_template, request

bp = Blueprint('home', __name__)


@bp.route('/')
def home():
    """Home page"""
    return render_template('home/page.html')


@bp.route('/load-form', methods=['GET'])
def load_form():
    """Load dynamic form modal"""
    from datetime import datetime

    mode = request.args.get('modal-mode')
    object_class = request.args.get('object-class')
    print(f"Loading form '{mode}' for page '{object_class}'...")
    today = datetime.now().strftime('%Y-%m-%d')
    if mode:
        return render_template(f'{object_class}/form/{mode}.html', today=today)
    else:
        return "Invalid mode", 400
