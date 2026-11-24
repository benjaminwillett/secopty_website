"""Render the illustrative Secopty report pages shown on the homepage (synthetic Riverside Technology Group data).

Usage: python build/make_report_previews.py <repo root> <work folder>
Writes public/img/hero/*.webp and public/img/gallery/*.webp. Needs Playwright (Chromium) and Pillow.
"""
import sys
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

repo = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
work.mkdir(parents=True, exist_ok=True)
fonts = (repo / "public/fonts").as_uri()

SHIELD = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="{s}" height="{s}"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#a78bfa"/><stop offset="1" stop-color="#6d28d9"/></linearGradient></defs><path d="M32 4 L55 12 V30 C55 45 45 56 32 60 C19 56 9 45 9 30 V12 Z" fill="url(#g)"/><path d="M21 32 L29 40 L44 23" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>"""

CSS = """
@font-face{font-family:Inter;src:url(%(f)s/inter-latin-var.woff2);font-weight:100 900}
@font-face{font-family:Poppins;src:url(%(f)s/poppins-latin-500.woff2);font-weight:500}
@font-face{font-family:Poppins;src:url(%(f)s/poppins-latin-600.woff2);font-weight:600}
*{box-sizing:border-box}
body{margin:0;font:400 13px/1.45 Inter,sans-serif;color:#221a38;background:#fff}
.page{display:flex;flex-direction:column;padding:38px 46px 26px;background:#fff;overflow:hidden}
.hdr{display:flex;justify-content:space-between;align-items:center;padding-bottom:12px;border-bottom:2px solid #6d28d9}
.logo{display:flex;align-items:center;gap:8px;font:600 19px/1 Poppins;color:#2a1454}
.hdr .ctx{font-size:11.5px;color:#6b6385;letter-spacing:.04em}
.pill{font:600 10px/1 Inter;letter-spacing:.12em;text-transform:uppercase;color:#5b21b6;border:1.5px solid #8b5cf6;border-radius:5px;padding:7px 11px;background:#f5f3ff}
.kicker{font:600 11px/1 Inter;letter-spacing:.16em;text-transform:uppercase;color:#6d28d9;margin:22px 0 8px}
h1{font:600 27px/1.15 Poppins;color:#1c1033;margin:0}
h2{font:600 15px/1.2 Poppins;color:#1c1033;margin:20px 0 8px}
.lead{color:#544a6e;margin-top:8px;max-width:760px;font-size:13.5px}
.ftr{margin-top:auto;padding-top:10px;border-top:1px solid #ddd6f3;display:flex;justify-content:space-between;font-size:10.5px;color:#6b6385}
.tiles{display:grid;gap:12px;margin-top:16px}
.tile{border:1px solid #ddd6f3;border-radius:8px;padding:12px 14px;background:#faf8ff}
.tile b{display:block;font:600 26px/1 Poppins;color:#5b21b6}
.tile span{display:block;margin-top:6px;font-size:11.5px;color:#544a6e}
.tile.warn b{color:#b9650f}.tile.bad b{color:#b42318}
table{width:100%;border-collapse:collapse;font-size:12px}
th{text-align:left;font:600 10.5px/1.2 Inter;letter-spacing:.08em;text-transform:uppercase;color:#4c3f6b;background:#f1edfb;padding:8px 10px;border-bottom:1px solid #cfc5ee}
td{padding:8px 10px;border-bottom:1px solid #e6e0f5;vertical-align:top}
.mono{font-family:Consolas,"Cascadia Mono",monospace;font-size:11.5px}
.b{display:inline-block;font:700 9.5px/1 Inter;letter-spacing:.07em;text-transform:uppercase;color:#fff;border-radius:4px;padding:4px 7px;white-space:nowrap}
.high{background:#b42318}.med{background:#b9650f}.low{background:#6b7280}.ok{background:#18794e}.ver{background:#fff;color:#8a5a00;border:1px solid #d6a23a}.vio{background:#6d28d9}
.call{border-left:5px solid #d6a23a;background:#fdf6e3;padding:11px 14px;border-radius:0 6px 6px 0;margin-top:16px}
.call b{display:block;font:600 11px/1.2 Inter;letter-spacing:.08em;text-transform:uppercase;color:#7a4f00;margin-bottom:3px}
.call.v{border-color:#6d28d9;background:#f5f3ff}.call.v b{color:#5b21b6}
.cols{display:grid;gap:26px}
.muted{color:#6b6385}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
.chip{border:1px solid #cfc5ee;border-radius:999px;padding:5px 11px;font-size:11.5px;color:#3d3158;background:#fff}
.chip.on{background:#6d28d9;border-color:#6d28d9;color:#fff}
.bar{display:flex;height:16px;border-radius:4px;overflow:hidden;background:#f1edfb}
.bar i{display:block;height:100%}
.legend{display:flex;gap:16px;font-size:11px;color:#544a6e;margin-top:10px}
.legend i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:5px;vertical-align:-1px}
.dot{display:inline-block;width:13px;height:13px;border-radius:50%%}
.d-ok{background:#18794e}.d-bad{background:#b42318}.d-gap{background:#fff;border:2px dashed #b9650f}
.mx td,.mx th{text-align:center;padding:9px 6px}.mx td:first-child,.mx th:first-child{text-align:left}
.cell{display:block;border-radius:5px;padding:6px 4px;font:600 10.5px/1 Inter}
.c-p{background:#ede9fe;color:#4c1d95}.c-n{background:#f3f4f6;color:#6b7280}.c-v{background:#fdf0cf;color:#7a4f00;border:1px solid #d6a23a}.c-s{color:#b8b0cc}
""".replace("%(f)s", fonts).replace("%%", "%")


