"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Get all members
@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

# Get one member
@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"error": "Member not found"}), 404

# Add one member
@app.route('/member', methods=['POST'])
def add_member():
    new_member = request.json
    if not new_member or not all(k in new_member for k in ("first_name", "age", "lucky_numbers")):
        return jsonify({"error": "Invalid input"}), 400
    member = jackson_family.add_member(new_member)
    return jsonify(member), 200  # Change 201 to 200

# Delete a member
@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_a_member(member_id):
    result = jackson_family.delete_member(member_id)
    if "error" in result:
        return jsonify(result), 404
    return jsonify(result), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
