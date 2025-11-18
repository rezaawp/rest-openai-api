from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from services.extraction_invoice.main import process_invoices
from extensions import db
from models.bulk_invoice_status import BulkInvoiceStatus

process_inv = Blueprint("process_inv", __name__)

@process_inv.route("/process_invoices", methods=["POST"])
def process_uploaded_invoices():
    data = request.get_json()
    if not data or "directory" not in data:
        return jsonify({"error": "No directory provided"}), 400

    invoice_dir = data["directory"]

    if not os.path.exists(invoice_dir):
        return jsonify({"error": "Directory does not exist"}), 400

    try:
        results = process_invoices(invoice_dir)
        record = BulkInvoiceStatus.query.filter_by(random_dir_name=invoice_dir).first()
        record.status = "Processed"
        db.session.commit()
        return jsonify({"message": "Invoices processed successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500