def chrome(kind, body, w, h, page_no, ctx="Network Security &amp; Compliance · RTG-HQ"):
    return f"""<!doctype html><meta charset="utf-8"><style>{CSS}.page{{width:{w}px;height:{h}px}}</style>
<div class="page {kind}"><div class="hdr"><div class="logo">{SHIELD.format(s=24)}Secopty</div><div class="ctx">{ctx}</div></div>
{body}
<div class="ftr"><span>Illustrative preview · synthetic data · Riverside Technology Group is a fictional organisation</span><span>{page_no}</span></div></div>"""


def rows(data):
    return "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in data)


def head(cols):
    return "<tr>" + "".join(f"<th>{c}</th>" for c in cols) + "</tr>"


B = lambda cls, text: f'<span class="b {cls}">{text}</span>'
M = lambda t: f'<span class="mono">{t}</span>'

# ---------------------------------------------------------------- portrait pages (A4 at 96 dpi)
PW, PH = 794, 1123

cover = f"""<!doctype html><meta charset="utf-8"><style>{CSS}
.page{{width:{PW}px;height:{PH}px;padding:0}}
.top{{padding:64px 62px 0;display:flex;justify-content:space-between;align-items:center}}
.top .logo{{font-size:30px;gap:12px}}
.band{{margin-top:190px;background:#1c1033;color:#fff;padding:44px 62px 48px;border-bottom:6px solid #8b5cf6}}
.band .k{{font:600 11.5px/1 Inter;letter-spacing:.18em;text-transform:uppercase;color:#c4b5fd;border-top:3px solid #8b5cf6;display:inline-block;padding-top:12px}}
.band h1{{color:#fff;font-size:46px;margin-top:20px}}
.band p{{margin:10px 0 0;font-size:16px;color:#e4dcf7}}
.band p.o{{font:600 17px/1.2 Poppins;color:#fff;margin-top:14px}}
.meta{{margin:auto 62px 70px;width:auto}}
.meta td{{padding:10px 0;font-size:12.5px;border-bottom:1px solid #e6e0f5}}
.meta td:first-child{{width:170px;font-weight:600;color:#3d3158}}
</style><div class="page"><div class="top"><div class="logo">{SHIELD.format(s=40)}Secopty</div><span class="pill">Illustrative preview · synthetic data</span></div>
<div class="band"><span class="k">Network security &amp; compliance report</span><h1>RTG-HQ</h1><p class="o">Riverside Technology Group</p><p>Vulnerabilities, firewall policy, device hardening, segmentation and vendor support</p></div>
<div class="meta"><table>{rows([
    ["Site", "RTG-HQ"],
    ["Organisation", "Riverside Technology Group"],
    ["Document", "Network Security and Compliance Report"],
    ["Scope", "20 switches and 2 firewalls"],
    ["Evidence collected", "20 Oct 2026, authorised read-only exports"],
    ["Report sections", "Five reports, with audit evidence and coverage"],
    ["Review status", "Not reviewed: illustrative layout"],
    ["Classification", "Public preview: synthetic data, fictional organisation"],
])}</table></div></div>"""

