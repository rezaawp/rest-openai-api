from services.extraction_invoice.extraction import extract_invoices_data
from services.extraction_invoice.processing import (
    build_invoices_dataframe, generate_financial_summary, create_excel_report
)
from services.extraction_invoice.config import settings

async def process_invoices():
    invoices_filenames, invoices_json = await extract_invoices_data(settings.INVOICES_DIR)
    invoices_df = build_invoices_dataframe(invoices_filenames, invoices_json)
    total_s, monthly_df = generate_financial_summary(invoices_df)
    create_excel_report(invoices_df, total_s, monthly_df, settings.REPORT_FILEPATH)
