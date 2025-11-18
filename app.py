from flask import Flask, render_template
import os
from services.extraction_invoice.main import process_invoices
import asyncio
from controllers.upload_controller import upload_bp  # import blueprint

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

app.register_blueprint(upload_bp, url_prefix="/api")

port = int(os.getenv("PORT", 5000))
debug = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
if __name__ == '__main__':
    app.run(debug=debug, port=port)