BARS = [  # report, high, medium, low, verify
    ("Vulnerabilities and upgrades", 2, 2, 0, 2),
    ("Firewall policy review", 1, 2, 1, 0),
    ("Device hardening", 1, 3, 1, 1),
    ("Network segmentation", 0, 0, 0, 2),
    ("End-of-life and vendor support", 1, 2, 0, 0),
]
UNIT = 26
bar_rows = "".join(
    f"""<tr><td style="width:215px">{n}</td><td><div class="bar" style="width:{(h + m + l + v) * UNIT}px">
<i class="high" style="width:{h * UNIT}px"></i><i class="med" style="width:{m * UNIT}px"></i><i class="low" style="width:{l * UNIT}px"></i><i style="width:{v * UNIT}px;background:#f3d488"></i></div></td>
<td style="width:44px;text-align:right;font-weight:600">{h + m + l + v}</td></tr>"""
    for n, h, m, l, v in BARS)
tot = [sum(b[i] for b in BARS) for i in (1, 2, 3, 4)]

overview = chrome("", f"""
<p class="kicker">Section 1</p><h1>Assessment overview</h1>
<div class="tiles" style="grid-template-columns:repeat(4,1fr)">
<div class="tile"><b>22</b><span>devices in scope</span></div>
<div class="tile bad"><b>{tot[0]}</b><span>high-severity findings</span></div>
<div class="tile"><b>{tot[0] + tot[1] + tot[2]}</b><span>findings in total</span></div>
<div class="tile warn"><b>{tot[3]}</b><span>items needing verification</span></div></div>
<h2>Findings by report</h2>
<table>{bar_rows}</table>
<div class="legend"><span><i class="high"></i>High</span><span><i class="med"></i>Medium</span><span><i class="low"></i>Low</span><span><i style="background:#f3d488"></i>Needs verification</span></div>
<h2>Audit evidence and coverage</h2>
<table>{head(["Evidence", "Source", "Collected", "Coverage"])}{rows([
    ["Device inventory and software versions", "Inventory export", "20 Oct 2026", B("ok", "Complete")],
    ["Switch configurations", "Read-only export, 20 devices", "20 Oct 2026", B("ok", "Complete")],
    ["Firewall rulebase, NAT and routes", "Read-only export, 2 devices", "20 Oct 2026", B("ok", "Complete")],
    ["Approved account register", "Supplied by RTG", "14 Oct 2026", B("ok", "Complete")],
    ["Central authentication groups", "Identity system", "Not supplied", B("ver", "Evidence gap")],
    ["Documented network boundaries", "Supplied by RTG", "Draft only", B("ver", "Partial")],
])}</table>
<p class="muted" style="margin-top:8px;font-size:11.5px">Where evidence was not supplied, the related checks are marked as needing verification and do not count as passed.</p>
<h2>Priority actions</h2>
<table>{head(["#", "Action", "Section", "Severity"])}{rows([
    ["1", "Upgrade the core switches to a supported release that fixes the applicable advisories", "2 and 6", B("high", "High")],
    ["2", "Restrict rule 31, which allows the guest network to reach any destination on HTTPS", "3", B("high", "High")],
    ["3", "Confirm the owner of the local administrator account rtg-legacy", "4", B("high", "High")],
    ["4", "Plan replacement of access switches nearing the end of security updates", "6", B("med", "Medium")],
])}</table>""", PW, PH, "Page 3")

