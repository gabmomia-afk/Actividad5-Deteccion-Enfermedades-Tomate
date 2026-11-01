
from pathlib import Path
from xml.sax.saxutils import escape

import markdown
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, KeepTogether
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from html.parser import HTMLParser


CARPETA = Path(__file__).resolve().parent

ESTILOS = getSampleStyleSheet()
ESTILOS.add(ParagraphStyle(
    name="TituloOruga",
    parent=ESTILOS["Heading1"],
    fontSize=19,
    leading=24,
    textColor=colors.HexColor("#21643A"),
    spaceAfter=14,
))
ESTILOS.add(ParagraphStyle(
    name="SubtituloOruga",
    parent=ESTILOS["Heading2"],
    fontSize=13,
    leading=17,
    textColor=colors.HexColor("#21643A"),
    spaceBefore=12,
    spaceAfter=7,
))
ESTILOS.add(ParagraphStyle(
    name="TextoOruga",
    parent=ESTILOS["BodyText"],
    fontSize=9,
    leading=14,
    spaceAfter=7,
))
ESTILOS.add(ParagraphStyle(
    name="CeldaOruga",
    parent=ESTILOS["BodyText"],
    fontSize=7,
    leading=10,
))
ESTILOS.add(ParagraphStyle(
    name="CodigoOruga",
    parent=ESTILOS["BodyText"],
    fontName="Courier",
    fontSize=7,
    leading=11,
    spaceAfter=7,
))


class ConvertidorHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.elementos = []
        self.texto = ""
        self.tabla = []
        self.fila = []
        self.en_tabla = False
        self.en_celda = False
        self.en_codigo = False
        self.bloque = None

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.en_tabla = True
            self.tabla = []
        elif tag == "tr":
            self.fila = []
        elif tag in ("td", "th"):
            self.en_celda = True
            self.texto = ""
        elif tag == "pre":
            self.en_codigo = True
            self.texto = ""
        elif tag in ("h1", "h2", "h3", "p", "li"):
            self.bloque = tag
            self.texto = ""
        elif tag == "strong":
            self.texto += "<b>"
        elif tag == "em":
            self.texto += "<i>"
        elif tag == "br":
            self.texto += "<br/>"

    def handle_endtag(self, tag):
        if tag in ("td", "th"):
            self.fila.append(
                Paragraph(self.texto.strip(), ESTILOS["CeldaOruga"])
            )
            self.en_celda = False
            self.texto = ""
        elif tag == "tr":
            if self.fila:
                self.tabla.append(self.fila)
        elif tag == "table":
            if self.tabla:
                tabla = Table(
                    self.tabla,
                    repeatRows=1,
                    hAlign="LEFT"
                )
                tabla.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0),
                     colors.HexColor("#DDEEE2")),
                    ("GRID", (0, 0), (-1, -1),
                     0.4, colors.HexColor("#CCCCCC")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 6),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]))
                self.elementos.append(tabla)
                self.elementos.append(Spacer(1, 10))
            self.en_tabla = False
        elif tag == "pre":
            contenido = escape(self.texto.strip()).replace("\n", "<br/>")
            self.elementos.append(
                Paragraph(contenido, ESTILOS["CodigoOruga"])
            )
            self.en_codigo = False
            self.texto = ""
        elif tag in ("h1", "h2", "h3", "p", "li"):
            if not self.en_tabla and not self.en_codigo:
                estilo = (
                    "TituloOruga" if tag == "h1"
                    else "SubtituloOruga" if tag in ("h2", "h3")
                    else "TextoOruga"
                )
                contenido = self.texto.strip()
                if tag == "li":
                    contenido = "• " + contenido
                if contenido:
                    self.elementos.append(
                        Paragraph(contenido, ESTILOS[estilo])
                    )
            self.bloque = None
            self.texto = ""
        elif tag == "strong":
            self.texto += "</b>"
        elif tag == "em":
            self.texto += "</i>"

    def handle_data(self, data):
        self.texto += escape(data) if not self.en_codigo else data


def generar_pdf(nombre):
    origen = CARPETA / f"{nombre}.md"
    destino = CARPETA / f"{nombre}.pdf"

    contenido = origen.read_text(encoding="utf-8")
    html = markdown.markdown(
        contenido,
        extensions=["tables", "fenced_code"]
    )

    convertidor = ConvertidorHTML()
    convertidor.feed(html)

    for elemento in convertidor.elementos:
        if isinstance(elemento, Paragraph):
            if elemento.style.name in ("TituloOruga", "SubtituloOruga"):
                elemento.keepWithNext = True

    documento = SimpleDocTemplate(
        str(destino),
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    documento.build(convertidor.elementos)
    print(f"PDF generado: {destino}")


if __name__ == "__main__":
    generar_pdf("manual_despliegue")
    generar_pdf("reporte_validacion")
