#!/usr/bin/env python3
"""Build the P1 PDF and editable vector diagrams from docs/p1/relatorio.md."""
from pathlib import Path
import re
import textwrap

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak,
    Table, TableStyle, Preformatted, Flowable,
)
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon, Circle
from reportlab.graphics import renderSVG, renderPDF

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs/p1/relatorio.md"
OUT = ROOT / "docs/p1/P1_IAL214_Grupo2.pdf"
NAVY = colors.HexColor("#183C32")
GREEN = colors.HexColor("#3E7257")
SAGE = colors.HexColor("#E8F0E9")
PALE = colors.HexColor("#F4F7F4")
GOLD = colors.HexColor("#C69645")
INK = colors.HexColor("#202A25")
MUTED = colors.HexColor("#64736A")
GRID = colors.HexColor("#D4DED7")
WHITE = colors.white


class GraphicFlowable(Flowable):
    def __init__(self, drawing, scale=1):
        super().__init__()
        self.drawing = drawing
        self.scale_factor = scale
        self.width = drawing.width * scale
        self.height = drawing.height * scale

    def wrap(self, avail_width, avail_height):
        return (self.width, self.height)

    def draw(self):
        self.canv.saveState()
        self.canv.scale(self.scale_factor, self.scale_factor)
        renderPDF.draw(self.drawing, self.canv, 0, 0)
        self.canv.restoreState()


def box(d, x, y, w, h, title, detail="", fill=PALE, title_size=9, detail_size=7.2):
    d.add(Rect(x, y, w, h, fillColor=fill, strokeColor=GRID, strokeWidth=0.8))
    d.add(String(x + 8, y + h - 16, title, fontName="Helvetica-Bold", fontSize=title_size, fillColor=NAVY))
    if detail:
        lines = detail.split("\n")
        for i, line in enumerate(lines):
            d.add(String(x + 8, y + h - 29 - i * (detail_size + 2), line,
                         fontName="Helvetica", fontSize=detail_size, fillColor=MUTED))


def arrow(d, x1, y1, x2, y2, label=""):
    d.add(Line(x1, y1, x2, y2, strokeColor=GREEN, strokeWidth=1.2))
    dx, dy = x2 - x1, y2 - y1
    if abs(dx) >= abs(dy):
        sign = 1 if dx >= 0 else -1
        d.add(Polygon([x2, y2, x2-6*sign, y2+3, x2-6*sign, y2-3],
                      fillColor=GREEN, strokeColor=GREEN))
    else:
        sign = 1 if dy >= 0 else -1
        d.add(Polygon([x2, y2, x2+3, y2-6*sign, x2-3, y2-6*sign],
                      fillColor=GREEN, strokeColor=GREEN))
    if label:
        d.add(String((x1+x2)/2 - len(label)*1.6, (y1+y2)/2 + 5, label,
                     fontName="Helvetica", fontSize=6.4, fillColor=MUTED))


def current_architecture():
    d = Drawing(520, 194)
    d.add(String(10, 177, "FLUXO ATUAL DOS DADOS DO GRUPO 2", fontName="Helvetica-Bold",
                 fontSize=9, fillColor=NAVY))
    box(d, 10, 111, 112, 43, "Carga historica", "cadastros, leituras, arquivos", SAGE)
    box(d, 10, 36, 112, 43, "Simulador ao vivo", "sensores e maquinas")
    box(d, 164, 127, 104, 42, "MariaDB", "cadastro e operacoes")
    box(d, 164, 71, 104, 42, "MongoDB", "leituras e telemetria")
    box(d, 164, 15, 104, 42, "MinIO", "NDVI e laudo de solo")
    box(d, 314, 71, 98, 42, "Broker MQTT", "topicos do grupo", SAGE)
    box(d, 433, 71, 78, 42, "Redis", "estado recente")
    arrow(d, 122, 132, 158, 148)
    arrow(d, 122, 132, 158, 92)
    arrow(d, 122, 132, 158, 36)
    arrow(d, 122, 57, 308, 92)
    arrow(d, 122, 53, 428, 82)
    d.add(Line(267, 77, 267, 58, strokeColor=GOLD, strokeWidth=1,
               strokeDashArray=[3, 2]))
    d.add(String(271, 63, "chave MinIO", fontName="Helvetica", fontSize=6.2, fillColor=MUTED))
    d.add(String(287, 10, "Historico MongoDB termina em 29/09/2026; MQTT nao persiste nele automaticamente.",
                 fontName="Helvetica-Oblique", fontSize=6.7, fillColor=MUTED))
    return d


