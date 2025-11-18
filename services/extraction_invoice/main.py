from services.extraction_invoice.extraction import extract_invoices_data
from services.extraction_invoice.processing import (
    build_invoices_dataframe, generate_financial_summary, create_excel_report
)
from dotenv import load_dotenv
import os
from extensions import db
from models.bulk_invoice_status import BulkInvoiceStatus

load_dotenv()
async def process_invoices(invoice_dir="data/invoices"):
    _path_dir = os.path.join(os.getenv("INVOICE_DIR", "i=nvoices"), invoice_dir)
    record = BulkInvoiceStatus.query.filter_by(random_dir_name=invoice_dir).first()
    record.status = "Processing"
    db.session.commit()
    invoices_filenames, invoices_json = await extract_invoices_data(_path_dir)
    invoices_df = build_invoices_dataframe(invoices_filenames, invoices_json)
    total_s, monthly_df = generate_financial_summary(invoices_df)
    create_excel_report(invoices_df, total_s, monthly_df, f"data/outputs/invoices-report-{invoice_dir}.xlsx")
