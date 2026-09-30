"""Génère un PPTX éditable à partir du contenu du pitch INDIE.CO."""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pathlib import Path

ROOT = Path(__file__).parent
ASSETS = ROOT / "assets"
OUT = ROOT / "INDIE-CO_pitch.pptx"

# Palette (proche du site)
KLEIN_BLUE = RGBColor(0x00, 0x2F, 0xA7)
KLEIN_DEEP = RGBColor(0x00, 0x1F, 0x6E)
IVORY = RGBColor(0xF5, 0xED, 0xD8)
IVORY_DARK = RGBColor(0xEA, 0xE0, 0xC5)
INK = RGBColor(0x0A, 0x08, 0x10)
INK_SOFT = RGBColor(0x33, 0x30, 0x40)
ROTHKO_ORANGE = RGBColor(0xE8, 0x5D, 0x2F)
ROTHKO_CRIMSON = RGBColor(0xB5, 0x2A, 0x1F)
GOLD = RGBColor(0xF5, 0xA6, 0x23)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LINE = RGBColor(0xD8, 0xCE, 0xB4)

# Fonts (utilise les fallback système)
F_DISPLAY = "Georgia"        # proxy pour Fraunces
F_BODY = "Calibri"           # proxy pour Inter
F_MONO = "Consolas"          # proxy pour JetBrains Mono

# Slide size 16:9 large (13.333 x 7.5 inches)
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
SW = prs.slide_width
SH = prs.slide_height

BLANK = prs.slide_layouts[6]  # layout vide


def add_slide(bg=IVORY):
    slide = prs.slides.add_slide(BLANK)
    bg_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SW, SH)
    bg_shape.line.fill.background()
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = bg
    return slide


def add_text(slide, x, y, w, h, text, *, font=F_BODY, size=14,
             color=INK, bold=False, italic=False, align=PP_ALIGN.LEFT,
             anchor=MSO_ANCHOR.TOP, line_spacing=1.15):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.margin_left = tf.margin_right = 0
    tf.margin_top = tf.margin_bottom = 0
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    lines = text.split("\n") if isinstance(text, str) else text
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = line_spacing
        r = p.add_run()
        r.text = line
        r.font.name = font
        r.font.size = Pt(size)
        r.font.color.rgb = color
        r.font.bold = bold
        r.font.italic = italic
    return tb


def add_bullets(slide, x, y, w, h, items, *, font=F_DISPLAY, size=14,
                color=INK, bullet_color=ROTHKO_ORANGE, gap=0.5):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.margin_left = tf.margin_right = 0
    tf.margin_top = tf.margin_bottom = 0
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.line_spacing = 1.35
        p.space_after = Pt(gap * 8)
        r1 = p.add_run()
        r1.text = "•  "
        r1.font.name = font
        r1.font.size = Pt(size)
        r1.font.color.rgb = bullet_color
        r1.font.bold = True
        r2 = p.add_run()
        r2.text = item
        r2.font.name = font
        r2.font.size = Pt(size)
        r2.font.color.rgb = color
    return tb


def add_rect(slide, x, y, w, h, fill, line_color=None, line_w=0):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    s.fill.solid()
    s.fill.fore_color.rgb = fill
    if line_color is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line_color
        s.line.width = Pt(line_w)
    s.shadow.inherit = False
    return s


def add_round(slide, x, y, w, h, fill, line_color=None):
    s = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    s.adjustments[0] = 0.08
    s.fill.solid()
    s.fill.fore_color.rgb = fill
    if line_color is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line_color
        s.line.width = Pt(0.75)
    s.shadow.inherit = False
    return s


def add_line(slide, x1, y1, x2, y2, color=KLEIN_BLUE, w=1.5):
    ln = slide.shapes.add_connector(1, x1, y1, x2, y2)
    ln.line.color.rgb = color
    ln.line.width = Pt(w)
    return ln


def chapter_label(slide, x, y, text, color=KLEIN_BLUE):
    add_text(slide, x, y, Inches(6), Inches(0.3), text,
             font=F_MONO, size=10, color=color, bold=True)


def title_block(slide, x, y, w, title_main, title_em, *, size=42):
    tb = slide.shapes.add_textbox(x, y, w, Inches(2.2))
    tf = tb.text_frame
    tf.margin_left = tf.margin_right = 0
    tf.margin_top = tf.margin_bottom = 0
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.line_spacing = 1.05
    r = p1.add_run()
    r.text = title_main
    r.font.name = F_DISPLAY
    r.font.size = Pt(size)
    r.font.color.rgb = INK
    r.font.bold = False
    p2 = tf.add_paragraph()
    p2.line_spacing = 1.05
    r2 = p2.add_run()
    r2.text = title_em
    r2.font.name = F_DISPLAY
    r2.font.size = Pt(size)
    r2.font.color.rgb = INK
    r2.font.italic = True
    return tb


# =============================================================
# SLIDE 1 — Couverture
# =============================================================
s = add_slide(bg=IVORY)
# Bande Klein Blue à gauche
add_rect(s, 0, 0, Inches(4.2), SH, KLEIN_BLUE)
add_rect(s, Inches(4.2), 0, Inches(0.05), SH, GOLD)

# Logo centré (si présent)
logo = ASSETS / "logo.png"
if logo.exists():
    s.shapes.add_picture(str(logo), Inches(6.5), Inches(1.7), height=Inches(1.6))

# Marque
add_text(s, Inches(5.5), Inches(3.6), Inches(7), Inches(1.2),
         "INDIE.CO", font=F_DISPLAY, size=64, color=INK, align=PP_ALIGN.CENTER)
add_text(s, Inches(5.5), Inches(4.7), Inches(7), Inches(0.5),
         "IP TV", font=F_MONO, size=14, color=KLEIN_BLUE, align=PP_ALIGN.CENTER, bold=True)
