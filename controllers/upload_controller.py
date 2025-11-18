from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
import uuid
from services.extraction_invoice.main import process_invoices
import asyncio

upload_bp = Blueprint("upload", __name__)

ALLOWED_EXTENSIONS = {"pdf"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if file and allowed_file(file.filename):
        # Ambil extension aslinya
        ext = file.filename.rsplit(".", 1)[1].lower()

        random_string = uuid.uuid4().hex
        # Generate nama random
        random_name = f"{random_string}.{ext}"

        invoice_dir = os.getenv("INVOICE_DIR", "invoices") + "/" + random_string
        
        os.makedirs(invoice_dir, exist_ok=True)
        
        save_path = os.path.join(invoice_dir, random_name)
        file.save(save_path)

        asyncio.run(process_invoices(invoice_dir=invoice_dir))

        return jsonify({
            "message": "Upload successful",
            "original_filename": secure_filename(file.filename),
            "saved_as": random_name,
            "path": save_path
        }), 200

    return jsonify({"error": "Invalid file type, only PDF allowed"}), 400