hard_p = chrome("", f"""
<p class="kicker">Section 4 · Device hardening</p><h1>User accounts and admin access</h1>
<p class="lead">Local accounts found in the collected configurations, compared with the approved account register supplied by Riverside Technology Group.</p>
<div class="tiles" style="grid-template-columns:repeat(3,1fr)">
<div class="tile"><b>3</b><span>local accounts across 22 devices</span></div>
<div class="tile"><b>2</b><span>match the approved register</span></div>
<div class="tile bad"><b>1</b><span>administrator with no verified owner</span></div></div>
<h2>Local account inventory</h2>
<table>{head(["Account", "Privilege", "Found on", "Register", "Review status"])}{rows([
    [M("rtg-emergency"), "Administrator", "22 devices", "Listed", B("ok", "Approved emergency access")],
    [M("rtg-legacy"), "Administrator", M("c9300-hq-a04"), "Not listed", B("high", "Owner requires verification")],
    [M("rtg-monitor"), "Read-only", "22 devices", "Listed", B("ok", "Approved monitoring")],
])}</table>
<div class="call"><b>Central access needs separate evidence</b>TACACS+ is configured on all 22 devices. Central group membership and assigned privileges were not supplied and are not assessed here.</div>
<h2>Finding</h2>
<table>{rows([
    ["<b>Finding</b>", "Privileged local account with no verified owner " + B("high", "High")],
    ["<b>Affected</b>", M("c9300-hq-a04") + ", headquarters access switch"],
    ["<b>Evidence</b>", "Redacted device configuration, line 212, and the approved account register dated 14 Oct 2026"],
    ["<b>Why it matters</b>", "An administrator account outside the register can change the device without central authentication."],
    ["<b>Recommended action</b>", "Confirm the owner. Remove the account, or add it to the register as an approved exception."],
])}</table>
<h2>Management access baseline</h2>
<table>{head(["Check", "Result", "Devices"])}{rows([
    ["SSH only for remote management", B("ok", "Met"), "22 of 22"],
    ["Management access limited to approved addresses", B("med", "Not met"), "8 switches have no restriction"],
    ["Logging sent to the central collector", B("ok", "Met"), "22 of 22"],
])}</table>""", PW, PH, "Page 21")

# ---------------------------------------------------------------- landscape figures
LW, LH = 1200, 760

vuln = chrome("", f"""
<p class="kicker">Section 2 · Vulnerabilities and upgrades</p><h1>Applicable advisories and target releases</h1>
<div class="tiles" style="grid-template-columns:repeat(4,1fr)">
<div class="tile"><b>22</b><span>devices matched to vendor advisories by model and installed software</span></div>
<div class="tile bad"><b>4</b><span>findings where a supported release fixes the advisory</span></div>
<div class="tile warn"><b>2</b><span>findings that need manual verification of a feature or setting</span></div>
<div class="tile"><b>3</b><span>target releases cover every applicable advisory listed</span></div></div>
<h2>Advisories by device group</h2>
<table>{head(["Devices", "Model", "Installed", "Advisory", "Severity", "Supported target release", "Status"])}{rows([
    [M("c9500-hq-c01, c02"), "C9500-24Y4C", M("17.6.4"), M("CVE-2099-10432"), B("high", "High"), M("17.12.x"), B("vio", "Fix available")],
    [M("c9500-hq-c01, c02"), "C9500-24Y4C", M("17.6.4"), M("CVE-2099-10518"), B("high", "High"), M("17.12.x"), B("vio", "Fix available")],
    [M("c9300-hq-a01 to a10"), "C9300-48P", M("17.9.3"), M("CVE-2099-10518"), B("med", "Medium"), M("17.12.x"), B("vio", "Fix available")],
    [M("c9300-hq-a01 to a10"), "C9300-48P", M("17.9.3"), M("CVE-2099-11207"), B("med", "Medium"), M("17.12.x"), B("ver", "Verify: web UI enabled?")],
    [M("vsp5420-hq-a09 to a16"), "5420M-48W-4YE", M("8.10.1"), M("CVE-2099-12066"), B("med", "Medium"), M("9.1.x"), B("vio", "Fix available")],
    [M("pa3410-hq-f01, f02"), "PA-3410", M("11.1.2"), M("CVE-2099-13391"), B("low", "Low"), M("11.1.6"), B("ver", "Verify: portal in use?")],
])}</table>
<div class="call v"><b>How to read this page</b>An advisory is listed when the device model and installed software fall inside the vendor's affected range. Where the vendor says exposure depends on a feature or setting, the row is marked for manual verification.</div>
<p class="muted" style="margin-top:10px;font-size:11px">Advisory identifiers and software releases on this page are placeholders.</p>""", LW, LH, "Page 9")