add_text(s, Inches(5.5), Inches(5.6), Inches(7), Inches(0.6),
         "La télévision culturelle mondiale.",
         font=F_DISPLAY, size=22, color=INK_SOFT, italic=True, align=PP_ALIGN.CENTER)

# Texte vertical bande gauche
add_text(s, Inches(0.6), Inches(0.6), Inches(3.2), Inches(0.4),
         "01 — COUVERTURE", font=F_MONO, size=10, color=GOLD, bold=True)
add_text(s, Inches(0.6), Inches(6.7), Inches(3.2), Inches(0.4),
         "Pitch deck · 2026", font=F_MONO, size=10, color=IVORY, bold=True)

# =============================================================
# SLIDE 2 — Présentation / Problématique
# =============================================================
s = add_slide()
chapter_label(s, Inches(0.6), Inches(0.55), "01 — PRÉSENTATION")
title_block(s, Inches(0.6), Inches(0.95), Inches(12),
            "INDIE.CO — IP TV", "La télévision culturelle mondiale.")

# Ligne décorative
add_line(s, Inches(0.6), Inches(3.15), Inches(12.7), Inches(3.15), color=LINE, w=0.75)

# Citation Malraux (gauche)
add_text(s, Inches(0.6), Inches(3.5), Inches(6), Inches(0.4),
         "LA CITATION", font=F_MONO, size=9, color=KLEIN_BLUE, bold=True)
add_text(s, Inches(0.6), Inches(3.9), Inches(6), Inches(2.5),
         "« Il existe une télévision pour passer le temps,\net une autre pour comprendre le temps. »",
         font=F_DISPLAY, size=20, color=INK, italic=True, line_spacing=1.3)
add_text(s, Inches(0.6), Inches(5.8), Inches(6), Inches(0.4),
         "— André Malraux", font=F_MONO, size=10, color=INK_SOFT)

# La problématique (droite)
add_text(s, Inches(7.2), Inches(3.5), Inches(5.6), Inches(0.4),
         "LA PROBLÉMATIQUE", font=F_MONO, size=9, color=ROTHKO_ORANGE, bold=True)
add_text(s, Inches(7.2), Inches(3.9), Inches(5.6), Inches(2.5),
         "Le contenu étant aussi important que le flux, le zapping a remplacé le regard.\n\n"
         "Face à la saturation des plateformes généralistes, il n'existe aucune télévision "
         "mondiale dédiée à la culture, l'art et le soft power, pensée pour l'ère d'Internet.",
         font=F_BODY, size=13, color=INK_SOFT, line_spacing=1.4)
add_text(s, Inches(7.2), Inches(6.4), Inches(5.6), Inches(0.5),
         "INDIE.CO comble ce vide.",
         font=F_DISPLAY, size=18, color=KLEIN_BLUE, bold=True, italic=True)

# =============================================================
# SLIDE 3 — Pourquoi / Vision
# =============================================================
s = add_slide()
chapter_label(s, Inches(0.6), Inches(0.55), "02 — POURQUOI")
title_block(s, Inches(0.6), Inches(0.95), Inches(12),
            "Revenir aux", "réels contenus.")

add_text(s, Inches(0.6), Inches(3.1), Inches(12), Inches(1.1),
         "Le numérique appliqué à l'image provoque un basculement de civilisation aussi "
         "important que celui de la galaxie Gutenberg. Ce basculement ne vaut qu'à une condition "
         "expresse : revenir aux réels contenus. C'est là que se situe toute l'ambition d'INDIE.CO — l'idée visionnaire.",
         font=F_BODY, size=12, color=INK_SOFT, line_spacing=1.5)

add_text(s, Inches(0.6), Inches(4.5), Inches(12), Inches(0.3),
         "TROIS CONVICTIONS FONDENT LE PROJET",
         font=F_MONO, size=10, color=KLEIN_BLUE, bold=True)

convictions = [
    ("01", "Comprendre.",
     "Aller plus loin que le précepte de Malraux : créer une télévision qui ne se contente pas "
     "de comprendre le temps, mais le révolutionne et le dépasse."),
    ("02", "Rayonner.",
     "Faire de la culture un instrument de soft power : la France et l'Europe comme point de "
     "départ, le monde comme extension naturelle."),
    ("03", "Élever.",
     "« La télévision de demain est un art et une industrie. » Le média lui-même, par sa "
     "conception et son habillage inspiré de Mark Rothko, est une forme conceptuelle d'art."),
]
card_w = Inches(4.0)
gap = Inches(0.2)
start_x = Inches(0.6)
for i, (num, ttl, txt) in enumerate(convictions):
    x = start_x + i * (card_w + gap)
    add_round(s, x, Inches(4.95), card_w, Inches(2.15), WHITE, line_color=LINE)
    add_text(s, x + Inches(0.3), Inches(5.1), Inches(1), Inches(0.35), num,
             font=F_MONO, size=11, color=KLEIN_BLUE, bold=True)
    add_text(s, x + Inches(0.3), Inches(5.4), card_w - Inches(0.6), Inches(0.5), ttl,
             font=F_DISPLAY, size=18, color=INK, italic=True)
    add_text(s, x + Inches(0.3), Inches(5.95), card_w - Inches(0.6), Inches(1.2), txt,
             font=F_BODY, size=10, color=INK_SOFT, line_spacing=1.35)

# =============================================================
# SLIDE 4 — La solution (dark)
# =============================================================
s = add_slide(bg=INK)
add_text(s, Inches(0.6), Inches(0.55), Inches(6), Inches(0.3),
         "03 — LA SOLUTION", font=F_MONO, size=10, color=GOLD, bold=True)
