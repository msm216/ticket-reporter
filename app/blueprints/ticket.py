"""Ticket Blueprint - Ticket management routes"""

import os
import pandas as pd
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from werkzeug.utils import secure_filename

from app.models import Ticket
from app.utilities import allowed_file, update_tickets_from_dataframe

bp = Blueprint('ticket', __name__, url_prefix='/ticket')


@bp.route('')
def ticket_page():
    """Ticket list page"""
    theme = 'ticket'
    print(f"\nTheme of the page: '{theme}'.")

    # Get all Ticket instances
    tickets_all = Ticket.query.all()
    # Sort tasks by execute_on descending
    for ticket in tickets_all:
        ticket.tasks = sorted(ticket.tasks, key=lambda r: r.execute_on, reverse=True)

    tickets_filtered = tickets_all

    # Group tickets
    tickets_by_group = {'All': tickets_filtered}
    group_order = ['All']
    filter_by = 'none'

    return render_template('ticket/page.html',
                           tickets=tickets_all,
                           tickets_by_group=tickets_by_group,
                           group_order=group_order,
                           filter_by=filter_by)


@bp.route('/upload', methods=['POST'])
def upload_ticket():
    """Upload and process ticket CSV/Excel file"""
    # Check if file exists in request
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    # Check if filename is empty
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    # Validate file extension
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Process file
        if filename.endswith('.csv'):
            df = pd.read_csv(filepath, parse_dates=['created_on'])
        elif filename.endswith('.xlsx'):
            df = pd.read_excel(filepath, parse_dates=['created_on'])
        else:
            flash('Unsupported file format')
            return redirect(request.url)

        # Update database from dataframe
        update_tickets_from_dataframe(df)
        flash('File successfully uploaded and processed')
        return redirect(url_for('ticket.ticket_page'))

    flash('File type not allowed')
    return redirect(request.url)