def proposed_architecture():
    d = Drawing(520, 204)
    d.add(String(10, 187, "ARQUITETURA PROPOSTA PARA A P2", fontName="Helvetica-Bold",
                 fontSize=9, fillColor=NAVY))
    box(d, 10, 145, 84, 40, "Gerente", "navegador", SAGE)
    box(d, 126, 145, 130, 40, "Container web", "monolito modular · :8000", SAGE)
    box(d, 370, 153, 138, 34, "MariaDB", "cadastros e custos")
    box(d, 370, 109, 138, 34, "MongoDB", "historico e alertas")
    box(d, 370, 65, 138, 34, "Redis", "estado recente")
    box(d, 370, 21, 138, 34, "MinIO", "mapas e laudo")
    box(d, 10, 0, 84, 36, "Sensores", "e maquinas")
    box(d, 126, 0, 92, 36, "Broker MQTT", "topicos do grupo")
    box(d, 246, 0, 98, 36, "Coletor", "validar, deduplicar")
    arrow(d, 94, 165, 120, 165)
    d.add(Line(256, 165, 282, 165, strokeColor=GREEN, strokeWidth=1.2))
    d.add(Line(282, 38, 282, 165, strokeColor=GREEN, strokeWidth=1.2))
    for yy in (170, 126, 82, 38):
        arrow(d, 282, yy, 366, yy)
    arrow(d, 94, 18, 120, 18)
    arrow(d, 218, 18, 240, 18)
    # Collector writes are gold to distinguish the continuous ingestion path.
    d.add(Line(344, 27, 362, 112, strokeColor=GOLD, strokeWidth=1.4))
    d.add(Polygon([362,112,355,108,360,106], fillColor=GOLD, strokeColor=GOLD))
    d.add(Line(344, 16, 362, 80, strokeColor=GOLD, strokeWidth=1.4))
    d.add(Polygon([362,80,355,77,360,74], fillColor=GOLD, strokeColor=GOLD))
    d.add(String(354, 8, "Porta publica do grupo: confirmar. Coletor sem porta publica.",
                 fontName="Helvetica-Oblique", fontSize=6.5, fillColor=MUTED))
    return d


def screen_frame(title, subtitle, variant):
    d = Drawing(520, 300)
    d.add(Rect(1, 1, 518, 298, fillColor=WHITE, strokeColor=GRID, strokeWidth=1))
    d.add(Rect(1, 257, 518, 42, fillColor=NAVY, strokeColor=NAVY))
    d.add(String(16, 281, "BOA VISTA | PAINEL DE CAMPO", fontName="Helvetica-Bold", fontSize=10, fillColor=WHITE))
    d.add(String(16, 266, title, fontName="Helvetica", fontSize=8, fillColor=colors.HexColor("#DCE9DF")))
    d.add(Rect(1, 1, 90, 256, fillColor=PALE, strokeColor=GRID, strokeWidth=.5))
    nav = ["Visao geral", "Talhoes", "Operacoes", "NDVI e solo"]
    for i, label in enumerate(nav):
        y = 225 - i * 32
        active = (variant == i)
        if active:
            d.add(Rect(9, y-7, 75, 22, fillColor=SAGE, strokeColor=SAGE))
        d.add(String(16, y, label, fontName="Helvetica-Bold" if active else "Helvetica",
                     fontSize=7.5, fillColor=NAVY if active else MUTED))
    d.add(String(106, 235, subtitle, fontName="Helvetica-Bold", fontSize=11, fillColor=NAVY))
    d.add(String(106, 220, "Fazenda Boa Vista  |  atualizado em --/--/---- --:-- BRT",
                 fontName="Helvetica", fontSize=6.8, fillColor=MUTED))
    return d