tb = s.shapes.add_textbox(Inches(0.6), Inches(0.95), Inches(12), Inches(2))
tf = tb.text_frame; tf.word_wrap = True
p1 = tf.paragraphs[0]; p1.line_spacing = 1.05
r = p1.add_run(); r.text = "Une télévision culturelle mondiale."
r.font.name = F_DISPLAY; r.font.size = Pt(38); r.font.color.rgb = WHITE
p2 = tf.add_paragraph(); p2.line_spacing = 1.05
r2 = p2.add_run(); r2.text = "Deux façons de la vivre."
r2.font.name = F_DISPLAY; r2.font.size = Pt(38); r2.font.color.rgb = WHITE; r2.font.italic = True

add_text(s, Inches(0.6), Inches(3.0), Inches(12), Inches(0.4),
         "Un même catalogue, deux expériences complémentaires.",
         font=F_BODY, size=13, color=RGBColor(0xC5, 0xC0, 0xB8), italic=True)

# Deux cartes
cards = [
    ("01", "INDIE.CO", "La chaîne",
     "Une véritable chaîne de télévision fondée sur la VOD relinéarisée : un catalogue culturel "
     "éditorialisé, une grille pensée par une rédaction et un rendez-vous quotidien.",
     ["Débats, rencontres, portraits",
      "Documentaires et captations de spectacle vivant",
      "Cinéma d'auteur et coproductions internationales",
      "Replay et catch-up intégrés"], KLEIN_BLUE),
    ("02", "TV4U", "Votre télévision",
     "Une expérience personnalisée sans direction des programmes : chaque utilisateur construit "
     "sa propre télévision à partir du catalogue.",
     ["Playlists sur mesure (interfaces neuronales à terme)",
      "Programmes adaptés aux goûts et horaires",
      "Recommandations intelligentes",
      "Fonctions sociales pour partager et échanger"], ROTHKO_ORANGE),
]

for i, (num, brand, tag, desc, items, accent) in enumerate(cards):
    x = Inches(0.6) + i * Inches(6.4)
    w = Inches(6.0)
    add_round(s, x, Inches(3.7), w, Inches(3.6), RGBColor(0x1A, 0x18, 0x24))
    add_rect(s, x, Inches(3.7), Inches(0.08), Inches(3.6), accent)
    add_text(s, x + Inches(0.4), Inches(3.85), Inches(1), Inches(0.3), num,
             font=F_MONO, size=11, color=accent, bold=True)
    add_text(s, x + Inches(0.4), Inches(4.15), w - Inches(0.8), Inches(0.5), brand,
             font=F_DISPLAY, size=22, color=WHITE, bold=True)
    add_text(s, x + Inches(0.4), Inches(4.65), w - Inches(0.8), Inches(0.35), tag,
             font=F_MONO, size=10, color=accent, bold=True)
    add_text(s, x + Inches(0.4), Inches(5.0), w - Inches(0.8), Inches(0.9), desc,
             font=F_BODY, size=10, color=RGBColor(0xD5, 0xD0, 0xC8), line_spacing=1.35)
    add_bullets(s, x + Inches(0.4), Inches(6.05), w - Inches(0.8), Inches(1.2),
                items, font=F_BODY, size=9,
                color=RGBColor(0xC0, 0xBB, 0xB0), bullet_color=accent, gap=0.15)

# =============================================================
# SLIDE 5 — La technologie
# =============================================================
s = add_slide()
chapter_label(s, Inches(0.6), Inches(0.55), "04 — LA TECHNOLOGIE")
title_block(s, Inches(0.6), Inches(0.95), Inches(12),
            "IPTV + OTT", "+ Intelligence artificielle.", size=38)
add_text(s, Inches(0.6), Inches(3.05), Inches(12), Inches(0.9),
         "Une diffusion accessible sur tous les écrans, un boîtier IP breveté relié à la box du "
         "fournisseur d'accès à Internet, et une IA au cœur de l'expérience.",
         font=F_BODY, size=12, color=INK_SOFT, line_spacing=1.45)

# Pipeline
steps = ["Catalogue\nFilms · docs · captations",
         "Cloud INDIE.CO\nServeurs mondiaux",
         "IA & Données\nProfilage · Recommandation",
         "Distribution\nIPTV · OTT",
         "Tous les écrans\nTV · PC · Mobile · Tablette"]
step_w = Inches(2.3)
step_h = Inches(1.1)
step_y = Inches(4.15)
total_w = 5 * step_w.emu + 4 * Inches(0.15).emu
start_x = int((SW.emu - total_w) / 2)
for i, txt in enumerate(steps):
    x = Emu(start_x + i * (step_w.emu + Inches(0.15).emu))
    fill = KLEIN_BLUE if i == 2 else IVORY_DARK
    color = WHITE if i == 2 else INK
    add_round(s, x, step_y, step_w, step_h, fill)
    lines = txt.split("\n")
    add_text(s, x + Inches(0.15), step_y + Inches(0.2), step_w - Inches(0.3), Inches(0.4),
             lines[0], font=F_DISPLAY, size=13, color=color, bold=True, align=PP_ALIGN.CENTER)
    add_text(s, x + Inches(0.15), step_y + Inches(0.65), step_w - Inches(0.3), Inches(0.4),
             lines[1], font=F_BODY, size=9, color=color, align=PP_ALIGN.CENTER)

# Sections IA + parcours OTT
add_text(s, Inches(0.6), Inches(5.55), Inches(6), Inches(0.3),
         "L'IA AU CŒUR DE LA PERSONNALISATION",
         font=F_MONO, size=9, color=KLEIN_BLUE, bold=True)
ai = ["Recommandations — moteur nourri par les préférences déclarées",
      "Sous-titrage multilingue — adaptation aux marchés asiatiques",
      "Accessibilité renforcée — système dédié aux malentendants",
      "Profilage éthique — profils programmes et publicitaire distincts"]
