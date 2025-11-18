from services.extraction_invoice.extraction import extract_invoices_data
from services.extraction_invoice.processing import (
    build_invoices_dataframe, generate_financial_summary, create_excel_report
)
from dotenv import load_dotenv

load_dotenv()
async def process_invoices(invoice_dir="data/invoices"):
    invoices_filenames, invoices_json = await extract_invoices_data(invoice_dir)
    invoices_df = build_invoices_dataframe(invoices_filenames, invoices_json)
    total_s, monthly_df = generate_financial_summary(invoices_df)
    create_excel_report(invoices_df, total_s, monthly_df, "data/invoices-report.xlsx")
