from extensions import db

class BulkInvoiceStatus(db.Model):
    __tablename__ = "bulk_invoice_statuses"

    id = db.Column(db.Integer, primary_key=True)
    random_dir_name = db.Column(db.String(500))
    status = db.Column(db.String(100))