add_bullets(s, Inches(0.6), Inches(5.9), Inches(6), Inches(1.3), ai,
            font=F_BODY, size=10, color=INK_SOFT, bullet_color=KLEIN_BLUE, gap=0.15)

add_text(s, Inches(7.2), Inches(5.55), Inches(5.6), Inches(0.3),
         "LE PARCOURS OTT",
         font=F_MONO, size=9, color=ROTHKO_ORANGE, bold=True)
ott = ["01  Créer son profil",
       "02  Renseigner ses goûts",
       "03  Accéder au catalogue",
       "04  Composer sa grille"]
add_bullets(s, Inches(7.2), Inches(5.9), Inches(5.6), Inches(1.3), ott,
            font=F_BODY, size=10, color=INK_SOFT, bullet_color=ROTHKO_ORANGE, gap=0.15)

# =============================================================
# SLIDE 6 — Catalogue
# =============================================================
s = add_slide(bg=IVORY_DARK)
add_text(s, Inches(0.6), Inches(0.55), Inches(6), Inches(0.3),
         "05 — LE CATALOGUE", font=F_MONO, size=10, color=GOLD, bold=True)
title_block(s, Inches(0.6), Inches(0.95), Inches(12),
            "Une télévision culturelle.", "Un softpower assumé.", size=36)

add_text(s, Inches(0.6), Inches(3.0), Inches(12), Inches(1.0),
         "Coproductions internationales, productions propres (captations musicales, théâtrales, "
         "chorégraphiques), catalogue de films acquis ou du domaine public, contributions "
         "d'internautes créatifs révélées par des concours.",
         font=F_BODY, size=11, color=INK_SOFT, line_spacing=1.4)

# Parcours en 5 étapes
add_text(s, Inches(0.6), Inches(4.15), Inches(12), Inches(0.3),
         "LE PARCOURS UTILISATEUR, EN CINQ ÉTAPES",
         font=F_MONO, size=9, color=KLEIN_BLUE, bold=True)
journey = [
    ("01", "Plateforme mondiale INDIE.CO"),
    ("02", "Profil et préférences"),
    ("03", "Personnalisation IA"),
    ("04", "Chaîne ou sélection"),
    ("05", "TV · Mobile · Web"),
]
jw = Inches(2.4)
for i, (n, t) in enumerate(journey):
    x = Inches(0.6) + i * Inches(2.5)
    add_round(s, x, Inches(4.55), jw, Inches(0.85), WHITE, line_color=LINE)
    add_text(s, x + Inches(0.2), Inches(4.62), jw - Inches(0.4), Inches(0.25), n,
             font=F_MONO, size=9, color=KLEIN_BLUE, bold=True)
    add_text(s, x + Inches(0.2), Inches(4.9), jw - Inches(0.4), Inches(0.5), t,
             font=F_DISPLAY, size=11, color=INK, bold=True)

# Thèmes en pastilles
themes = ["Littérature", "Art", "Cinéma", "Musique", "Bande dessinée", "Histoire",
          "Géographie", "Économie", "Société", "Psychanalyse", "Linguistique",
          "Ethnologie", "Éthologie", "Spiritualités", "Médecine", "Agriculture & vin", "Sport"]
tx = Inches(0.6); ty = Inches(5.7)
for t in themes:
    w = Inches(0.15 + len(t) * 0.09)
    add_round(s, tx, ty, w, Inches(0.35), WHITE, line_color=KLEIN_BLUE)
    add_text(s, tx, ty + Inches(0.03), w, Inches(0.3), t,
             font=F_MONO, size=8, color=KLEIN_BLUE, align=PP_ALIGN.CENTER, bold=True)
    tx = Emu(tx + w + Inches(0.1))
    if tx > Inches(12):
        tx = Inches(0.6); ty = Emu(ty + Inches(0.45))

# Softpower
add_text(s, Inches(0.6), Inches(6.9), Inches(3), Inches(0.3),
         "SOFTPOWER", font=F_MONO, size=9, color=ROTHKO_ORANGE, bold=True)
add_text(s, Inches(3), Inches(6.9), Inches(10), Inches(0.3),
         "France  →  Europe  →  Amériques  →  Asie  →  Monde",
         font=F_MONO, size=11, color=INK, bold=True)

# =============================================================
# SLIDE 7 — Modèle économique
# =============================================================
s = add_slide()
chapter_label(s, Inches(0.6), Inches(0.55), "06 — LE MODÈLE ÉCONOMIQUE")
tb = s.shapes.add_textbox(Inches(0.6), Inches(0.95), Inches(12), Inches(2.2))
tf = tb.text_frame; tf.word_wrap = True
for i, line in enumerate(["Un modèle hybride.",
                          "La publicité finance la gratuité,",
                          "l'abonnement achète la liberté."]):
    p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
    p.line_spacing = 1.05
    r = p.add_run(); r.text = line
    r.font.name = F_DISPLAY; r.font.size = Pt(30); r.font.color.rgb = INK
    if i > 0: r.font.italic = True

add_text(s, Inches(0.6), Inches(3.1), Inches(12), Inches(0.8),
         "Principe fondateur : publicité complète = gratuité ; sans publicité = abonnement. "
         "Avec tous les mix intermédiaires possibles.",
         font=F_BODY, size=12, color=INK_SOFT, line_spacing=1.4)

# Deux cartes tarif
card_w = Inches(5.5)
add_round(s, Inches(0.6), Inches(4.15), card_w, Inches(2.5), WHITE, line_color=LINE)
add_text(s, Inches(0.8), Inches(4.3), card_w, Inches(0.3), "GRATUIT",
         font=F_MONO, size=9, color=ROTHKO_ORANGE, bold=True)
add_text(s, Inches(0.8), Inches(4.6), card_w, Inches(0.5), "Avec publicité",
         font=F_DISPLAY, size=18, color=INK)
