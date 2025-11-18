from extensions import db

class Invoice(db.Model):
    __tablename__ = "invoices"

    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(100), nullable=False, unique=True)
    invoice_date = db.Column(db.Date, nullable=False)
    invoice_type = db.Column(db.String(50))  # incoming / outgoing
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"))

    # kolom baru
    issuer_name = db.Column(db.String(255))
    issuer_address = db.Column(db.String(500))
    issuer_phone = db.Column(db.String(50))
    issuer_email = db.Column(db.String(100))
    
    recipient_name = db.Column(db.String(255))
    recipient_address = db.Column(db.String(500))
    recipient_phone = db.Column(db.String(50))
    recipient_email = db.Column(db.String(100))
    
    subtotal = db.Column(db.Numeric(12,2))
    tax_rate = db.Column(db.Numeric(5,2))
    tax = db.Column(db.Numeric(12,2))
    total = db.Column(db.Numeric(12,2))
    terms = db.Column(db.Text)
    # Relationship
    items = db.relationship("InvoiceItem", backref="invoice", lazy=True)
