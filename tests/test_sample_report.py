"""The published sample report and the findings showcase."""
import hashlib
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "build"))
import package_release  # noqa: E402
import server  # noqa: E402

PUBLIC = ROOT / "public"
SAMPLE = PUBLIC / server.SAMPLE_REPORT
PAGE = (PUBLIC / "index.html").read_text(encoding="utf-8")


def client():
    return server.create_app({"FORM_SECRET": "test-secret", "SENDER": [].append}).test_client()


def test_sample_report_is_the_reviewed_file():
    assert SAMPLE.name == "Netopty_Sample_Network_As-Built_Report.pdf"
    data = SAMPLE.read_bytes()
    assert data.startswith(b"%PDF-")
    approved = package_release.APPROVED_DOCUMENTS["public/" + server.SAMPLE_REPORT]
    assert hashlib.sha256(data).hexdigest() == approved      # re-review before changing this file


def test_only_the_sample_report_is_a_document():
    docs = [p.relative_to(ROOT).as_posix() for p in PUBLIC.rglob("*")
            if p.is_file() and p.suffix.lower() not in package_release.ALLOWED_PUBLIC]
    assert docs == list(package_release.APPROVED_DOCUMENTS)


def test_sample_report_downloads_as_an_attachment():
    r = client().get("/" + server.SAMPLE_REPORT)
    assert r.status_code == 200
    assert r.mimetype == "application/pdf"
    assert r.headers["Content-Disposition"] == 'attachment; filename="Netopty_Sample_Network_As-Built_Report.pdf"'
    assert r.headers["X-Content-Type-Options"] == "nosniff"
    assert r.headers["Cache-Control"] == "public, max-age=86400"
    assert r.data == SAMPLE.read_bytes()


@pytest.mark.parametrize("path", ["/samples/other.pdf", "/samples/netopty_sample_network_as-built_report.PDF",
                                  "/img/x.pdf", "/samples/../samples/Netopty_Sample_Network_As-Built_Report.pdf"])
def test_no_other_pdf_path_is_served(path):
    assert client().get(path).status_code == 404


def test_packaging_refuses_an_unreviewed_sample(monkeypatch):
    monkeypatch.setitem(package_release.APPROVED_DOCUMENTS, "public/" + server.SAMPLE_REPORT, "0" * 64)
    with pytest.raises(SystemExit, match="differs from the reviewed version"):
        package_release.collect()


def test_packaging_includes_the_reviewed_sample():
    files = {p.relative_to(ROOT).as_posix() for p in package_release.collect()}
    assert "public/" + server.SAMPLE_REPORT in files


def test_download_button_needs_no_registration_and_does_not_preload():
    link = re.search(r'<a [^>]*href="/samples/Netopty_Sample_Network_As-Built_Report\.pdf"[^>]*>(.*?)</a>', PAGE, re.S)
    assert link and "Download full sample report" in link.group(1)
    assert "download" in link.group(0)
    start = PAGE.index('id="sample-reports"')
    block = PAGE[start:PAGE.index('</section>', start)]
    assert link.group(0) in block
    assert "No registration" in block
    # The PDF loads only when asked for: not embedded, framed, preloaded or prefetched.
    assert not re.search(r'<(iframe|embed|object)[^>]*\.pdf', PAGE)
    assert not re.search(r'<link[^>]*\.pdf', PAGE)


def test_findings_showcase():
    i = PAGE.index('id="findings"')
    block = PAGE[i:PAGE.index("</section>", i)]
    assert "More than documentation. Actionable network insights." in block
    for title in ("Identify configuration issues", "Understand the evidence", "Plan improvements"):
        assert f"<h3>{title}</h3>" in block
    assert "synthetic" in block                              # the sample's findings are from the fictional network
    assert "not a security audit" in block                   # qualified, not overstated


def test_no_tracking_on_the_download():
    assert not re.search(r"(?i)google-analytics|googletagmanager|gtag\(|plausible|matomo|segment\.com|hotjar", PAGE)
    assert 'href="/samples/' in PAGE and "onclick" not in PAGE