add_text(s, Inches(0.8), Inches(5.05), card_w, Inches(0.7), "0 €",
         font=F_DISPLAY, size=36, color=KLEIN_BLUE, bold=True)
add_bullets(s, Inches(0.8), Inches(5.85), card_w - Inches(0.4), Inches(0.9),
            ["Accès au catalogue",
             "Publicité ciblée et éthique",
             "Recommandations personnalisées"],
            font=F_BODY, size=10, color=INK_SOFT, bullet_color=ROTHKO_ORANGE, gap=0.1)

# + centré
add_text(s, Inches(6.2), Inches(5.0), Inches(1), Inches(1), "+",
         font=F_DISPLAY, size=48, color=LINE, align=PP_ALIGN.CENTER)

add_round(s, Inches(7.25), Inches(4.15), card_w, Inches(2.5), KLEIN_BLUE)
add_text(s, Inches(7.45), Inches(4.3), card_w, Inches(0.3), "PREMIUM",
         font=F_MONO, size=9, color=GOLD, bold=True)
add_text(s, Inches(7.45), Inches(4.6), card_w, Inches(0.5), "Sans publicité",
         font=F_DISPLAY, size=18, color=WHITE)
add_text(s, Inches(7.45), Inches(5.05), card_w, Inches(0.7), "15 €/mois",
         font=F_DISPLAY, size=32, color=WHITE, bold=True)
add_bullets(s, Inches(7.45), Inches(5.85), card_w - Inches(0.4), Inches(0.9),
            ["Aucune publicité",
             "Accès intégral au catalogue",
             "Fonctions sociales avancées"],
            font=F_BODY, size=10, color=WHITE, bullet_color=GOLD, gap=0.1)

# Note
add_text(s, Inches(0.6), Inches(6.9), Inches(12), Inches(0.4),
         "Grâce au boîtier IP, chaque point d'audience génère un retour économique mesurable, comme en TV classique.",
         font=F_BODY, size=10, color=INK_SOFT, italic=True, align=PP_ALIGN.CENTER)

# =============================================================
# SLIDE 8 — Structure
# =============================================================
s = add_slide()
chapter_label(s, Inches(0.6), Inches(0.55), "07 — STRUCTURE")
title_block(s, Inches(0.6), Inches(0.95), Inches(12),
            "Une société pensée", "pour fédérer les partenaires.", size=32)

blocks = [
    ("Juridique et capital", "SAS « INDIE.CO »",
     "La SASU existante est prête à être transformée en SAS « INDIE.CO ». Capital variable, "
     "objectif 500 000 € rapidement. Actionnariat social, nominal 1 €.",
     "Europe · Amériques · Asie", KLEIN_BLUE),
    ("Modèle de droits", "Droits d'auteur en actions",
     "Scénaristes, réalisateurs et ayants droit deviennent partenaires. Cette clause permet de "
     "constituer rapidement un catalogue tout en alignant les intérêts.",
     "« Emmagasiner du marbre »", ROTHKO_ORANGE),
    ("Implantation", "Paris & États-Unis",
     "Paris comme centre initial, pôle technique aux États-Unis (NY ou LA), société de "
     "production de longs métrages adossée à la chaîne.",
     "Paris · New York · Los Angeles", KLEIN_BLUE),
]
cw = Inches(4.0); cx = Inches(0.6); cy = Inches(3.55)
for i, (lbl, ttl, txt, foot, accent) in enumerate(blocks):
    x = cx + i * (cw + Inches(0.2))
    add_round(s, x, cy, cw, Inches(3.6), WHITE, line_color=LINE)
    add_rect(s, x, cy, cw, Inches(0.08), accent)
    add_text(s, x + Inches(0.3), cy + Inches(0.25), cw - Inches(0.6), Inches(0.3), lbl.upper(),
             font=F_MONO, size=9, color=accent, bold=True)
    add_text(s, x + Inches(0.3), cy + Inches(0.6), cw - Inches(0.6), Inches(0.6), ttl,
             font=F_DISPLAY, size=17, color=INK, bold=True)
    add_text(s, x + Inches(0.3), cy + Inches(1.5), cw - Inches(0.6), Inches(1.6), txt,
             font=F_BODY, size=10, color=INK_SOFT, line_spacing=1.4)
    add_text(s, x + Inches(0.3), cy + Inches(3.1), cw - Inches(0.6), Inches(0.4), foot,
             font=F_MONO, size=9, color=accent, bold=True)

# =============================================================
# SLIDE 9 — Femmes et hommes (dark)
# =============================================================
s = add_slide(bg=INK)
add_text(s, Inches(0.6), Inches(0.55), Inches(8), Inches(0.3),
         "08 — LES FEMMES ET LES HOMMES", font=F_MONO, size=10, color=GOLD, bold=True)
tb = s.shapes.add_textbox(Inches(0.6), Inches(0.95), Inches(12), Inches(2))
tf = tb.text_frame; tf.word_wrap = True
for i, line in enumerate(["Un média porté", "par des regards."]):
    p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
    p.line_spacing = 1.05
    r = p.add_run(); r.text = line
    r.font.name = F_DISPLAY; r.font.size = Pt(36); r.font.color.rgb = WHITE
    if i > 0: r.font.italic = True
add_text(s, Inches(0.6), Inches(2.85), Inches(12), Inches(0.6),
         "INDIE.CO est d'abord une aventure humaine : des auteurs, des artistes, des "
         "scientifiques, des techniciens — et une éthique éditoriale incarnée.",
         font=F_BODY, size=12, color=RGBColor(0xC5, 0xC0, 0xB8), italic=True, line_spacing=1.4)

