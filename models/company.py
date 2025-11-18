from extensions import db

class Company(db.Model):
    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(500), nullable=False)
    phone = db.Column(db.String(50))
    email = db.Column(db.String(100))
    description = db.Column(db.String(1000))

    # Relationship
    invoices = db.relationship("Invoice", backref="company", lazy=True)