def wireframe_overview():
    d = screen_frame("Visao geral", "Resumo da fazenda", 0)
    metrics = [(106, 171, "255 ha", "area divulgada"), (207, 171, "6", "talhoes"),
               (308, 171, "--", "sensores online"), (409, 171, "--", "alertas recentes")]
    for x,y,a,b in metrics:
        d.add(Rect(x,y,91,42,fillColor=PALE,strokeColor=GRID))
        d.add(String(x+8,y+24,a,fontName="Helvetica-Bold",fontSize=12,fillColor=NAVY))
        d.add(String(x+8,y+9,b,fontName="Helvetica",fontSize=6.3,fillColor=MUTED))
    d.add(Rect(106,66,253,91,fillColor=WHITE,strokeColor=GRID))
    d.add(String(116,143,"Umidade por talhao - ultimas 24 h",fontName="Helvetica-Bold",fontSize=8,fillColor=NAVY))
    for i in range(5):
        d.add(Line(120,83+i*11,348,83+i*11,strokeColor=GRID,strokeWidth=.45))
    pts=[(123,91),(161,102),(197,97),(234,119),(269,111),(306,132),(344,125)]
    for a,b in zip(pts,pts[1:]): d.add(Line(a[0],a[1],b[0],b[1],strokeColor=GREEN,strokeWidth=1.6))
    d.add(Rect(371,66,132,91,fillColor=WHITE,strokeColor=GRID))
    d.add(String(381,143,"Alertas recentes",fontName="Helvetica-Bold",fontSize=8,fillColor=NAVY))
    for i, s in enumerate(["Solo seco  |  T03", "Sensor offline  |  SS-04", "Chuva intensa  |  area"]):
        y=121-i*22
        d.add(Circle(383,y+2,3,fillColor=GOLD,strokeColor=GOLD))
        d.add(String(391,y,s,fontName="Helvetica",fontSize=6.4,fillColor=INK))
    d.add(String(106,49,"Fontes: MariaDB, MongoDB, Redis e MQTT. Exibir a origem e a atualidade junto a cada valor.",
                 fontName="Helvetica-Oblique",fontSize=6.5,fillColor=MUTED))
    return d


def wireframe_sensors():
    d = screen_frame("Talhoes", "Talhao T03 e sensores", 1)
    d.add(Rect(106,187,397,28,fillColor=PALE,strokeColor=GRID))
    d.add(String(117,198,"Talhao [T03 v]    Periodo [ultimos 7 dias v]    Sensor [SS-03 v]",
                 fontName="Helvetica",fontSize=7,fillColor=INK))
    d.add(Rect(106,70,397,105,fillColor=WHITE,strokeColor=GRID))
    d.add(String(117,160,"Umidade do solo por profundidade (%)",fontName="Helvetica-Bold",fontSize=8,fillColor=NAVY))
    for i in range(4): d.add(Line(128,92+i*15,486,92+i*15,strokeColor=GRID,strokeWidth=.45))
    p1=[(130,103),(177,111),(221,107),(268,128),(313,122),(360,140),(408,130),(482,146)]
    p2=[(130,94),(177,100),(221,99),(268,112),(313,108),(360,122),(408,119),(482,129)]
    for pts,col in [(p1,GREEN),(p2,GOLD)]:
        for a,b in zip(pts,pts[1:]): d.add(Line(a[0],a[1],b[0],b[1],strokeColor=col,strokeWidth=1.5))
    d.add(String(117,52,"Qualidade: duplicatas -- | intervalos sem leitura -- | firmware -- | ultima leitura --",
                 fontName="Helvetica",fontSize=6.8,fillColor=MUTED))
    return d


def wireframe_costs():
    d = screen_frame("Operacoes", "Operacoes e custos", 2)
    d.add(Rect(106,187,397,28,fillColor=PALE,strokeColor=GRID))
    d.add(String(117,198,"Safra [2025/26 v]     Talhao [todos v]     Periodo [01/06 - 29/09]",
                 fontName="Helvetica",fontSize=7,fillColor=INK))
    d.add(Rect(106,70,397,105,fillColor=WHITE,strokeColor=GRID))
    d.add(Rect(107,151,395,23,fillColor=SAGE,strokeColor=SAGE))
    cols=[(116,"Operacao"),(231,"Qtd."),(286,"Custo total"),(365,"Talhao"),(431,"Periodo")]
    for x,s in cols: d.add(String(x,159,s,fontName="Helvetica-Bold",fontSize=6.8,fillColor=NAVY))
    rows=[("Adubacao","--","R$ --","T01-T06","--"),("Pulverizacao","--","R$ --","T01-T06","--"),("Colheita","--","R$ --","T02/T03","--")]
    for j,row in enumerate(rows):
        y=133-j*22
        d.add(Line(107,y-7,502,y-7,strokeColor=GRID,strokeWidth=.5))
        for (x,_),val in zip(cols,row): d.add(String(x,y,val,fontName="Helvetica",fontSize=6.8,fillColor=INK))
    d.add(String(106,51,"Origem: MariaDB operacao + safra + talhao; telemetria de maquina opcional via MongoDB.",
                 fontName="Helvetica-Oblique",fontSize=6.5,fillColor=MUTED))
    return d