# 2 blocs
add_round(s, Inches(0.6), Inches(3.75), Inches(6), Inches(1.9), RGBColor(0x1A, 0x18, 0x24))
add_rect(s, Inches(0.6), Inches(3.75), Inches(0.08), Inches(1.9), KLEIN_BLUE)
add_text(s, Inches(0.85), Inches(3.9), Inches(5), Inches(0.3), "CRÉER",
         font=F_MONO, size=10, color=KLEIN_BLUE, bold=True)
add_bullets(s, Inches(0.85), Inches(4.25), Inches(5.5), Inches(1.4), [
    "Direction éditoriale et artistique garante de la ligne",
    "Réseau international de coproducteurs",
    "Jeunes créateurs révélés par des concours"
], font=F_BODY, size=10, color=RGBColor(0xD5, 0xD0, 0xC8), bullet_color=KLEIN_BLUE, gap=0.15)

add_round(s, Inches(6.85), Inches(3.75), Inches(6), Inches(1.9), RGBColor(0x1A, 0x18, 0x24))
add_rect(s, Inches(6.85), Inches(3.75), Inches(0.08), Inches(1.9), ROTHKO_ORANGE)
add_text(s, Inches(7.1), Inches(3.9), Inches(5), Inches(0.3), "FAIRE VIVRE",
         font=F_MONO, size=10, color=ROTHKO_ORANGE, bold=True)
add_bullets(s, Inches(7.1), Inches(4.25), Inches(5.5), Inches(1.4), [
    "Pôle technique et plateforme (diffusion, middleware, IA)",
    "Régie publicitaire et partenariats",
    "Modérateurs éthiques omniprésents"
], font=F_BODY, size=10, color=RGBColor(0xD5, 0xD0, 0xC8), bullet_color=ROTHKO_ORANGE, gap=0.15)

# Écosystème 5 cartes
eco = [
    ("Créateurs", ["Réalisateurs", "Producteurs", "Artistes", "Auteurs"]),
    ("Experts", ["Chercheurs", "Scientifiques", "Intellectuels", "Journalistes"]),
    ("Technologie", ["Ingénieurs", "Développeurs", "IA & données"]),
    ("Média", ["Programmation", "Production", "Distribution"]),
    ("Partenaires", ["Institutions", "Fondations", "Marques", "Universités"]),
]
ew = Inches(2.4); ex = Inches(0.6); ey = Inches(5.85)
for name, items in eco:
    add_round(s, ex, ey, ew, Inches(1.45), RGBColor(0x1F, 0x1D, 0x2A))
    add_text(s, ex + Inches(0.2), ey + Inches(0.15), ew - Inches(0.4), Inches(0.3), name,
             font=F_DISPLAY, size=12, color=GOLD, bold=True)
    tb = s.shapes.add_textbox(ex + Inches(0.2), ey + Inches(0.5), ew - Inches(0.4), Inches(0.9))
    tf = tb.text_frame; tf.word_wrap = True
    for i, it in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.line_spacing = 1.15
        r = p.add_run(); r.text = it
        r.font.name = F_BODY; r.font.size = Pt(9); r.font.color.rgb = RGBColor(0xC5, 0xC0, 0xB8)
    ex = ex + ew + Inches(0.1)

# =============================================================
# SLIDE 10 — Budget initial
# =============================================================
s = add_slide(bg=IVORY_DARK)
chapter_label(s, Inches(0.6), Inches(0.55), "09 — BUDGET INITIAL")
tb = s.shapes.add_textbox(Inches(0.6), Inches(0.95), Inches(12), Inches(1.5))
tf = tb.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]; p.line_spacing = 1.05
r = p.add_run(); r.text = "Année 1 : "
r.font.name = F_DISPLAY; r.font.size = Pt(36); r.font.color.rgb = INK
r2 = p.add_run(); r2.text = "51,5 M€ HT."
r2.font.name = F_DISPLAY; r2.font.size = Pt(36); r2.font.color.rgb = KLEIN_BLUE
r2.font.italic = True; r2.font.bold = True

add_text(s, Inches(0.6), Inches(2.5), Inches(12), Inches(0.9),
         "Un investissement de lancement couvert par une augmentation de capital de 51 M€ : "
         "18,9 M€ d'investissements (CAPEX) et 32,6 M€ de charges d'exploitation.",
         font=F_BODY, size=12, color=INK_SOFT, line_spacing=1.4)

# Grand chiffre
add_round(s, Inches(0.6), Inches(3.7), Inches(5.5), Inches(2.0), KLEIN_BLUE)
add_text(s, Inches(0.85), Inches(3.85), Inches(5), Inches(0.4),
         "BESOIN DE FINANCEMENT · ANNÉE 1",
         font=F_MONO, size=9, color=GOLD, bold=True)
add_text(s, Inches(0.85), Inches(4.25), Inches(5), Inches(1.1),
         "51,5 M€ HT", font=F_DISPLAY, size=44, color=WHITE, bold=True)
add_text(s, Inches(0.85), Inches(5.3), Inches(5), Inches(0.4),
         "CAPEX + charges d'exploitation",
         font=F_BODY, size=10, color=RGBColor(0xE0, 0xDB, 0xC5), italic=True)