fw = chrome("", f"""
<p class="kicker">Section 3 · Firewall policy review</p><h1>Rulebook in plain English</h1>
<p class="lead">Source: {M("pa3410-hq-f01")}, Palo Alto Networks PAN-OS, 42 security rules. Each row links back to the original rule.</p>
<div class="chips"><span class="chip">Source: any</span><span class="chip">Destination: any</span><span class="chip">Service: any</span><span class="chip on">Action: allow</span><span class="chip on">Logging: all</span><span class="chip">Showing 6 of 42 rules</span></div>
<h2>Rules</h2>
<table>{head(["Rule", "What it does", "Source", "Destination", "Service", "Action", "Logged", "Review"])}{rows([
    [M("12"), "Staff workstations can reach the data-centre applications over HTTPS", "Corp-Users", "DC-Apps", M("tcp/443"), "Allow", "Yes", B("ok", "No issue")],
    [M("14"), "Network administrators can manage switches and firewalls over SSH", "Mgmt-Jump", "Net-Mgmt", M("tcp/22"), "Allow", "Yes", B("ok", "No issue")],
    [M("19"), "Building systems can reach their vendor's update service", "Building-Sys", "Vendor-Update", M("tcp/443"), "Allow", "No", B("med", "Not logged")],
    [M("27"), "Servers can reach any internet address on any port", "DC-Apps", "Internet", M("any"), "Allow", "Yes", B("med", "Any service")],
    [M("31"), "Guest Wi-Fi can reach any destination over HTTPS, including internal networks", "Guest-WiFi", "any", M("tcp/443"), "Allow", "Yes", B("high", "Any destination")],
    [M("38"), "Printers can send scans to the file server", "Printers", "File-Srv", M("tcp/445"), "Allow", "No", B("low", "Not logged")],
])}</table>
<div class="call"><b>Finding · rule 31</b>The destination is "any", so the guest network is not limited to the internet. Restrict the destination to the internet zone, then confirm with the segmentation report.</div>""", LW, LH, "Page 14")

CHECKS = [
    ("SSH only for remote management", "ok ok ok ok"),
    ("Management access limited to approved addresses", "ok ok bad ok"),
    ("Session timeout set on management lines", "ok bad bad ok"),
    ("Logging sent to the central collector", "ok ok ok ok"),
    ("Time synchronised to approved NTP servers", "ok ok bad ok"),
    ("SNMP v3 only, no default community strings", "ok ok ok ok"),
    ("Central authentication configured (TACACS+)", "ok ok ok ok"),
    ("Central group membership and privileges", "gap gap gap gap"),
    ("Login banner present", "ok ok ok bad"),
]
check_rows = "".join(
    f"<tr><td>{n}</td>" + "".join(f'<td><span class="dot d-{s}"></span></td>' for s in st.split()) + "</tr>"
    for n, st in CHECKS)
hard = chrome("", f"""
<p class="kicker">Section 4 · Device hardening</p><h1>Baseline results by device group</h1>
<p class="lead">Settings read from the collected configurations and compared with the baseline agreed with Riverside Technology Group.</p>
<div class="cols" style="grid-template-columns:1.55fr 1fr;margin-top:6px">
<div><h2>Baseline checks</h2>
<table class="mx"><tr><th>Check</th><th>Core switches<br>2</th><th>Access, Cisco<br>10</th><th>Access, Extreme<br>8</th><th>Firewalls<br>2</th></tr>{check_rows}</table>
<div class="legend"><span><span class="dot d-ok" style="width:10px;height:10px;margin-right:5px"></span>Met on every device</span><span><span class="dot d-bad" style="width:10px;height:10px;margin-right:5px"></span>Not met on one or more</span><span><span class="dot d-gap" style="width:10px;height:10px;margin-right:5px"></span>Evidence not supplied</span></div></div>
<div><h2>Local accounts</h2>
<table>{head(["Account", "Privilege", "Status"])}{rows([
    [M("rtg-emergency"), "Administrator", B("ok", "Approved")],
    [M("rtg-legacy"), "Administrator", B("high", "Owner unverified")],
    [M("rtg-monitor"), "Read-only", B("ok", "Approved")],
])}</table>
<div class="tiles" style="grid-template-columns:1fr 1fr">
<div class="tile"><b>27</b><span>of 36 checks met</span></div>
<div class="tile warn"><b>4</b><span>checks without evidence</span></div></div>
<div class="call"><b>Evidence gap</b>TACACS+ is configured. Group membership and assigned privileges need evidence from the identity system.</div></div></div>""", LW, LH, "Page 20")

