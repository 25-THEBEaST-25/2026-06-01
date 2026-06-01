from io import BytesIO

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from app.schemas.security import ScanResponse


class ReportService:
    def build_pdf(self, scan: ScanResponse) -> bytes:
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        y = height - 64

        pdf.setFont("Helvetica-Bold", 18)
        pdf.drawString(48, y, "Cyber Risk Radar Report")
        y -= 32
        pdf.setFont("Helvetica", 11)
        pdf.drawString(48, y, f"Domain: {scan.domain}")
        y -= 18
        pdf.drawString(48, y, f"Risk score: {scan.risk_score}/100")
        y -= 30

        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawString(48, y, "Executive Summary")
        y -= 18
        pdf.setFont("Helvetica", 10)
        pdf.drawString(48, y, f"{len(scan.findings)} findings and {len(scan.recommendations)} recommendations.")
        y -= 28

        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawString(48, y, "Findings")
        y -= 18
        pdf.setFont("Helvetica", 9)
        for finding in scan.findings[:18]:
            if y < 72:
                pdf.showPage()
                y = height - 64
            pdf.drawString(48, y, f"- [{finding.severity.upper()}] {finding.message}")
            y -= 14

        y -= 12
        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawString(48, y, "Recommendations")
        y -= 18
        pdf.setFont("Helvetica", 9)
        for recommendation in scan.recommendations[:18]:
            if y < 72:
                pdf.showPage()
                y = height - 64
            pdf.drawString(48, y, f"- {recommendation.title}: {recommendation.remediation[:90]}")
            y -= 14

        pdf.save()
        return buffer.getvalue()