# Tableau budget (barres)
rows = [
    ("Charges semi-variables (acquisitions audio & commercial)", 16.9, 1.00),
    ("Charges fixes d'exploitation", 13.3, 0.79),
    ("CAPEX matériel (tangible)", 10.6, 0.63),
    ("CAPEX incorporel (droits, logiciels)", 8.2, 0.49),
    ("Salaires & charges sociales", 2.4, 0.14),
    ("Charges variables (taxes CA)", 0.1, 0.01),
]
bx = Inches(6.4); by = Inches(3.7); bw = Inches(6.4); rh = Inches(0.35); gap = Inches(0.05)
for i, (lbl, val, pct) in enumerate(rows):
    ry = by + i * (rh + gap)
    add_text(s, bx, ry, Inches(4.0), rh, lbl,
             font=F_BODY, size=9, color=INK, anchor=MSO_ANCHOR.MIDDLE)
    bar_max = Inches(1.8)
    bar_x = bx + Inches(4.1)
    add_rect(s, bar_x, ry + Inches(0.1), bar_max, Inches(0.15), IVORY, line_color=None)
    bar_fill = Emu(int(bar_max.emu * pct))
    add_rect(s, bar_x, ry + Inches(0.1), bar_fill, Inches(0.15), KLEIN_BLUE)
    add_text(s, bx + Inches(6.0), ry, Inches(0.5), rh, f"{val} M€",
             font=F_MONO, size=9, color=KLEIN_BLUE, bold=True, align=PP_ALIGN.RIGHT,
             anchor=MSO_ANCHOR.MIDDLE)

# Free cash flow
add_round(s, Inches(0.6), Inches(6.0), Inches(12.2), Inches(1.2), WHITE, line_color=LINE)
add_text(s, Inches(0.85), Inches(6.15), Inches(4), Inches(0.3),
         "FREE CASH FLOW · ANNÉE 1", font=F_MONO, size=9, color=ROTHKO_ORANGE, bold=True)
add_text(s, Inches(0.85), Inches(6.5), Inches(4), Inches(0.6),
         "−31,8 M€", font=F_DISPLAY, size=24, color=ROTHKO_ORANGE, bold=True)
add_text(s, Inches(5.2), Inches(6.35), Inches(7.5), Inches(0.8),
         "EBITDA : −31,8 M€   ·   EBIT : −33,3 M€   ·   Trésorerie fin d'année : 0,4 M€",
         font=F_BODY, size=11, color=INK_SOFT, anchor=MSO_ANCHOR.MIDDLE)

# =============================================================
# SLIDE 11 — Prévisionnel 5 ans
# =============================================================
s = add_slide(bg=IVORY_DARK)
chapter_label(s, Inches(0.6), Inches(0.55), "10 — PRÉVISIONNEL FINANCIER")
title_block(s, Inches(0.6), Inches(0.95), Inches(12),
            "Une trajectoire", "exponentielle sur 5 ans.", size=32)

# Grand chiffre
add_round(s, Inches(0.6), Inches(3.1), Inches(5.8), Inches(3.4), KLEIN_BLUE)
add_text(s, Inches(0.85), Inches(3.3), Inches(5), Inches(0.4),
         "CHIFFRE D'AFFAIRES CUMULÉ",
         font=F_MONO, size=10, color=GOLD, bold=True)
add_text(s, Inches(0.85), Inches(3.75), Inches(5), Inches(1.4),
         "1,86 Md€", font=F_DISPLAY, size=52, color=WHITE, bold=True)
add_text(s, Inches(0.85), Inches(5.15), Inches(5), Inches(0.4),
         "Sur 5 années d'exploitation (2026 — 2030)",
         font=F_BODY, size=10, color=RGBColor(0xE0, 0xDB, 0xC5), italic=True)
metas = [
    ("Abonnés TV Année 5", "10 M"),
    ("Point d'équilibre", "Année 3 (+25,6 M€)"),
    ("EBIT Année 5", "1 068 M€"),
    ("Trésorerie Année 5", "1 242 M€"),
]
for i, (lbl, val) in enumerate(metas):
    y = Inches(5.7) + i * Inches(0.2)
    add_text(s, Inches(0.85), y, Inches(3.0), Inches(0.2), lbl,
             font=F_BODY, size=9, color=RGBColor(0xD5, 0xD0, 0xC5))
    add_text(s, Inches(3.85), y, Inches(2.0), Inches(0.2), val,
             font=F_MONO, size=9, color=WHITE, bold=True)

# Timeline 5 années
years = [
    ("Année 1 · 2026", "10 000 abonnés", "834 k€"),
    ("Année 2 · 2027", "150 000 abonnés", "13,3 M€"),
    ("Année 3 · 2028", "1 M abonnés", "95,9 M€"),
    ("Année 4 · 2029", "5 M abonnés", "500,4 M€"),
    ("Année 5 · 2030", "10 M abonnés", "1 251 M€"),
]
yx = Inches(6.6); yy = Inches(3.1); yw = Inches(1.22); yh = Inches(1.4)
for i, (lbl, subs, ca) in enumerate(years):
    x = yx + i * (yw + Inches(0.05))
    fill = ROTHKO_ORANGE if i == 4 else WHITE
    txt_color = WHITE if i == 4 else INK
    accent = GOLD if i == 4 else KLEIN_BLUE
    add_round(s, x, yy, yw, yh, fill, line_color=LINE if i != 4 else None)
    add_text(s, x + Inches(0.1), yy + Inches(0.15), yw - Inches(0.2), Inches(0.3), lbl,
             font=F_MONO, size=7, color=accent, bold=True, align=PP_ALIGN.CENTER)
    add_text(s, x + Inches(0.1), yy + Inches(0.5), yw - Inches(0.2), Inches(0.35), subs,
             font=F_BODY, size=8, color=txt_color, align=PP_ALIGN.CENTER)
    add_text(s, x + Inches(0.1), yy + Inches(0.85), yw - Inches(0.2), Inches(0.5), ca,
             font=F_DISPLAY, size=13, color=txt_color, bold=True, align=PP_ALIGN.CENTER)

# Sources revenus
add_text(s, Inches(6.6), Inches(4.75), Inches(6.5), Inches(0.3),
         "CINQ SOURCES DE REVENUS · VENTILATION ANNÉE 5",
         font=F_MONO, size=9, color=KLEIN_BLUE, bold=True)
