"""Blueprints package initialization"""

from app.blueprints.home import bp as home_bp
from app.blueprints.issue import bp as issue_bp
from app.blueprints.ticket import bp as ticket_bp
from app.blueprints.pages import bp as pages_bp
from app.blueprints.api import bp as api_bp

__all__ = ['home_bp', 'issue_bp', 'ticket_bp', 'pages_bp', 'api_bp']
