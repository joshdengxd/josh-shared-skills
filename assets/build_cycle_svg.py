"""Builds cycle.svg. Every text is width-checked against its box (conservative fonts) so nothing overflows."""
import os

try:
    from PIL import ImageFont
except ImportError:  # checks skipped if Pillow is missing
    ImageFont = None

W, H = 1280, 780
SANS = "Inter,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
INK, MUTED, LINE = "#1f2328", "#57606a", "#8c959f"
C = {"refine": "#E36209", "build": "#1F6FEB", "scale": "#0E8A8A", "ship": "#6B4FBB", "data": "#2EA44F", "base": "#57606a"}
TINT = {"refine": "#FFF8F2", "build": "#F4F8FF", "scale": "#F0FAFA", "ship": "#F8F5FF", "data": "#F2FBF4", "base": "#F6F8FA"}
o = []
a = o.append
problems = []

_fonts = {}


def width(text, size, bold=False, mono=False):
    if ImageFont is None:
        return 0
    name = ("courbd.ttf" if mono else ("arialbd.ttf" if bold else "arial.ttf"))
    key = (name, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(os.path.join(os.environ.get("WINDIR", "C:/Windows"), "Fonts", name), int(size * 4))
    return _fonts[key].getlength(text) / 4


def check(text, size, maxw, bold=False, mono=False):
    w = width(text, size, bold, mono)
    if w > maxw:
        problems.append("%r: %.0f > %.0f" % (text, w, maxw))


def text(x, y, s, size=12, color=MUTED, bold=False, mono=False, anchor="start", maxw=None, spacing=None):
    if maxw:
        check(s, size, maxw, bold, mono)
    ls = ' letter-spacing="%s"' % spacing if spacing else ""
    a('<text x="%s" y="%s" font-family="%s" font-size="%s"%s fill="%s" text-anchor="%s"%s>%s</text>'
      % (x, y, MONO if mono else SANS, size, ' font-weight="700"' if bold else "", color, anchor, ls, s))


def panel(x, y, w, h, n, title, k):
    a('<rect x="%s" y="%s" width="%s" height="%s" rx="14" fill="%s" stroke="%s" stroke-opacity="0.35"/>' % (x, y, w, h, TINT[k], C[k]))
    a('<circle cx="%s" cy="%s" r="11" fill="%s"/>' % (x + 24, y + 26, C[k]))
    text(x + 24, y + 30.5, n, 12, "#fff", True, anchor="middle")
    text(x + 43, y + 30.5, title, 12, C[k], True, maxw=w - 60, spacing=1.1)


def card(x, y, w, h, title, subs, k, mono=True, fill="#fff"):
    a('<rect x="%s" y="%s" width="%s" height="%s" rx="9" fill="%s" stroke="%s" stroke-opacity="0.5" filter="url(#sh)"/>' % (x, y, w, h, fill, C[k]))
    a('<rect x="%s" y="%s" width="4" height="%s" rx="2" fill="%s"/>' % (x + 1, y + 9, h - 18, C[k]))
    inner = w - 32
    if subs:
        text(x + 16, y + 22, title, 14, INK, True, mono, maxw=inner)
        for i, s in enumerate(subs):
            text(x + 16, y + 39 + i * 15, s, 12, MUTED, maxw=inner)
    else:
        text(x + 16, y + h / 2 + 5, title, 14, INK, True, mono, maxw=inner)


def pill(x, y, w, h, label, k, solid=False):
    if solid:
        a('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" filter="url(#sh)"/>' % (x, y, w, h, h / 2, C[k]))
        text(x + w / 2, y + h / 2 + 5, label, 13.5, "#fff", True, anchor="middle", maxw=w - 24)
    else:
        a('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="#fff" stroke="%s" stroke-dasharray="4 3"/>' % (x, y, w, h, h / 2, C[k]))
        text(x + w / 2, y + h / 2 + 4.5, label, 12, MUTED, anchor="middle", maxw=w - 24)


def arrow(d, k=None, dash=False):
    col = C[k] if k else LINE
    m = "m_" + (k or "n")
    a('<path d="%s" fill="none" stroke="%s" stroke-width="1.6"%s stroke-linejoin="round" marker-end="url(#%s)"/>'
      % (d, col, ' stroke-dasharray="5 4"' if dash else "", m))


# ---------- canvas ----------
a('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" role="img" '
  'aria-label="Delivery cycle: refine, build and evaluate, run at scale, ship, investigate with data, foundations">' % (W, H, W, H))
defs = ['<filter id="sh" x="-5%" y="-10%" width="110%" height="130%"><feDropShadow dx="0" dy="1.5" stdDeviation="2.5" flood-color="#1f2328" flood-opacity="0.08"/></filter>']
for k, col in list(C.items()) + [("n", LINE)]:
    defs.append('<marker id="m_%s" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="%s"/></marker>' % (k, col))
a("<defs>%s</defs>" % "".join(defs))
a('<rect x="0.5" y="0.5" width="%d" height="%d" rx="18" fill="#FFFFFF" stroke="#D0D7DE"/>' % (W - 1, H - 1))
text(32, 46, "Delivery cycle", 22, INK, True)
text(32, 70, "From a vague ticket to a production release. Independent agents, code and tests verify the work; a person takes the irreversible steps.", 13, MUTED, maxw=W - 64)

PY, PH = 96, 340
X1, W1 = 32, 250
X2, W2 = 318, 440
X3, W3 = 794, 454
Y0 = PY + 54

# ---------- 1 refine ----------
panel(X1, PY, W1, PH, "1", "REFINE", "refine")
ix, iw = X1 + 20, W1 - 40
for i, label in enumerate(["Epic or feature", "Spec: agent drafts, you approve"]):
    y = Y0 + i * 46
    pill(ix, y, iw, 32, label, "refine")
    arrow("M%s %s V%s" % (ix + iw / 2, y + 33, y + 44), "refine")
card(ix, Y0 + 2 * 46, iw, 32, "create-ticket", None, "refine")
arrow("M%s %s V%s" % (ix + iw / 2, Y0 + 2 * 46 + 33, Y0 + 2 * 46 + 44), "refine")
TR_Y = Y0 + 3 * 46
card(ix, TR_Y, iw, 62, "refine-ticket", ["Spec + acceptance criteria", "You approve the summary"], "refine")
text(X1 + W1 / 2, PY + PH - 18, "dashed: process step, no skill yet", 11, MUTED, anchor="middle", maxw=W1 - 24)

# ---------- 2 build / evaluate ----------
panel(X2, PY, W2, PH, "2", "BUILD, EVALUATE, IMPROVE", "build")
bx, bw = X2 + 20, W2 - 60
rows = [("implement-and-verify-ticket", ["Checks + e2e green; fresh agent checks each criterion"]),
        ("verify-against-criteria", ["Follow-up: read-only code review, with evidence"]),
        ("live-env-local-test", ["Follow-up: real environment, local build"])]
for i, (t, s) in enumerate(rows):
    y = Y0 + i * 78
    card(bx, y, bw, 58, t, s, "build")
    if i:
        arrow("M%s %s V%s" % (bx + bw / 2, y - 20 + 1, y - 2), "build")
loop_x = bx + bw + 12
arrow("M%s %s H%s V%s H%s" % (bx + bw, Y0 + 78 + 29, loop_x, Y0 + 29, bx + bw + 2), "build", dash=True)
text(X2 + W2 / 2, PY + PH - 36, "Not passing: findings go back to the implementer,", 11.5, C["build"], anchor="middle", maxw=W2 - 30)
text(X2 + W2 / 2, PY + PH - 20, "and every round gets a new verifier.", 11.5, C["build"], anchor="middle", maxw=W2 - 30)
# refine -> build
arrow("M%s %s H%s V%s H%s" % (ix + iw, TR_Y + 31, X1 + W1 + 18, Y0 + 29, bx - 2), "refine")

# ---------- 4 ship ----------
panel(X3, PY, W3, PH, "4", "SHIP", "ship")
sx, sw = X3 + 20, W3 - 40
card(sx, Y0, sw, 62, "Before merge: private environment",
     ["Branch build in a short-lived Kubernetes pod", "run-e2e-automation, plus manual QA by people"], "ship", mono=False)
MP_Y = Y0 + 76
pill(sx, MP_Y, sw, 34, "On land request: merge, deploy, re-check", "ship", solid=True)
arrow("M%s %s V%s" % (sx + sw / 2, Y0 + 63, MP_Y - 2), "ship")
half = (sw - 16) / 2
C_Y = MP_Y + 46
card(sx, C_Y, half, 58, "deploy-to-staging", ["Explicit tag, GitOps sync"], "ship")
card(sx + half + 16, C_Y, half, 58, "run-e2e-automation", ["Suite again on staging"], "ship")
arrow("M%s %s V%s H%s V%s" % (sx + sw / 2, MP_Y + 35, MP_Y + 42, sx + half / 2, C_Y - 2), "ship")
arrow("M%s %s H%s" % (sx + half, C_Y + 29, sx + half + 14), "ship")
D_Y = C_Y + 70
card(sx, D_Y, sw, 50, "prod-release-gate", ["Stop after each step; canary go / no-go"], "ship")
arrow("M%s %s V%s" % (sx + half + 16 + half / 2, C_Y + 59, D_Y - 2), "ship")
text(X3 + W3 / 2, PY + PH - 18, "Only a clean run is released. People perform every production action.", 11, MUTED, anchor="middle", maxw=W3 - 24)
# build -> ship
arrow("M%s %s H%s V%s H%s" % (bx + bw, Y0 + 156 + 29, X2 + W2 + 18, Y0 + 31, sx - 2), "build")
text(bx + bw + 6, Y0 + 156 + 22, "pass", 11, C["build"], True, maxw=40)

# ---------- 3 scale ----------
BY, BH = PY + PH + 22, 88
a('<rect x="%s" y="%s" width="%s" height="%s" rx="14" fill="%s" stroke="%s" stroke-opacity="0.35"/>' % (X2, BY, W2, BH, TINT["scale"], C["scale"]))
a('<circle cx="%s" cy="%s" r="11" fill="%s"/>' % (X2 + 24, BY + 26, C["scale"]))
text(X2 + 24, BY + 30.5, "3", 12, "#fff", True, anchor="middle")
text(X2 + 43, BY + 30.5, "RUN IT AT SCALE", 12, C["scale"], True, spacing=1.1)
text(X2 + 20, BY + 56, "drain-refined", 14, INK, True, True, maxw=W2 - 40)
text(X2 + 20, BY + 74, "Unattended: each group runs box 2, then land-ticket.", 12, MUTED, maxw=W2 - 40)
arrow("M%s %s V%s" % (X2 + W2 / 2, BY - 2, PY + PH + 3), "scale", dash=True)

# ---------- 5 data ----------
DY, DH = BY + BH + 22, 78
a('<rect x="%s" y="%s" width="%s" height="%s" rx="14" fill="%s" stroke="%s" stroke-opacity="0.35"/>' % (32, DY, W - 64, DH, TINT["data"], C["data"]))
a('<circle cx="56" cy="%s" r="11" fill="%s"/>' % (DY + 26, C["data"]))
text(56, DY + 30.5, "5", 12, "#fff", True, anchor="middle")
text(75, DY + 30.5, "INVESTIGATE WITH DATA", 12, C["data"], True, spacing=1.1)
card(52, DY + 40, 150, 30, "log-analysis", None, "data")
text(222, DY + 60, "debug  ·  size a change  ·  check an assumption  ·  evidence for specs  ·  baseline  ·  release watch  ·  A/B tests",
     12.5, MUTED, maxw=W - 64 - 200)
ax = X1 + W1 / 2
arrow("M%s %s V%s" % (ax, DY - 2, PY + PH + 3), "data", dash=True)
text(ax + 8, PY + PH + 50, "evidence for", 11, C["data"], True, maxw=X2 - ax - 16)
text(ax + 8, PY + PH + 64, "specs and design", 11, C["data"], True, maxw=X2 - ax - 16)
up_x, down_x = X3 + 120, X3 + 300
arrow("M%s %s V%s" % (up_x, DY - 2, PY + PH + 3), "data", dash=True)
text(up_x + 8, PY + PH + 50, "canary checks", 11, C["data"], True, maxw=down_x - up_x - 20)
text(up_x + 8, PY + PH + 64, "and debugging", 11, C["data"], True, maxw=down_x - up_x - 20)
arrow("M%s %s V%s" % (down_x, PY + PH + 3, DY - 2), "data", dash=True)
text(down_x + 8, PY + PH + 50, "release watch", 11, C["data"], True, maxw=W - 32 - down_x - 16)
text(down_x + 8, PY + PH + 64, "and A/B results", 11, C["data"], True, maxw=W - 32 - down_x - 16)

# ---------- 6 foundations ----------
FY, FH = DY + DH + 22, 78
a('<rect x="%s" y="%s" width="%s" height="%s" rx="14" fill="%s" stroke="%s" stroke-opacity="0.35"/>' % (32, FY, W - 64, FH, TINT["base"], C["base"]))
a('<circle cx="56" cy="%s" r="11" fill="%s"/>' % (FY + 26, C["base"]))
text(56, FY + 30.5, "6", 12, "#fff", True, anchor="middle")
text(75, FY + 30.5, "FOUNDATIONS", 12, C["base"], True, spacing=1.1)
card(52, FY + 40, 120, 30, "wrap-up", None, "base")
card(186, FY + 40, 250, 30, "agent-context-template", None, "base")
text(456, FY + 60, "Every session ends by saving what worked as memory; every repo starts with the right rules.",
     12.5, MUTED, maxw=W - 64 - 440)

a("</svg>")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cycle.svg")
open(out, "w", encoding="utf-8").write("\n".join(o))
if problems:
    print("TEXT OVERFLOW:\n  " + "\n  ".join(problems))
else:
    print("all text fits")
