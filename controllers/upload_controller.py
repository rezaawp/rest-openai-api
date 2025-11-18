from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
import uuid
from services.extraction_invoice.main import process_invoices
from models.company import Company
from extensions import db
from models.bulk_invoice_status import BulkInvoiceStatus

upload_bp = Blueprint("upload", __name__)

ALLOWED_EXTENSIONS = {"pdf"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route("/upload", methods=["POST"])
def upload_file():
    if "files" not in request.files:
        return jsonify({"error": "No files part in the request"}), 400

    files = request.files.getlist("files")

    if len(files) == 0:
        return jsonify({"error": "No files selected"}), 400

    saved_files = []
    invoice_dirs = []

    random_dir = uuid.uuid4().hex

    invoice_dir = os.path.join(os.getenv("INVOICE_DIR", "invoices"), random_dir)
    os.makedirs(invoice_dir, exist_ok=True)

    for file in files:
        if file.filename == "":
            continue

        if file and allowed_file(file.filename):
            # Ambil extension
            ext = file.filename.rsplit(".", 1)[1].lower()

            # Random folder & filename
            random_string = uuid.uuid4().hex
            random_name = f"{random_string}.{ext}"
            
            save_path = os.path.join(invoice_dir, random_name)
            file.save(save_path)

            saved_files.append({
                "original_filename": secure_filename(file.filename),
                "saved_as": random_name,
                "folder": invoice_dir,
                "path": save_path
            })

            invoice_dirs.append(invoice_dir)

        else:
            return jsonify({"error": f"Invalid file type: {file.filename}"}), 400

    db.session.add(BulkInvoiceStatus(
        random_dir_name=random_dir,
        status="Uploaded"
    ))

    db.session.commit()

    return jsonify({
        "message": "Multiple upload success",
        "files": saved_files,
        "directory": invoice_dir
    }), 200

@upload_bp.route("/uploaded_dir", methods=["GET"])
def get_uploaded_dir():
    dirs = BulkInvoiceStatus.query.filter_by(status="Uploaded").all()
    result = []
    for dir_status in dirs:
        result.append({
            "id": dir_status.id,
            "random_dir_name": dir_status.random_dir_name,
            "status": dir_status.status
        })
    return jsonify({
        "status":"success",
        "message": "Fetched uploaded directories",
        "data":result   
    }), 200