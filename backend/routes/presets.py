from flask import Blueprint, request, jsonify
from ..models import db, Preset

presets_bp = Blueprint('presets', __name__)


@presets_bp.route('/presets', methods=['GET'])
def get_presets():
    presets = Preset.query.all()
    results = [{"id": preset.id, "name": preset.name, "styles": preset.get_styles()} for preset in presets]
    return jsonify(results)
   
    
@presets_bp.route('/presets', methods=['POST'])
def create_preset():
    preset_data = request.get_json()
    print(preset_data)
    return preset_data
