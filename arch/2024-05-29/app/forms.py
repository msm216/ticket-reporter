from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, DateTimeField, SelectField
from wtforms.validators import DataRequired

class TaskForm(FlaskForm):
    id = StringField('ID', validators=[DataRequired()])
    execute_on = DateTimeField('Execute On', validators=[DataRequired()])
    ticket_id = SelectField('Ticket', coerce=str, validators=[DataRequired()])
    description = TextAreaField('Description')
    effort = IntegerField('Effort')

class TicketForm(FlaskForm):
    id = StringField('ID', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    report_on = DateTimeField('Report On', validators=[DataRequired()])
    project_id = SelectField('Project', coerce=str)
    description = TextAreaField('Description')
    update_on = DateTimeField('Update On')

class ProjectForm(FlaskForm):
    id = StringField('ID', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    create_on = DateTimeField('Create On', validators=[DataRequired()])
    charger_amount = IntegerField('Charger Amount')
    latitude = IntegerField('Latitude')
    longitude = IntegerField('Longitude')