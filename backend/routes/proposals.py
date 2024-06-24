from flask import Blueprint, request, jsonify
from ..models import Proposal, db
from flask_jwt_extended import jwt_required, get_jwt_identity

proposals_bp = Blueprint('proposals', __name__)

@proposals_bp.route('/proposals', methods=['POST'])
@jwt_required()  # access to this endpoint is only allowed if the client request includes an approved JWT access token 
def createProposal(): 
    try:
        proposal_data = request.get_json()
        styles = proposal_data.get('styles')
        include_columns = proposal_data.get('columns')

        if not styles:  # if the request has an empty styles field, send an error back to the client 
            return jsonify({'error': 'Styles can not be empty'}), 400
        
        # create new Proposal instance with client request data
        new_proposal = Proposal(
            run_type=proposal_data['type'],
            view_by=proposal_data['view'],
            pairs_cases=proposal_data['pairs_cases'],
            stock_filters=proposal_data['filters'],
            status=proposal_data['status'],
            file_name=proposal_data['filename'],
            include_columns=include_columns,
            styles=styles
        )
        # store new Proposal instance in DB
        db.session.add(new_proposal)
        db.session.commit()
        # return created proposal data back to the client 
        return jsonify(new_proposal.serizalize), 200
    except Exception as e:
        return jsonify({'error': e})

