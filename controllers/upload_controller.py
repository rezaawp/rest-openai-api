from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
import uuid
from services.extraction_invoice.main import process_invoices
from models.company import Company

upload_bp = Blueprint("upload", __name__)

ALLOWED_EXTENSIONS = {"pdf"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route("/upload", methods=["POST"])
def upload_file():
    # # companies = Company.query.all()
    # # if not companies:
    # #     return jsonify({"message": "Upload endpoint"}), 200
    # # else:
    # return jsonify({"message": "Companies exist in the database"}), 200
    # Harus ada key 'files'
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

    # Jalankan proses hanya sekali untuk semua folder
    # (jika logic kamu butuh satu folder per file, gunakan loop)
    # for i_dir in invoice_dirs:
    #     asyncio.run(process_invoices(invoice_dir=i_dir))

    return jsonify({
        "message": "Multiple upload success",
        "files": saved_files
    }), 200