def wireframe_ndvi():
    d = screen_frame("NDVI e solo", "Imagens e analise de solo", 3)
    d.add(Rect(106,187,397,28,fillColor=PALE,strokeColor=GRID))
    d.add(String(117,198,"Talhao [T03 v]     Data da imagem [--/--/---- v]     Cobertura de nuvem: --%",
                 fontName="Helvetica",fontSize=7,fillColor=INK))
    d.add(Rect(106,60,190,111,fillColor=PALE,strokeColor=GRID))
    d.add(String(117,157,"Mapa NDVI - imagem MinIO",fontName="Helvetica-Bold",fontSize=8,fillColor=NAVY))
    d.add(Rect(124,78,154,66,fillColor=colors.HexColor("#DDE7D5"),strokeColor=GRID))
    d.add(Polygon([130,84,180,82,194,96,186,111,165,115,153,138,135,130],fillColor=colors.HexColor("#79A765"),strokeColor=WHITE,strokeWidth=1))
    d.add(Polygon([194,96,216,85,268,90,270,123,238,136,186,111],fillColor=colors.HexColor("#CF9A58"),strokeColor=WHITE,strokeWidth=1))
    d.add(Rect(309,60,194,111,fillColor=WHITE,strokeColor=GRID))
    d.add(String(320,157,"Analise de solo - laudo CSV",fontName="Helvetica-Bold",fontSize=8,fillColor=NAVY))
    for i, label in enumerate(["pH", "Materia organica", "Fosforo (P)", "Potassio (K)"]):
        y=137-i*17
        d.add(String(320,y,label,fontName="Helvetica",fontSize=7,fillColor=INK))
        d.add(String(440,y,"--",fontName="Helvetica-Bold",fontSize=7,fillColor=NAVY))
    d.add(String(106,43,"Catalogo e NDVI medio: MongoDB imagens. Binario do mapa e laudo: MinIO.",
                 fontName="Helvetica-Oblique",fontSize=6.5,fillColor=MUTED))
    return d


def export_assets():
    assets = {
        "docs/p1/arquitetura/atual.svg": current_architecture(),
        "docs/p1/arquitetura/proposta.svg": proposed_architecture(),
        "docs/p1/wireframes/01-visao-geral.svg": wireframe_overview(),
        "docs/p1/wireframes/02-talhao-sensores.svg": wireframe_sensors(),
        "docs/p1/wireframes/03-operacoes-custos.svg": wireframe_costs(),
        "docs/p1/wireframes/04-ndvi-solo.svg": wireframe_ndvi(),
    }
    for relative, drawing in assets.items():
        renderSVG.drawToFile(drawing, str(ROOT / relative))
    return assets


