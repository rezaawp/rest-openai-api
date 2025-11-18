from flask import Blueprint, send_file, request, jsonify
from werkzeug.utils import secure_filename
import os
from services.extraction_invoice.main import process_invoices
from extensions import db
from models.bulk_invoice_status import BulkInvoiceStatus
from models.invoice import Invoice
import asyncio
from sqlalchemy.orm import selectinload

invoice_handler = Blueprint("process_inv", __name__)

@invoice_handler.route("/process_invoices", methods=["POST"])
def process_uploaded_invoices():
    data = request.get_json()
    if not data or "directory" not in data:
        return jsonify({"error": "No directory provided"}), 400

    invoice_dir = data["directory"]

    _path_dir = os.path.join(os.getenv("INVOICE_DIR", "i=nvoices"), invoice_dir)
    if not os.path.exists(_path_dir):
        return jsonify({"error": "Directory does not exist"}), 400

    try:
        asyncio.run(process_invoices(invoice_dir))
        record = BulkInvoiceStatus.query.filter_by(random_dir_name=invoice_dir).first()
        record.status = "Processed"
        db.session.commit()
        return jsonify({
            "message": "Invoices processed successfully", 
            "data": {
                "download_url": f"http://localhost:5000/api/download-output?directory={invoice_dir}"
            }}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@invoice_handler.route("/download_output", methods=["GET"])
def download_outputs():
    # Ambil directory dari query parameter GET
    invoice_dir = request.args.get("directory")
    if not invoice_dir:
        return jsonify({"error": "No directory provided"}), 400

    # Path file output
    output_path = os.path.join("data", "outputs", f"invoices-report-{invoice_dir}.xlsx")

    if not os.path.exists(output_path):
        return jsonify({"error": "Output file does not exist"}), 400

    try:
        # Kirim file sebagai attachment agar bisa di-download
        return send_file(
            output_path,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            as_attachment=True,
            download_name=f"invoices-report-{invoice_dir}.xlsx"
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@invoice_handler.route("/invoices", methods=["GET"])
def list_invoices():
    invoices = Invoice.query.options(selectinload(Invoice.items)).all()
    result = []
    for inv in invoices:
        invoice_dict = {
            "invoice_number": inv.invoice_number,
            "invoice_date": inv.invoice_date.isoformat() if inv.invoice_date else None,
            "invoice_type": inv.invoice_type,
            "issuer": {
                "name": inv.issuer_name,
                "address": inv.issuer_address,
                "phone": inv.issuer_phone,
                "email": inv.issuer_email
            },
            "recipient": {
                "name": inv.recipient_name,
                "address": inv.recipient_address,
                "phone": inv.recipient_phone,
                "email": inv.recipient_email
            },
            "subtotal": float(inv.subtotal) if inv.subtotal else 0,
            "tax_rate": float(inv.tax_rate) if inv.tax_rate else 0,
            "tax": float(inv.tax) if inv.tax else 0,
            "total": float(inv.total) if inv.total else 0,
            "terms": inv.terms,
            "items": [
                {"description": item.description, "total": float(item.total)}
                for item in inv.items
            ]
        }
        result.append(invoice_dict)

    # Return JSON
    return jsonify(result), 200