ZONES = ["Corporate", "Guest Wi-Fi", "Building systems", "Servers", "Management", "Internet"]
MATRIX = {
    "Corporate": "s n n p n p",
    "Guest Wi-Fi": "v s n v n p",
    "Building systems": "n n s n n p",
    "Servers": "n n n s n p",
    "Management": "p n p p s n",
}
LAB = {"s": ("c-s", "–"), "n": ("c-n", "No path"), "p": ("c-p", "Permitted"), "v": ("c-v", "Verify")}
mx = "<tr><th>From \\ To</th>" + "".join(f"<th>{z}</th>" for z in ZONES) + "</tr>" + "".join(
    f"<tr><td><b>{src}</b></td>" + "".join(
        '<td><span class="cell {}">{}</span></td>'.format(*LAB[c]) for c in cells.split()) + "</tr>"
    for src, cells in MATRIX.items())
seg = chrome("", f"""
<p class="kicker">Section 5 · Network segmentation</p><h1>Paths between agreed boundaries</h1>
<p class="lead">Each cell combines firewall policy, routing and NAT evidence for traffic from one zone to another.</p>
<div class="cols" style="grid-template-columns:1.6fr 1fr;margin-top:4px">
<div><h2>Zone-to-zone matrix</h2><table class="mx">{mx}</table>
<div class="legend"><span><i style="background:#ede9fe;border:1px solid #c4b5fd"></i>Permitted by the evidence</span><span><i style="background:#f3f4f6;border:1px solid #d1d5db"></i>No permitted path found</span><span><i style="background:#fdf0cf;border:1px solid #d6a23a"></i>Needs verification against the agreed boundary</span></div>
<div class="tiles" style="grid-template-columns:repeat(3,1fr)">
<div class="tile"><b>25</b><span>zone pairs assessed</span></div>
<div class="tile"><b>8</b><span>pairs permitted by the evidence</span></div>
<div class="tile warn"><b>2</b><span>pairs needing verification</span></div></div></div>
<div><h2>Path needing verification</h2>
<table>{rows([
    ["<b>Path</b>", "Guest Wi-Fi to Servers"],
    ["<b>Policy</b>", "Rule " + M("31") + " allows " + M("tcp/443") + " to any destination"],
    ["<b>Routing</b>", "Route present through " + M("c9500-hq-c01")],
    ["<b>NAT</b>", "No translation applies"],
    ["<b>Agreed boundary</b>", "Guest traffic reaches the internet only (draft boundary document)"],
    ["<b>Status</b>", B("ver", "Needs verification")],
])}</table>
<div class="call"><b>Why it is not marked as a breach</b>The boundary document is a draft. Confirm the agreed boundary, then restrict rule 31.</div></div></div>""", LW, LH, "Page 27")

YEARS = [2026, 2027, 2028, 2029, 2030, 2031]
X0, YW = 0, 100 / len(YEARS)


def pct(year_frac):
    return (year_frac - YEARS[0]) * YW