def make_styles():
    s = getSampleStyleSheet()
    s.add(ParagraphStyle(name="CoverTitle", parent=s["Title"], fontName="Helvetica-Bold",
                         fontSize=26, leading=31, textColor=NAVY, alignment=TA_LEFT,
                         spaceAfter=12))
    s.add(ParagraphStyle(name="CoverSub", parent=s["Normal"], fontName="Helvetica",
                         fontSize=12, leading=17, textColor=GREEN, spaceAfter=7))
    s.add(ParagraphStyle(name="H1x", parent=s["Heading1"], fontName="Helvetica-Bold",
                         fontSize=16, leading=20, textColor=NAVY, spaceBefore=12, spaceAfter=8,
                         keepWithNext=True))
    s.add(ParagraphStyle(name="H2x", parent=s["Heading2"], fontName="Helvetica-Bold",
                         fontSize=11, leading=14, textColor=GREEN, spaceBefore=10, spaceAfter=5,
                         keepWithNext=True))
    s.add(ParagraphStyle(name="Bodyx", parent=s["BodyText"], fontName="Helvetica",
                         fontSize=8.8, leading=12.4, textColor=INK, spaceAfter=6))
    s.add(ParagraphStyle(name="Smallx", parent=s["BodyText"], fontName="Helvetica",
                         fontSize=7.4, leading=9.8, textColor=INK, spaceAfter=1))
    s.add(ParagraphStyle(name="TableHead", parent=s["BodyText"], fontName="Helvetica-Bold",
                         fontSize=7.1, leading=8.7, textColor=WHITE))
    s.add(ParagraphStyle(name="TableCell", parent=s["BodyText"], fontName="Helvetica",
                         fontSize=6.9, leading=8.7, textColor=INK))
    s.add(ParagraphStyle(name="Note", parent=s["BodyText"], fontName="Helvetica-Bold",
                         fontSize=8.1, leading=11, textColor=NAVY, backColor=SAGE,
                         borderColor=GREEN, borderWidth=.5, borderPadding=8,
                         spaceBefore=14, spaceAfter=8))
    s.add(ParagraphStyle(name="CodeHead", parent=s["BodyText"], fontName="Helvetica-Bold",
                         fontSize=8.2, leading=10, textColor=GREEN, spaceBefore=6, spaceAfter=4,
                         keepWithNext=True))
    s.add(ParagraphStyle(name="Caption", parent=s["BodyText"], fontName="Helvetica-Oblique",
                         fontSize=7, leading=9, textColor=MUTED, alignment=TA_CENTER,
                         spaceBefore=3, spaceAfter=8))
    return s


def inline_markup(text):
    # Escape plain text first, then restore the small Markdown subset used by the report.
    from xml.sax.saxutils import escape
    codes = []
    links = []
    def save_code(match):
        codes.append(match.group(1))
        return f"CODETOKEN{len(codes)-1}TOKEN"
    def save_link(match):
        links.append((match.group(1), match.group(2)))
        return f"LINKTOKEN{len(links)-1}TOKEN"
    prepared = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", save_link, text.strip())
    out = escape(re.sub(r"`([^`]+)`", save_code, prepared))
    out = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", out)
    out = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", out)
    for i, code in enumerate(codes):
        out = out.replace(f"CODETOKEN{i}TOKEN", f"<font name='Courier' size='7.4'>{escape(code)}</font>")
    for i, (label, url) in enumerate(links):
        out = out.replace(f"LINKTOKEN{i}TOKEN", f"<link href='{escape(url)}' color='#3E7257'>{escape(label)}</link>")
    return out


def parse_table(lines, styles, page_width):
    data = []
    for idx, line in enumerate(lines):
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if idx == 1 and all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in cells):
            continue
        style = styles["TableHead"] if not data else styles["TableCell"]
        data.append([Paragraph(inline_markup(cell), style) for cell in cells])
    if not data:
        return Spacer(1, 1)
    cols = max(len(row) for row in data)
    widths = [page_width / cols] * cols
    # Give the first field narrower room in repeated records; preserve total width.
    if cols >= 3:
        widths[0] = page_width * .17
        rest = (page_width - widths[0]) / (cols - 1)
        widths[1:] = [rest] * (cols - 1)
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), NAVY),
        ("GRID", (0,0), (-1,-1), .35, GRID),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, PALE]),
    ]))
    return t


