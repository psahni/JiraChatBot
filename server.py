import re
from flask import Flask, request, jsonify
from sample_audit_data import audit_data
from summary import generate_summary
from bot.main import process

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
    req = request.json
    print(req["query"])
    if not req["query"]:
        return jsonify({"status": "error", "message": "query is blank"}), 400

    pattern = r"\b(summary|summerization|summerize)\b"

    if re.search(pattern, req["query"], re.IGNORECASE):
        print(req["query"])
        output = generate_summary(audit_data)
    else:
        output = process(req["query"])
    return jsonify({"status": "success", "message": "Summary generated successfully", "data": output })


if __name__ == '__main__':
    app.run(debug=True)
