"""ReportLab PDF certificate generation with QR code."""

from __future__ import annotations

import io
from datetime import datetime
from typing import Any

import qrcode
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from app.config import Settings, get_settings
from app.core.exceptions import ServiceError
from app.db.queries import passport as passport_q
from app.db.queries import users as users_q
from app.services.document_service import upload_to_storage_sync

# In-memory certificate job status (passport_id -> status)
_certificate_jobs: dict[str, dict[str, Any]] = {}


def get_certificate_status(certificate_id: str) -> dict[str, Any]:
    job = _certificate_jobs.get(certificate_id)
    if not job:
        return {"id": certificate_id, "status": "not_found", "download_url": None}
    return job


def _verification_label(status: str) -> str:
    return {
        "ai_provisional": "AI Provisional",
        "community_verified": "Community Verified",
        "master_verified": "Master Verified",
    }.get(status, status)


def generate_certificate_pdf(
    supabase: Any,
    user_id: str,
    *,
    settings: Settings | None = None,
) -> dict[str, Any]:
    s = settings or get_settings()
    passport = passport_q.get_passport_by_user(supabase, user_id)
    if not passport:
        raise ServiceError("Passport not found", 404)

    passport_id = passport["id"]
    _certificate_jobs[passport_id] = {"id": passport_id, "status": "processing", "download_url": None}

    user = users_q.get_user_by_id(supabase, user_id) or {}
    skills = passport_q.get_skills(supabase, passport_id)

    styles = getSampleStyleSheet()
    story: list[Any] = []

    story.append(Paragraph("<b>KaushalPass</b>", styles["Title"]))
    story.append(Paragraph("Digital Skill Passport", styles["Heading2"]))
    story.append(Spacer(1, 0.5 * cm))
    story.append(
        Paragraph(
            f"<b>{user.get('full_name') or 'Skill Holder'}</b>",
            styles["Heading1"],
        )
    )
    issued = passport.get("issued_at", "")
    if isinstance(issued, str) and "T" in issued:
        issued = issued.split("T")[0]
    story.append(Paragraph(f"Issued: {issued}", styles["Normal"]))
    if user.get("occupation_category"):
        story.append(Paragraph(f"Occupation: {user['occupation_category']}", styles["Normal"]))
    story.append(Paragraph(f"Passport Code: {passport['passport_code']}", styles["Normal"]))
    story.append(Spacer(1, 0.8 * cm))

    table_data = [["Skill Name", "Level", "NSQF Level", "Verified By"]]
    for sk in skills:
        table_data.append(
            [
                sk["skill_name"],
                sk["skill_level"],
                str(sk["nsqf_level"]),
                _verification_label(sk["verification_status"]),
            ]
        )
    if len(table_data) == 1:
        table_data.append(["—", "—", "—", "—"])

    table = Table(table_data, colWidths=[6 * cm, 3 * cm, 3 * cm, 4 * cm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4F46E5")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F3F4F6")]),
            ]
        )
    )
    story.append(table)
    story.append(Spacer(1, 1 * cm))

    verify_url = f"{s.APP_URL.rstrip('/')}/verify/{passport_id}"
    story.append(
        Paragraph(
            f"Verify at kaushalpass.in/verify/{passport['passport_code']}",
            styles["Normal"],
        )
    )

    # QR overlay on PDF via canvas callback
    qr = qrcode.QRCode(version=1, box_size=4, border=2)
    qr.add_data(verify_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_buffer = io.BytesIO()
    qr_img.save(qr_buffer, format="PNG")
    qr_bytes = qr_buffer.getvalue()

    # Rebuild with QR on last page using canvas callback
    buffer2 = io.BytesIO()
    doc2 = SimpleDocTemplate(buffer2, pagesize=A4, rightMargin=2 * cm, leftMargin=2 * cm)

    def _add_qr(canvas: Any, _doc: Any) -> None:
        from reportlab.lib.utils import ImageReader

        canvas.saveState()
        canvas.drawImage(
            ImageReader(io.BytesIO(qr_bytes)),
            A4[0] - 5 * cm,
            1.5 * cm,
            width=3.5 * cm,
            height=3.5 * cm,
        )
        canvas.restoreState()

    doc2.build(story, onFirstPage=_add_qr, onLaterPages=_add_qr)
    pdf_bytes = buffer2.getvalue()

    storage_path = f"{passport_id}.pdf"
    upload_to_storage_sync(
        supabase,
        s.CERTIFICATES_BUCKET,
        storage_path,
        pdf_bytes,
        "application/pdf",
        s,
    )
    signed = supabase.storage.from_(s.CERTIFICATES_BUCKET).create_signed_url(
        storage_path,
        s.STORAGE_SIGNED_URL_EXPIRY_SECONDS,
    )
    download_url = signed.get("signedURL") or signed.get("signedUrl") or ""

    result = {
        "id": passport_id,
        "status": "completed",
        "download_url": download_url,
        "passport_code": passport["passport_code"],
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }
    _certificate_jobs[passport_id] = result
    return result
