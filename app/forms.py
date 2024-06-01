from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, DateTimeField, SubmitField, SelectField
from wtforms.validators import DataRequired


class TaskForm(FlaskForm):
    execute_on = DateTimeField('Execute On', validators=[DataRequired()])
    ticket_id = StringField('Ticket ID', validators=[DataRequired()])
    description = TextAreaField('Description')
    effort = IntegerField('Effort')
    submit = SubmitField('Submit')

class TicketForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    report_on = DateTimeField('Report On', validators=[DataRequired()])
    project_id = StringField('Project ID')
    description = TextAreaField('Description')
    submit = SubmitField('Submit')

class ProjectForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    charger_amount = IntegerField('Charger Amount')
    latitude = IntegerField('Latitude')
    longitude = IntegerField('Longitude')
    create_on = DateTimeField('Create On')
    submit = SubmitField('Submit')