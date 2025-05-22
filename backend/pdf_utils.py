# backend/pdf_utils.py

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

def generate_pdf_brochure(output_path, title, url, summary):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.HexColor("#004080"))
    c.drawString(50, height - 60, title)

    # URL
    c.setFont("Helvetica-Oblique", 11)
    c.setFillColor(colors.blue)
    c.drawString(50, height - 90, url)

    # Summary
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 12)
    y = height - 130
    for line in summary.split('\n'):
        c.drawString(50, y, line)
        y -= 18
        if y < 80:
            c.showPage()
            y = height - 60

    # Footer/branding
    c.setFont("Helvetica-Oblique", 10)
    c.setFillColor(colors.HexColor("#888888"))
    c.drawString(50, 40, "Created by Preeti Kharb | github.com/PreetiKharb")

    c.save()
