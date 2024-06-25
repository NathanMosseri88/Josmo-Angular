from flask import Blueprint, request, jsonify
from ..models import Proposal, db
from flask_jwt_extended import jwt_required, get_jwt_identity
from python_files.Database_Modules import print_color
from python_files.Automation_Programs.Automate_Proposals_v2 import generate_web_proposal
proposals_bp = Blueprint('proposals', __name__)

@proposals_bp.route('/proposals', methods=['POST'])
@jwt_required()  # access to this endpoint is only allowed if the client request includes an approved JWT access token
def createProposal():
    # try:
    proposal_data = request.get_json()
    print_color(proposal_data, color='g')
    styles = proposal_data.get('styles')
    size_run = proposal_data.get('type')
    view = proposal_data.get('view')
    pairs_cases = proposal_data.get('pairs_cases')
    include_columns = proposal_data.get('columns')
    filters = proposal_data.get('filters')
    status = proposal_data.get('status')
    quantityLess = proposal_data.get('quantityLess')
    quantityGreater = proposal_data.get('quantityGreater')
    filename = proposal_data.get('filename')

    size_run = True if size_run == 'Size Run' else False

    upc = True if view == 'UPC' else False
    size_detail = True if view == 'Size' else False

    include_stock_or_no_stock = False if filters == 'In Stock Only' else True
    quantity_filter = quantityGreater
    less_than_quantity_filter = quantityLess
    active_only = True if status == 'Active' else False

    include_0_quantites =  True if filters == 'Include 0 Quantities' else True
    price_limit = 15



    Price = True if 'Price' in include_columns else False
    Cost = True if 'Cost' in include_columns else False
    Average_Cost = True
    percent_profit = 50
    ats = False
    incoming = False
    in_stock = False
    brand = False
    description = False
    note = False



    print_color(proposal_data, color='g')
    if not styles:  # if the request has an empty styles field, send an error back to the client
        return jsonify({'error': 'Styles can not be empty'}), 400

    # generate_web_proposal(styles=styles)
    # create new Proposal instance with client request data
    # new_proposal = Proposal(
    #     run_type=proposal_data['type'],
    #     view_by=proposal_data['view'],
    #     pairs_cases=proposal_data['pairs_cases'],
    #     stock_filters=proposal_data['filters'],
    #     status=proposal_data['status'],
    #     file_name=proposal_data['filename'],
    #     include_columns=include_columns,
    #     styles=styles
    # )
    # # store new Proposal instance in DB
    # db.session.add(new_proposal)
    # db.session.commit()
    # return created proposal data back to the client

    Data = True
    return jsonify(Data), 200
    # except Exception as e:
    #     return jsonify({'error': e})