def parse_report(assets, styles, page_width):
    lines = REPORT.read_text(encoding="utf-8").splitlines()
    story = []
    paragraph = []
    code = []
    in_code = False
    table = []
    title_done = False
    drawings_by_ref = {
        "arquitetura/atual.svg": assets["docs/p1/arquitetura/atual.svg"],
        "arquitetura/proposta.svg": assets["docs/p1/arquitetura/proposta.svg"],
        "wireframes/01-visao-geral.svg": assets["docs/p1/wireframes/01-visao-geral.svg"],
        "wireframes/02-talhao-sensores.svg": assets["docs/p1/wireframes/02-talhao-sensores.svg"],
        "wireframes/03-operacoes-custos.svg": assets["docs/p1/wireframes/03-operacoes-custos.svg"],
        "wireframes/04-ndvi-solo.svg": assets["docs/p1/wireframes/04-ndvi-solo.svg"],
    }

    def flush_para():
        if paragraph:
            text = " ".join(x.strip() for x in paragraph)
            if text:
                story.append(Paragraph(inline_markup(text), styles["Bodyx"]))
            paragraph.clear()

    def flush_table():
        if table:
            story.append(parse_table(table, styles, page_width))
            story.append(Spacer(1, 7))
            table.clear()

    for raw in lines:
        line = raw.rstrip()
        if line.startswith("```"):
            flush_para(); flush_table()
            if in_code:
                wrapped = []
                for c in code:
                    if len(c) > 99:
                        indent = len(c) - len(c.lstrip())
                        wrapped.extend(textwrap.wrap(c.strip(), width=99, subsequent_indent=" " * (indent + 2),
                                                     break_long_words=False, break_on_hyphens=False))
                    else:
                        wrapped.append(c)
                story.append(Preformatted("\n".join(wrapped), ParagraphStyle(
                    name="Code", fontName="Courier", fontSize=6.6, leading=8.2,
                    textColor=INK, backColor=PALE, borderColor=GRID, borderWidth=.4,
                    borderPadding=6, spaceBefore=2, spaceAfter=7)))
                code.clear()
                in_code = False
            else:
                in_code = True
            continue
        if in_code:
            code.append(line)
            continue
        if line.startswith("|"):
            flush_para()
            table.append(line)
            continue
        else:
            flush_table()
        if not line.strip():
            flush_para()
            continue
        image = re.match(r"!\[(.*?)\]\((.*?)\)", line.strip())
        if image:
            flush_para()
            alt, ref = image.groups()
            base = ref.split("/", 1)[-1] if ref.startswith("../") else ref
            drawing = drawings_by_ref.get(ref)
            if drawing is None:
                # Resolve paths relative to docs/p1; references may have a leading ../.
                for k, v in drawings_by_ref.items():
                    if ref.endswith(k): drawing = v; break
            if drawing:
                maxw = page_width
                maxh = 245 if "wireframes/" in ref else 190
                scale = min(maxw / drawing.width, maxh / drawing.height, 1)
                story.append(GraphicFlowable(drawing, scale))
                story.append(Paragraph(inline_markup(alt), styles["Caption"]))
            continue
        if line.startswith("# "):
            flush_para()
            if title_done:
                story.append(PageBreak())
            story.append(Paragraph(inline_markup(line[2:]), styles["CoverTitle"]))
            title_done = True
            continue
        if line.startswith("## "):
            flush_para()
            heading = line[3:]
            # First numbered section starts after the title metadata on cover.
            if re.match(r"^[1-6]\. ", heading) and not any(isinstance(x, PageBreak) for x in story):
                story.append(PageBreak())
            story.append(Paragraph(inline_markup(heading), styles["H1x"]))
            continue
        if line.startswith("### "):
            flush_para(); story.append(Paragraph(inline_markup(line[4:]), styles["H2x"]))
            continue
        if line.startswith("> "):
            flush_para(); story.append(Paragraph(inline_markup(line[2:]), styles["Note"]))
            continue
        if line.startswith("- "):
            flush_para(); story.append(Paragraph("&bull; " + inline_markup(line[2:]), styles["Bodyx"]))
            continue
        if re.match(r"^\*\*[^*]+\*\*", line):
            flush_para(); story.append(Paragraph(inline_markup(line), styles["CodeHead"]))
            continue
        paragraph.append(line)
    flush_para(); flush_table()
    return story


def page_decoration(canvas, doc):
    canvas.saveState()
    width, height = letter
    page = canvas.getPageNumber()
    if page > 1:
        canvas.setStrokeColor(GRID)
        canvas.setLineWidth(.5)
        canvas.line(.68*inch, height-.48*inch, width-.68*inch, height-.48*inch)
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(MUTED)
        canvas.drawString(.68*inch, height-.38*inch, "IAL214  |  Grupo 2  |  Fazenda Boa Vista")
        canvas.drawRightString(width-.68*inch, .38*inch, f"Versao de trabalho  |  {page}")
    canvas.restoreState()


def build_pdf(assets):
    styles = make_styles()
    doc = BaseDocTemplate(str(OUT), pagesize=letter,
                          leftMargin=.68*inch, rightMargin=.68*inch,
                          topMargin=.68*inch, bottomMargin=.62*inch,
                          title="P1 IAL214 Grupo 2 - Estudo dos dados e escopo",
                          author="Grupo 2 - Fazenda Boa Vista")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id="normal")
    doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=page_decoration)])
    story = [Spacer(1, .45*inch)]
    story.extend(parse_report(assets, styles, doc.width))
    doc.build(story)


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    assets = export_assets()
    build_pdf(assets)
    print(f"Created {OUT}")
