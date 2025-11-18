from extensions import db

class InvoiceItem(db.Model):
    __tablename__ = "invoice_items"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500))
    name = db.Column(db.String(500))
    total = db.Column(db.Float, nullable=False)
    invoice_id = db.Column(db.Integer, db.ForeignKey("invoices.id"))
    