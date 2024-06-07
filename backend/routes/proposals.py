from flask import Blueprint, request

proposals_bp = Blueprint('proposals', __name__)

@proposals_bp.route('/proposals', methods=['POST'])
def createProposal(): 
    proposal_data = request.get_json()
    print(proposal_data)
    return proposal_data