from flask import Flask, request, jsonify
from flask_cors import CORS
from algo import swap_typosquatting, remove_typesquatting, duplicate_typesquatting

app = Flask(__name__)
CORS(app)  # <-- allow requests from all origins (for dev)

@app.route("/typosquat", methods=["POST"])
def typosquat():
    data = request.json
    website = data.get("website")
    
    if not website:
        return jsonify({"error": "No website provided"}), 400

    swap_results = swap_typosquatting(website)
    remove_results = remove_typesquatting(website)
    duplicate_results = duplicate_typesquatting(website)

    return jsonify({
        "swap": swap_results,
        "remove": remove_results,
        "duplicate": duplicate_results
    })

if __name__ == "__main__":
    app.run(port=5000, debug=True)
