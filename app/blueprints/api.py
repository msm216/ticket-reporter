"""API Blueprint - Common CRUD operations for all models"""

import enum
from datetime import datetime
from flask import Blueprint, request, jsonify, send_file
from io import BytesIO
from weasyprint import HTML

from app.models import Issue, Resolution, Ticket, Task
from app import db

bp = Blueprint('api', __name__)


# MODEL MAPPING
MODELS = {
    'issue': Issue,
    'resolution': Resolution,
    'ticket': Ticket,
    'task': Task
}

REFERENCE = {
    'issue': 'resolution',
    'ticket': 'task'
}


############################################ CRUD ROUTES ###################################################

@bp.route('/<object_class>/<inst_id>', methods=['GET'])
def get_instance(inst_id: str, object_class: str):
    """Get instance data by ID and class"""
    print(f"Getting {object_class}: {inst_id}...")
    object_model = MODELS.get(object_class)
    if not object_model:
        return jsonify({'Error': f'Model {object_class} not found'}), 404

    instance = object_model.query.get(inst_id)
    if instance:
        instance_data = {}
        for column in object_model.__table__.columns:
            value = getattr(instance, column.name)
            if isinstance(value, enum.Enum):
                instance_data[column.name] = value.value
            elif isinstance(value, datetime):
                instance_data[column.name] = value.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(value, (str, int, float, bool, type(None))):
                instance_data[column.name] = value
            else:
                instance_data[column.name] = str(value)
        return jsonify(instance_data)
    return jsonify({'Error': 'Instance not found'}), 404


@bp.route('/<object_class>/add', methods=['POST'])
def add_instance(object_class: str):
    """Add new instance"""
    print(f"Adding new {object_class}...")
    object_model = MODELS.get(object_class)
    if not object_model:
        return jsonify(success=False, message=f"Model {object_class} not exist"), 400

    try:
        # Get form data from request
        if request.content_type == 'application/json':
            form_data = request.json
        else:
            form_data = request.form.to_dict()

        print(f"Received form data for '{object_class}': {form_data}")

        # Set report_on to current date if not provided
        report_on = form_data.get('report_on')
        if not report_on:
            form_data['report_on'] = datetime.now()
        else:
            form_data['report_on'] = datetime.strptime(report_on, '%Y-%m-%d')

        # Filter valid fields
        valid_fields = {key: form_data[key] for key in form_data if key in object_model.__table__.columns.keys()}

        # Create and save instance
        new_instance = object_model(**valid_fields)
        db.session.add(new_instance)
        db.session.commit()

        return jsonify(success=True, id=new_instance.id)
    except Exception as e:
        db.session.rollback()
        print(f"Error adding {object_class}: {str(e)}")
        return jsonify(success=False, message=f"Failed to add instance: {str(e)}"), 500


@bp.route('/<object_class>/<inst_id>/edit', methods=['PUT'])
def edit_instance(object_class: str, inst_id: int):
    """Edit existing instance"""
    print(f"Editing {object_class} instance: {inst_id}...")
    object_model = MODELS.get(object_class)
    if not object_model:
        return jsonify(success=False, message=f"Model {object_class} not exist"), 400

    try:
        # Get form data from request
        if request.content_type == 'application/json':
            form_data = request.json
        else:
            form_data = request.form.to_dict()

        print(f"Received form data for '{object_class}': {form_data}")

        instance = object_model.query.get(inst_id)
        if not instance:
            return jsonify(success=False, message=f"{object_class} instance with ID {inst_id} not found"), 404

        # Update instance attributes
        for key, value in form_data.items():
            if key in object_model.__table__.columns.keys():
                setattr(instance, key, value)

        db.session.commit()
        return jsonify(success=True, message="Instance updated successfully")
    except Exception as e:
        db.session.rollback()
        print(f"Error updating {object_class}: {str(e)}")
        return jsonify(success=False, message="Failed to update instance: " + str(e)), 500


@bp.route('/<object_class>/<inst_id>/update', methods=['POST'])
def update_instance(object_class: str, inst_id: str):
    """Update instance (placeholder)"""
    print(f"Updating {object_class}: {inst_id}")
    return jsonify(success=True)


@bp.route('/<object_class>/<inst_id>/delete', methods=['DELETE'])
def delete_instance(object_class: str, inst_id: str):
    """Delete instance"""
    print(f"Deleting {object_class}: {inst_id}")
    object_model = MODELS.get(object_class)
    instance = object_model.query.get(inst_id)
    db.session.delete(instance)
    db.session.commit()
    return jsonify(success=True)


@bp.route('/<object_class>/<inst_id>/print', methods=['GET'])
def generate_pdf(inst_id: str, object_class: str):
    """Generate PDF report for instance"""
    if not inst_id:
        return "No issue selected", 400

    object_model = MODELS.get(object_class)
    instance = object_model.query.get(inst_id)

    if not instance:
        return "Issue not found", 404

    # Render HTML template
    from flask import render_template
    rendered_html = render_template(f'report/{object_class}.html', inst=instance)

    # Convert HTML to PDF
    pdf_file = BytesIO()
    HTML(string=rendered_html).write_pdf(pdf_file)
    pdf_file.seek(0)

    return send_file(pdf_file,
                     download_name=f'{instance.id}.pdf',
                     as_attachment=False,
                     mimetype='application/pdf')
