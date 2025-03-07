from flask import Flask, request, jsonify
from jira_llm import generate_summary

app = Flask(__name__)

# Sample in-memory data storage
data_store = []


# Sample GET API
@app.route('/get-data', methods=['GET'])
def get_data():
    return jsonify({"status": "success", "data": data_store})


# Sample POST API
@app.route('/post-data', methods=['POST'])
def post_data():
    data = request.json  # Get JSON data from request body
    if not data:
        return jsonify({"status": "error", "message": "Invalid data"}), 400

    data_store.append(data)
    return jsonify({"status": "success", "message": "Data added successfully", "data": data}), 201


@app.route('/get-summary', methods=['POST'])
def get_summary():
    audit_data = request.json
    if not audit_data:
        return jsonify({"status": "error", "message": "Invalid data"}), 400

    summary = generate_summary(audit_data)
    return jsonify({"status": "success", "message": "Summary generated successfully", "data": summary})


if __name__ == '__main__':
    app.run(debug=True)
