from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from utils import extract_text, scan_data
from models import (
    save_scan_results,
    get_all_results,
    get_results_by_file,
    delete_scan_results,
)
from db import initialize_database

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing
app.config["UPLOAD_FOLDER"] = "./uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Initialize the database on server start
initialize_database()


# File upload and scanning endpoint
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Save the file
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)
    print(f"File saved: {file_path}")

    try:
        # Extract text and scan
        text = extract_text(file_path)
        if not text:
            return jsonify({"error": "Failed to extract text from the file."}), 500

        results = scan_data(text)
        save_scan_results(file.filename, results)  # Save results in the database

        print(f"Scan Results: {results}")
        return (
            jsonify({"message": "File processed successfully", "results": results}),
            200,
        )
    except Exception as e:
        print(f"Error during file processing: {e}")
        return jsonify({"error": f"Processing error: {e}"}), 500


@app.route("/results", methods=["GET"])
def get_results():
    file_name = request.args.get("file_name")  # Get the file_name parameter if provided
    try:
        if file_name:
            # Fetch results for a specific file
            results = get_results_by_file(
                file_name
            )  # Use the function for specific file
        else:
            # Fetch all results
            results = get_all_results()  # Use the function for all results
        return jsonify({"results": results}), 200
    except Exception as e:
        print(f"Error fetching results: {e}")
        return jsonify({"error": f"Error fetching results: {e}"}), 500


# Delete scanned results endpoint
@app.route("/delete", methods=["DELETE"])
def delete_scan():
    file_name = request.args.get("file_name")
    if not file_name:
        return jsonify({"error": "File name is required"}), 400

    try:
        delete_scan_results(file_name)  # Call the delete function
        return (
            jsonify({"message": f"Results for '{file_name}' deleted successfully"}),
            200,
        )
    except Exception as e:
        print(f"Error deleting scan results: {e}")
        return jsonify({"error": f"Error deleting scan results: {e}"}), 500


# Health check endpoint
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "Server is running"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
