from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, Preset

presets_bp = Blueprint('presets', __name__)


@presets_bp.route('/presets', methods=['GET'])
@jwt_required()
def get_presets():
    current_user = get_jwt_identity()
    presets = Preset.query.filter_by(user_id=current_user).all()
    results = [{"id": preset.id, "name": preset.name, "styles": preset.get_styles()} for preset in presets]
    return jsonify(results), 200
   
    
@presets_bp.route('/presets', methods=['POST'])
@jwt_required()
def create_preset():
    try:
        current_user = get_jwt_identity()
        print(current_user)
        preset_data = request.get_json()
        print(preset_data)
        name = preset_data.get('name')
        styles = preset_data.get('styles')
        if not name:
            return jsonify({'error': 'You must provide a Preset name'}), 400
        if not styles:
            return jsonify({'error': 'Styles can not be empty'}), 400
        
        new_preset = Preset(name=name, user_id=current_user)
        new_preset.set_styles(styles)
        db.session.add(new_preset)
        db.session.commit()
        return jsonify({'id': new_preset.id, 'name': new_preset.name, 'styles': new_preset.get_styles()}), 201
        
    except Exception as e:
        return jsonify({'error': e})
    
    