"""
PDF Export Tool

Generates a professional interaction report for a doctor visit.

Produces a formatted text report in all cases. When the optional
`reportlab` library is installed, also generates real PDF bytes that
can be returned as a file download from the API.

Uses the existing InteractionRepository — no raw SQLAlchemy queries here.
"""

import logging
from datetime import datetime
from io import BytesIO

from sqlalchemy.orm import Session

from app.repositories.repositories import InteractionRepository

logger = logging.getLogger(__name__)


class PDFTool:
    """
    Generate a professional HCP interaction report.

    Text report is always produced. PDF bytes are produced when reportlab
    is available; otherwise pdf_content is None (non-blocking degradation).
    """

    def __init__(self, db: Session) -> None:
        self.repo = InteractionRepository(db)

    def run(self, user_id: int, interaction_id: int | None = None) -> dict:
        """
        Fetch an interaction and build a formatted report.

        Parameters
        ----------
        user_id : int
            The authenticated representative's ID.
        interaction_id : int | None
            Specific interaction to export. Defaults to the most recent one.

        Returns
        -------
        dict
            Keys: reply (text report), pdf_content (bytes|None),
                  merged_draft, missing_fields, warnings, intent.
        """
        if interaction_id:
            interaction = self.repo.get_for_user(interaction_id, user_id)
            if not interaction:
                return self._error_result("Interaction not found or access denied.")
        else:
            interactions = self.repo.list_for_user(user_id, limit=1)
            if not interactions:
                return self._error_result("No interactions found to export.")
            interaction = interactions[0]

        text_report = self._build_text_report(interaction)
        pdf_bytes = self._try_generate_pdf(interaction)

        hint = "" if pdf_bytes else "\n\n(Install reportlab for PDF download support.)"
        return {
            "reply": text_report + hint,
            "pdf_content": pdf_bytes,
            "merged_draft": {},
            "missing_fields": [],
            "warnings": [],
            "intent": "pdf",
        }

    @staticmethod
    def _build_text_report(interaction) -> str:
        """Build a structured ASCII text report."""
        products = ", ".join(p.product_name for p in interaction.products) or "None"
        separator = "═" * 50
        return (
            f"{separator}\n"
            f"  HCP INTERACTION REPORT\n"
            f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
            f"{separator}\n\n"
            f"DOCTOR\n"
            f"  Name            : {interaction.doctor.name}\n"
            f"  Specialization  : {interaction.doctor.specialization or 'N/A'}\n"
            f"  Hospital        : {interaction.doctor.hospital or 'N/A'}\n"
            f"  City            : {interaction.doctor.city or 'N/A'}\n\n"
            f"INTERACTION\n"
            f"  Date            : {interaction.date}\n"
            f"  Time            : {interaction.time or 'N/A'}\n"
            f"  Type            : {interaction.interaction_type}\n"
            f"  Attendees       : {interaction.attendees or 'N/A'}\n"
            f"  Sentiment       : {interaction.sentiment or 'N/A'}\n"
            f"  Products        : {products}\n\n"
            f"DISCUSSION\n"
            f"  Topics          : {interaction.topics or 'N/A'}\n"
            f"  Materials       : {interaction.materials or 'N/A'}\n"
            f"  Samples         : {interaction.samples or 'N/A'}\n\n"
            f"SUMMARY\n"
            f"  {interaction.summary}\n\n"
            f"OUTCOMES\n"
            f"  {interaction.outcomes or 'N/A'}\n\n"
            f"FOLLOW-UP\n"
            f"  {interaction.followup or 'N/A'}\n"
            f"{separator}\n"
        )

    @staticmethod
    def _try_generate_pdf(interaction) -> bytes | None:
        """Attempt PDF generation with reportlab; return None if unavailable."""
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.lib.units import inch
            from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
            from reportlab.lib import colors

            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.75 * inch)
            styles = getSampleStyleSheet()
            story = []

            story.append(Paragraph("HCP Interaction Report", styles["Title"]))
            story.append(Spacer(1, 12))

            products = ", ".join(p.product_name for p in interaction.products) or "None"
            data = [
                ["Doctor", interaction.doctor.name],
                ["Specialization", interaction.doctor.specialization or "N/A"],
                ["Hospital", interaction.doctor.hospital or "N/A"],
                ["Date", str(interaction.date)],
                ["Type", interaction.interaction_type],
                ["Sentiment", interaction.sentiment or "N/A"],
                ["Products", products],
            ]
            table = Table(data, colWidths=[2 * inch, 4.5 * inch])
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("PADDING", (0, 0), (-1, -1), 6),
            ]))
            story.append(table)
            story.append(Spacer(1, 12))
            story.append(Paragraph("<b>Summary</b>", styles["Heading2"]))
            story.append(Paragraph(interaction.summary, styles["Normal"]))
            if interaction.outcomes:
                story.append(Spacer(1, 8))
                story.append(Paragraph("<b>Outcomes</b>", styles["Heading2"]))
                story.append(Paragraph(interaction.outcomes, styles["Normal"]))
            if interaction.followup:
                story.append(Spacer(1, 8))
                story.append(Paragraph("<b>Follow-up</b>", styles["Heading2"]))
                story.append(Paragraph(interaction.followup, styles["Normal"]))

            doc.build(story)
            return buffer.getvalue()

        except ImportError:
            logger.debug("reportlab not installed; PDF bytes skipped")
            return None
        except Exception as exc:
            logger.warning("PDF generation failed: %s", exc)
            return None

    @staticmethod
    def _error_result(reply: str) -> dict:
        return {
            "reply": reply,
            "pdf_content": None,
            "merged_draft": {},
            "missing_fields": [],
            "warnings": [],
            "intent": "pdf",
        }
