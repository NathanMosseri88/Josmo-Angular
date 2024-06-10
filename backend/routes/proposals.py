from flask import Blueprint, request, jsonify
from ..models import Proposal, db

proposals_bp = Blueprint('proposals', __name__)

@proposals_bp.route('/proposals', methods=['POST'])
def createProposal(): 
    try:
        proposal_data = request.get_json()
        styles = proposal_data.get('styles')
        include_columns = proposal_data.get('columns')

        if not styles:
            return jsonify({'error': 'Styles can not be empty'}), 400
        
        new_proposal = Proposal(
            run_type=proposal_data['type'],
            view_by=proposal_data['view'],
            pairs_cases=proposal_data['pairs_cases'],
            stock_filters =proposal_data['filters'],
            status=proposal_data['status'],
            file_name=proposal_data['filename']
        )
        new_proposal.set_styles(styles)
        new_proposal.set_include_columns(include_columns)
        db.session.add(new_proposal)
        db.session.commit()
        return jsonify(new_proposal.serizalize), 200
    except Exception as e:
        return jsonify({'error': e})