sources = [
    ("Abonnements TV", "1 125 M€"),
    ("Œuvres d'art", "90 M€"),
    ("Publicité audiovisuelle", "22,5 M€"),
    ("Publicité display", "7,5 M€"),
    ("VOD/SVOD", "6 M€"),
]
sy = Inches(5.15)
for lbl, val in sources:
    add_text(s, Inches(6.6), sy, Inches(4.5), Inches(0.25), lbl,
             font=F_BODY, size=10, color=INK)
    add_text(s, Inches(11.2), sy, Inches(1.8), Inches(0.25), val,
             font=F_MONO, size=10, color=KLEIN_BLUE, bold=True, align=PP_ALIGN.RIGHT)
    sy = sy + Inches(0.32)

# =============================================================
# SLIDE 12 — Équipe
# =============================================================
s = add_slide()
chapter_label(s, Inches(0.6), Inches(0.55), "11 — L'ÉQUIPE")
tb = s.shapes.add_textbox(Inches(0.6), Inches(0.95), Inches(12), Inches(1.7))
tf = tb.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER; p.line_spacing = 1.05
r = p.add_run(); r.text = "L'équipe"
r.font.name = F_DISPLAY; r.font.size = Pt(40); r.font.color.rgb = INK
p2 = tf.add_paragraph(); p2.alignment = PP_ALIGN.CENTER; p2.line_spacing = 1.05
r2 = p2.add_run(); r2.text = "fondatrice."
r2.font.name = F_DISPLAY; r2.font.size = Pt(40); r2.font.color.rgb = INK; r2.font.italic = True

# Deux portraits
def portrait(x, photo_name, name, role, items, accent):
    add_round(s, x, Inches(3.3), Inches(6.0), Inches(3.9), WHITE, line_color=LINE)
    photo = ASSETS / photo_name
    if photo.exists():
        s.shapes.add_picture(str(photo), x + Inches(0.4), Inches(3.6),
                             width=Inches(2.0), height=Inches(2.4))
    add_rect(s, x + Inches(0.35), Inches(3.55), Inches(2.1), Inches(0.06), accent)
    add_text(s, x + Inches(2.6), Inches(3.6), Inches(3.2), Inches(0.6), name,
             font=F_DISPLAY, size=20, color=INK, bold=True)
    add_text(s, x + Inches(2.6), Inches(4.15), Inches(3.2), Inches(0.6), role,
             font=F_MONO, size=8, color=accent, bold=True)
    add_bullets(s, x + Inches(2.6), Inches(4.85), Inches(3.2), Inches(2.2),
                items, font=F_BODY, size=9, color=INK_SOFT,
                bullet_color=accent, gap=0.1)

portrait(Inches(0.4), "xavier-lelong.jpg", "Xavier Lelong",
         "PRÉSIDENT-DIRECTEUR GÉNÉRAL · FONDATEUR",
         ["Beaux-Arts d'Orléans",
          "École de cinéma de Paris",
          "Producteur exécutif — cinéma, TV, pub",
          "Partenaire d'Images TV",
          "Réalisateur télévision"],
         KLEIN_BLUE)

portrait(Inches(6.9), "cofondatrice.jpg", "Lisa Silve",
         "CO-PRODUCTRICE EXÉCUTIVE · ASSISTANTE DE LA DG MARIA",
         ["Éco-systèmes",
          "Éco-féminisme",
          "Médecines alternatives",
          "Sétoise d'origine"],
         ROTHKO_ORANGE)

# =============================================================
# SLIDE 13 — Merci / Contact
# =============================================================
s = add_slide(bg=IVORY)
add_rect(s, 0, 0, Inches(4.2), SH, KLEIN_BLUE)
add_rect(s, Inches(4.2), 0, Inches(0.05), SH, GOLD)

if logo.exists():
    s.shapes.add_picture(str(logo), Inches(6.5), Inches(1.3), height=Inches(1.2))

add_text(s, Inches(5.5), Inches(2.7), Inches(7), Inches(0.4),
         "INDIE.CO · IP TV",
         font=F_MONO, size=12, color=KLEIN_BLUE, bold=True, align=PP_ALIGN.CENTER)
add_text(s, Inches(5.5), Inches(3.2), Inches(7), Inches(1.5),
         "Merci.", font=F_DISPLAY, size=72, color=INK, italic=True, align=PP_ALIGN.CENTER)

# Contact
cy = Inches(5.2)
contacts = [
    ("Xavier Lelong", "Président-directeur général · Fondateur"),
    ("Courriel", "indieco34@gmail.com"),
    ("Téléphone", "+33 6 28 13 72 87"),
]
for lbl, val in contacts:
    add_text(s, Inches(5.5), cy, Inches(2.5), Inches(0.3), lbl.upper(),
             font=F_MONO, size=9, color=KLEIN_BLUE, bold=True, align=PP_ALIGN.RIGHT)
    add_text(s, Inches(8.2), cy, Inches(4.5), Inches(0.3), val,
             font=F_DISPLAY, size=13, color=INK)
    cy = cy + Inches(0.45)

add_text(s, Inches(5.5), Inches(6.75), Inches(7), Inches(0.3),
         "La télévision culturelle mondiale.",
         font=F_DISPLAY, size=14, color=INK_SOFT, italic=True, align=PP_ALIGN.CENTER)

add_text(s, Inches(0.6), Inches(0.6), Inches(3.2), Inches(0.4),
         "12 — CONTACT", font=F_MONO, size=10, color=GOLD, bold=True)
add_text(s, Inches(0.6), Inches(7.0), Inches(3.2), Inches(0.4),
         "© 2026 Xavier Lelong pour INDIE.CO",
         font=F_MONO, size=8, color=IVORY, bold=True)

# =============================================================
prs.save(OUT)
print(f"✓ Généré : {OUT}")
print(f"  {len(prs.slides)} slides · format 16:9 (13.333 x 7.5\")")
