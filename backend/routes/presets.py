from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, Preset

presets_bp = Blueprint('presets', __name__)


@presets_bp.route('/presets', methods=['GET'])
@jwt_required()  # access to this endpoint is only allowed if the client request includes an approved JWT access token
def get_presets():
    current_user = get_jwt_identity()  # gets User ID using JWT auth token from request
    presets = Preset.query.filter_by(user_id=current_user).all()  # query DB for presets belonging to that user using the user_id foreign key column
    # create JSON array for queried presets
    results = [{"id": preset.id, "name": preset.name, "styles": preset.styles} for preset in presets]
    # sends prests JSON back to client
    return jsonify(results), 200
   
    
@presets_bp.route('/presets', methods=['POST'])
@jwt_required()  # access to this endpoint is only allowed if the client request includes an approved JWT access token
def create_preset():
    try:
        current_user = get_jwt_identity()  # gets User ID using JWT auth token from request
        preset_data = request.get_json()
        name = preset_data.get('name')
        styles = preset_data.get('styles')

        # if request is not sent with a name or an empty styles array, return errors
        if not name:
            return jsonify({'error': 'You must provide a Preset name'}), 400
        if not styles:
            return jsonify({'error': 'Styles can not be empty'}), 400
        
        # create new Preset instance and relate it to the user sending the request using the user_id column 
        new_preset = Preset(name=name, user_id=current_user, styles=styles)
        # store new Preset instance in DB
        db.session.add(new_preset)
        db.session.commit()
        # send new Preset data back to client
        return jsonify({'id': new_preset.id, 'name': new_preset.name, 'styles': new_preset.styles}), 201
        
    except Exception as e:
        return jsonify({'error': e})
    
    