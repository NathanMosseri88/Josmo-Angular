from flask import Blueprint, request, jsonify
from ..models import db, Preset

presets_bp = Blueprint('presets', __name__)


@presets_bp.route('/presets', methods=['GET'])
def get_presets():
    presets = Preset.query.all()
    results = [{"id": preset.id, "name": preset.name, "styles": preset.get_styles()} for preset in presets]
    return jsonify(results), 200
   
    
@presets_bp.route('/presets', methods=['POST'])
def create_preset():
    try:
        preset_data = request.get_json()
        name = preset_data.get('name')
        styles = preset_data.get('styles')
        if not name:
            return jsonify({'error': 'You must provide a Preset name'}), 400
        if not styles:
            return jsonify({'error': 'Styles can not be empty'}), 400
        
        new_preset = Preset(name=name)
        new_preset.set_styles(styles)
        db.session.add(new_preset)
        db.session.commit()
        return jsonify({'id': new_preset.id, 'name': new_preset.name, 'styles': new_preset.get_styles()}), 201
        
    except Exception as e:
        return jsonify({'error': e})
    
    