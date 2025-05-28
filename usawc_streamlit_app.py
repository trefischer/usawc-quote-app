
import streamlit as st
from fpdf import FPDF
from datetime import datetime

class QuotePDF(FPDF):
    def header(self):
        self.set_fill_color(23, 43, 77)
        self.rect(0, 0, 210, 30, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 12)
        self.set_xy(10, 6)
        self.cell(100, 6, "USA Wire & Cable", ln=True)
        self.set_font("Helvetica", "", 9)
        self.set_x(10)
        self.cell(100, 5, "6231 E Stassney Ln BLDG 13, Ste 200, Austin, TX 78744", ln=True)
        self.set_x(10)
        self.cell(100, 5, "Phone: (XXX) XXX-XXXX | www.usawirecable.com", ln=True)
        self.set_xy(150, 6)
        self.set_font("Helvetica", "B", 14)
        self.cell(50, 8, "QUOTE", 0, 2, "R")
        self.set_font("Helvetica", "", 9)
        self.cell(50, 5, "Quote #: 996095", 0, 2, "R")
        self.cell(50, 5, f"Date: {datetime.today().strftime('%b %d, %Y')}", 0, 2, "R")
        self.cell(50, 5, f"Expires: {(datetime.today() + pd.Timedelta(days=1)).strftime('%b %d, %Y')}", 0, 2, "R")

    def quote_table(self, data):
        self.set_y(40)
        self.set_font("Helvetica", "B", 9)
        headers = ["Qty", "Part Number", "Description", "UOM", "Unit Price", "Ext Price"]
        widths = [20, 40, 70, 15, 25, 30]
        for i, header in enumerate(headers):
            self.cell(widths[i], 8, header, 1, 0, "C", True)
        self.ln()
        self.set_font("Helvetica", "", 9)
        for row in data:
            for i, item in enumerate(row):
                self.cell(widths[i], 8, item, 1)
            self.ln()

    def totals(self, total):
        self.set_font("Helvetica", "B", 10)
        self.cell(170, 8, "Total", 1, 0, "R")
        self.cell(30, 8, total, 1, 1, "R")

st.title("USA Wire & Cable Quote Generator")

qty = st.text_input("Quantity", "2500")
part = st.text_input("Part Number", "561-65-3404")
desc = st.text_input("Description", "#12-3C MCHL 600V CPE")
uom = st.text_input("UOM", "FT")
unit_price = st.text_input("Unit Price", "$1.25")
ext_price = st.text_input("Extended Price", "$3,125.00")

if st.button("Generate Quote PDF"):
    pdf = QuotePDF()
    pdf.add_page()
    pdf.quote_table([[qty, part, desc, uom, unit_price, ext_price]])
    pdf.totals(ext_price)
    output_path = "usawc_quote_output.pdf"
    pdf.output(output_path)
    with open(output_path, "rb") as f:
        st.download_button("Download Your Quote", f, file_name="usawc_quote.pdf")
