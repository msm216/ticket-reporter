"""Issue Blueprint - Issue management routes"""

from datetime import datetime, timedelta
from flask import Blueprint, render_template, request

from app.models import Issue

bp = Blueprint('issue', __name__, url_prefix='/issue')


@bp.route('')
def issue_page():
    """Issue list page with filtering and grouping"""
    theme = 'issue'
    print(f"\nPage theme: {theme}")

    # Get all Issue instances
    issues_all = Issue.query.all()
    # Sort resolutions by update_on descending
    for issue in issues_all:
        issue.resolutions = sorted(issue.resolutions, key=lambda r: r.update_on, reverse=True)

    # Handle instance selection
    selected_issue_id = request.args.get('issue-select', 'all')

    if selected_issue_id == 'all':
        # Apply filtering conditions
        start_date_str = request.args.get('start-date', '2024-01-01')
        end_date_str = request.args.get('end-date', datetime.now().strftime('%Y-%m-%d'))
        exclude_closed = request.args.get('exclude-closed', False)

        # Convert date strings to date objects
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d') + timedelta(days=1)

        # Filter issues by date
        issues_filtered = [issue for issue in issues_all if end_date >= issue.report_on >= start_date]

        # Filter out closed issues
        if exclude_closed:
            issues_filtered = [issue for issue in issues_filtered if issue.progress.name.lower() != 'closed']

        # Handle grouping
        grouping_by = request.args.get('grouping-by', 'none')
        if grouping_by == 'none':
            issues_by_group = {'All': issues_filtered}
            group_order = ['All']
        elif grouping_by == 'category':
            categories = set([issue.category.name for issue in issues_filtered])
            issues_by_category = {category: [] for category in categories}
            for issue in issues_filtered:
                issues_by_category[issue.category.name].append(issue)
            issues_by_group = issues_by_category
            group_order = sorted(categories)
        elif grouping_by == 'severity':
            severity_order = ['vital', 'critical', 'grave', 'normal', 'minor']
            issues_by_severity = {severity: [] for severity in severity_order}
            for issue in issues_filtered:
                severity_name = issue.severity.name
                if severity_name in issues_by_severity:
                    issues_by_severity[severity_name].append(issue)
            issues_by_group = issues_by_severity
            group_order = severity_order

        expanded_issue_id = None
    else:
        # Show only selected issue
        selected_issue = next((issue for issue in issues_all if issue.id == selected_issue_id), None)
        issues_by_group = {'Selected': [selected_issue]}
        group_order = ['Selected']
        grouping_by = 'none'
        start_date_str = '2024-01-01'
        end_date_str = datetime.now().strftime('%Y-%m-%d')
        expanded_issue_id = selected_issue_id

    return render_template('issue/page.html',
                           page_theme=theme,
                           issues=issues_all,
                           issues_by_group=issues_by_group,
                           group_order=group_order,
                           grouping_by=grouping_by,
                           default_start_date=start_date_str,
                           default_end_date=end_date_str,
                           expanded_issue_id=expanded_issue_id)
