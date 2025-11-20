from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
import secrets
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from dotenv import load_dotenv
from utils import extract_text, scan_data
from models import (
    save_scan_results,
    get_all_results,
    get_results_by_file,
    delete_scan_results,
)
from db import initialize_database

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Configuration
app.config["UPLOAD_FOLDER"] = os.getenv("UPLOAD_FOLDER", "./uploads")
app.config["MAX_CONTENT_LENGTH"] = int(os.getenv("MAX_FILE_SIZE", 16 * 1024 * 1024))  # 16MB default
app.config["ALLOWED_EXTENSIONS"] = {"pdf"}
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", secrets.token_hex(32))

# Create uploads directory if it doesn't exist
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Initialize the database on server start
try:
    initialize_database()
except Exception as e:
    logger.error(f"Failed to initialize database: {e}")
    raise


def allowed_file(filename):
    """Check if file extension is allowed."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]


# File upload and scanning endpoint
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        logger.warning("Upload request received without file")
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        logger.warning("Upload request received with empty filename")
        return jsonify({"error": "No selected file"}), 400

    # Validate file extension
    if not allowed_file(file.filename):
        logger.warning(f"Invalid file type attempted: {file.filename}")
        return jsonify({"error": "Only PDF files are allowed"}), 400

    # Sanitize filename
    filename = secure_filename(file.filename)
    if not filename:
        return jsonify({"error": "Invalid filename"}), 400

    # Generate unique filename to prevent conflicts
    unique_filename = f"{secrets.token_hex(8)}_{filename}"
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_filename)

    try:
        # Save the file
        file.save(file_path)
        logger.info(f"File saved: {unique_filename}")

        # Extract text and scan
        text = extract_text(file_path)
        if not text:
            # Clean up file if extraction fails
            os.remove(file_path)
            logger.error(f"Failed to extract text from file: {unique_filename}")
            return jsonify({"error": "Failed to extract text from the file. Please ensure it's a valid PDF."}), 500

        results = scan_data(text)
        save_scan_results(filename, results)  # Save results in the database

        # Clean up uploaded file after processing
        try:
            os.remove(file_path)
            logger.info(f"Temporary file removed: {unique_filename}")
        except Exception as cleanup_error:
            logger.warning(f"Failed to remove temporary file {unique_filename}: {cleanup_error}")

        logger.info(f"File processed successfully: {filename}, found {len(results)} sensitive data items")
        return (
            jsonify({"message": "File processed successfully", "results": results}),
            200,
        )
    except RequestEntityTooLarge:
        logger.warning(f"File too large: {filename}")
        return jsonify({"error": "File size exceeds maximum allowed size"}), 413
    except Exception as e:
        # Clean up file on error
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass
        logger.error(f"Error during file processing: {e}", exc_info=True)
        return jsonify({"error": "An error occurred while processing the file"}), 500


@app.route("/results", methods=["GET"])
def get_results():
    file_name = request.args.get("file_name")
    try:
        if file_name:
            # Sanitize input
            file_name = secure_filename(file_name)
            if not file_name:
                return jsonify({"error": "Invalid file name"}), 400
            results = get_results_by_file(file_name)
            logger.info(f"Retrieved results for file: {file_name}")
        else:
            results = get_all_results()
            logger.info("Retrieved all scan results")
        return jsonify({"results": results}), 200
    except Exception as e:
        logger.error(f"Error fetching results: {e}", exc_info=True)
        return jsonify({"error": "An error occurred while fetching results"}), 500


# Delete scanned results endpoint
@app.route("/delete", methods=["DELETE"])
def delete_scan():
    file_name = request.args.get("file_name")
    if not file_name:
        return jsonify({"error": "File name is required"}), 400

    # Sanitize input
    file_name = secure_filename(file_name)
    if not file_name:
        return jsonify({"error": "Invalid file name"}), 400

    try:
        delete_scan_results(file_name)
        logger.info(f"Deleted scan results for file: {file_name}")
        return (
            jsonify({"message": f"Results for '{file_name}' deleted successfully"}),
            200,
        )
    except Exception as e:
        logger.error(f"Error deleting scan results: {e}", exc_info=True)
        return jsonify({"error": "An error occurred while deleting scan results"}), 500


# Health check endpoint
@app.route("/health", methods=["GET"])
def health_check():
    try:
        # Check database connection
        from db import get_db_connection
        conn = get_db_connection()
        conn.close()
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({"status": "unhealthy", "database": "disconnected"}), 503


# Error handlers
@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({"error": "File size exceeds maximum allowed size"}), 413


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}", exc_info=True)
    return jsonify({"error": "An internal server error occurred"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
