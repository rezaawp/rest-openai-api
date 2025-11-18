from extensions import db

class Invoice(db.Model):
    __tablename__ = "invoices"

    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(100), nullable=False, unique=True)
    invoice_date = db.Column(db.Date, nullable=False)
    invoice_type = db.Column(db.String(50))  # incoming / outgoing
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"))

    # Relationship
    items = db.relationship("InvoiceItem", backref="invoice", lazy=True)
