from flask import Flask, render_template
import os
from services.extraction_invoice.main import process_invoices
import asyncio

app = Flask(__name__)

@app.route('/')
def home():
    asyncio.run(process_invoices())
    return render_template('index.html')

port = int(os.getenv("PORT", 5000))
debug = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
if __name__ == '__main__':
    app.run(debug=debug, port=port)