LIFE = [  # label, count, end of security updates (year fraction), text, badge
    ("C9300-48P access switches", "10 devices", 2027.75, "Oct 2027", B("med", "Plan replacement")),
    ("C9500-24Y4C core switches", "2 devices", 2029.45, "Jun 2029", B("ok", "Supported")),
    ("5420M-48W-4YE access switches", "8 devices", 2030.2, "Mar 2030", B("ok", "Supported")),
    ("PA-3410 firewalls", "2 devices", 2031.6, "Aug 2031", B("ok", "Supported")),
    ("IOS-XE 17.6 on the core switches", "2 devices", 2026.2, "Mar 2026", B("high", "Upgrade now")),
    ("IOS-XE 17.9 on the access switches", "10 devices", 2027.2, "Mar 2027", B("med", "Plan upgrade")),
]
NOW = 2026.9
grid = "".join(f'<span style="position:absolute;left:{i * YW}%;top:0;bottom:0;border-left:1px solid #e6e0f5"></span>' for i in range(1, len(YEARS)))
life_rows = ""
for label, count, end, text, badge in LIFE:
    w = max(min(pct(end), 100), 0)
    colour = "#b42318" if end < NOW else ("#d08a1c" if end - NOW < 1.5 else "#8b5cf6")
    life_rows += f"""<tr><td style="width:250px"><b>{label}</b><br><span class="muted">{count}</span></td>
<td><div style="position:relative;height:26px;background:#faf8ff;border-radius:4px;overflow:hidden">{grid}
<span style="position:absolute;left:0;top:6px;height:14px;width:{w}%;background:{colour};border-radius:3px"></span>
<span style="position:absolute;left:{pct(NOW)}%;top:0;bottom:0;border-left:2px solid #1c1033"></span></div></td>
<td style="width:86px">{text}</td><td style="width:140px">{badge}</td></tr>"""
axis = "".join(f'<span style="flex:1;font-size:11px;color:#6b6385">{y}</span>' for y in YEARS)
life = chrome("", f"""
<p class="kicker">Section 6 · End-of-life and vendor support</p><h1>Security update timeline</h1>
<p class="lead">When security updates end for the hardware and software found at RTG-HQ, taken from vendor lifecycle notices.</p>
<div class="tiles" style="grid-template-columns:repeat(4,1fr)">
<div class="tile"><b>22</b><span>devices matched to a vendor lifecycle notice</span></div>
<div class="tile bad"><b>2</b><span>devices running software past the end of security updates</span></div>
<div class="tile warn"><b>10</b><span>devices within 18 months of the end of security updates</span></div>
<div class="tile"><b>12</b><span>devices with hardware supported into 2029 or later</span></div></div>
<h2>Security updates end</h2>
<table><tr><th>Hardware or software</th><th><div style="display:flex">{axis}</div></th><th>Ends</th><th>Priority</th></tr>{life_rows}</table>
<div class="legend"><span><i style="background:#1c1033;width:2px"></i>Assessment date, Nov 2026</span><span><i style="background:#b42318"></i>Ended</span><span><i style="background:#d08a1c"></i>Ends within 18 months</span><span><i style="background:#8b5cf6"></i>Supported</span></div>
<p class="muted" style="margin-top:12px;font-size:11px">Dates on this page are placeholders and are not vendor lifecycle data.</p>""", LW, 800, "Page 31")

PAGES = {
    "cover": (cover, PW, PH), "overview": (overview, PW, PH), "accounts": (hard_p, PW, PH),
    "vulnerabilities": (vuln, LW, LH), "firewall": (fw, LW, LH), "hardening": (hard, LW, LH),
    "segmentation": (seg, LW, LH), "lifecycle": (life, LW, 800),
}

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    for name, (html, w, h) in PAGES.items():
        src = work / f"{name}.html"
        src.write_text(html, encoding="utf-8")
        page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=2)
        page.goto(src.as_uri())
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(250)
        over = page.evaluate("(() => { const p = document.querySelector('.page'); return p.scrollHeight - p.clientHeight; })()")
        if over > 0:
            print("OVERFLOW", name, over)
        page.screenshot(path=str(work / f"{name}.png"), clip={"x": 0, "y": 0, "width": w, "height": h})
        page.close()
    browser.close()


def save(name, out, width):
    im = Image.open(work / f"{name}.png").convert("RGB")
    if width and width < im.width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out, "WEBP", quality=86, method=6)
    return im.size


img = repo / "public/img"
for src, dst in (("cover", "cover"), ("overview", "page2"), ("accounts", "page3")):
    for tag, width in (("480", 480), ("640", 640), ("1200", 1200), ("full", None)):
        print(dst, tag, save(src, img / f"hero/{dst}-{tag}.webp", width))
# Gallery thumbnails are a legible 3:2 crop from the top left of the page; the lightbox shows all of it.
CROP = {"vulnerabilities": 0.62, "firewall": 0.62, "hardening": 0.62, "segmentation": 0.78, "lifecycle": 0.78}
for name, frac in CROP.items():
    print(name, "full", save(name, img / f"gallery/{name}-full.webp", None))
    im = Image.open(work / f"{name}.png").convert("RGB")
    w = round(im.width * frac)
    crop = im.crop((0, 0, w, round(w / 1.5)))
    for width in (800, 1400):
        out = crop.resize((width, round(width / 1.5)), Image.LANCZOS)
        out.save(img / f"gallery/{name}-{width}.webp", "WEBP", quality=86, method=6)
        print(name, width, out.size)
