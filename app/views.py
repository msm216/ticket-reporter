import os

from flask import render_template, request, jsonify, redirect, url_for
from app import create_app, db
from app.models import Task, Ticket, Project
from app.forms import TaskForm, TicketForm, ProjectForm



app = create_app()


############## 主要页面 ##############

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/tasks')
def tasks():
    tasks = Task.query.all()
    form = TaskForm()
    return render_template('task.html', tasks=tasks, form=form)

@app.route('/tickets')
def tickets():
    tickets = Ticket.query.all()
    form = TicketForm()
    return render_template('ticket.html', tickets=tickets, form=form)

@app.route('/projects')
def projects():
    projects = Project.query.all()
    form = ProjectForm()
    return render_template('project.html', projects=projects, form=form)

@app.route('/about')
def about():
    last_modified_time = get_last_modified_time(os.getcwd())
    return render_template('about.html', last_modified_time=last_modified_time)

############## 功能页面 ##############

@app.route('/add_task', methods=['POST'])
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            execute_on=form.execute_on.data,
            ticket_id=form.ticket_id.data,
            description=form.description.data,
            effort=form.effort.data
        )
        task.id = Task.generate_id(task.execute_on)
        db.session.add(task)
        db.session.commit()
        return jsonify(success=True)
    return jsonify(success=False)

@app.route('/add_ticket', methods=['POST'])
def add_ticket():
    form = TicketForm()
    if form.validate_on_submit():
        ticket = Ticket(
            title=form.title.data,
            report_on=form.report_on.data,
            project_id=form.project_id.data,
            description=form.description.data
        )
        ticket.id = Ticket.generate_id(ticket.report_on)
        db.session.add(ticket)
        db.session.commit()
        return jsonify(success=True)
    return jsonify(success=False)

@app.route('/add_project', methods=['POST'])
def add_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(
            title=form.title.data,
            charger_amount=form.charger_amount.data,
            latitude=form.latitude.data,
            longitude=form.longitude.data,
            create_on=form.create_on.data
        )
        project.id = Project.generate_id(project.create_on)
        db.session.add(project)
        db.session.commit()
        return jsonify(success=True)
    return jsonify(success=False)






def get_last_modified_time(directory):
    import os
    import datetime
    latest_time = None
    for root, dirs, files in os.walk(directory):
        for fname in files:
            filepath = os.path.join(root, fname)
            file_mtime = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))
            if latest_time is None or file_mtime > latest_time:
                latest_time = file_mtime
    return latest_time






@app.route('/get_task/<task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    if task:
        return {
            'id': task.id,
            'execute_on': task.execute_on,
            'ticket_id': task.ticket_id,
            'description': task.description,
            'effort': task.effort
        }
    return {'success': False}

@app.route('/edit_task/<task_id>', methods=['POST'])
def edit_task(task_id):
    task = Task.query.get(task_id)
    if task:
        form = TaskForm(request.form)
        if form.validate_on_submit():
            task.execute_on = form.execute_on.data
            task.ticket_id = form.ticket_id.data
            task.description = form.description.data
            task.effort = form.effort.data
            db.session.commit()
            return {'success': True}
    return {'success': False}

@app.route('/delete_task/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return {'success': True}
    return {'success': False}

@app.route('/task_statistics', methods=['GET'])
def task_statistics():
    # Generate data for the charts
    bar_data = {
        'labels': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
        'data': [10, 20, 15, 5]
    }
    pie_data = {
        'labels': ['Ticket 1', 'Ticket 2', 'Ticket 3'],
        'data': [15, 25, 10]
    }
    return {
        'bar': bar_data,
        'pie': pie_data
    }