from io import BytesIO

import markdown
from bs4 import BeautifulSoup
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Preformatted,
)


def markdown_to_pdf(markdown_text: str) -> bytes:
    """
    Convert Markdown text to PDF bytes without creating
    an intermediate or output file.
    """

    # Markdown → HTML
    html = markdown.markdown(
        markdown_text,
        extensions=[
            "extra",
            "tables",
            "fenced_code",
            "toc",
        ],
    )

    soup = BeautifulSoup(html, "html.parser")

    # PDF in memory
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="TitleCustom",
            parent=styles["Title"],
            alignment=TA_CENTER,
            spaceAfter=20,
        )
    )

    styles.add(
        ParagraphStyle(
            name="CodeCustom",
            parent=styles["Code"],
            fontName="Courier",
            fontSize=8,
            leading=10,
            backColor=colors.whitesmoke,
            borderPadding=6,
        )
    )

    story = []

    for element in soup.find_all(recursive=False):

        tag = element.name
        text = element.get_text(" ", strip=True)

        if not text and tag not in ("pre",):
            continue

        # Headings
        if tag == "h1":
            story.append(
                Paragraph(text, styles["TitleCustom"])
            )

        elif tag == "h2":
            story.append(
                Paragraph(text, styles["Heading1"])
            )

        elif tag == "h3":
            story.append(
                Paragraph(text, styles["Heading2"])
            )

        # Paragraph
        elif tag == "p":
            story.append(
                Paragraph(
                    str(element),
                    styles["BodyText"],
                )
            )

            story.append(Spacer(1, 6))

        # Code block
        elif tag == "pre":
            code = element.get_text()

            story.append(
                Preformatted(
                    code,
                    styles["CodeCustom"],
                )
            )

            story.append(Spacer(1, 8))

        # Lists
        elif tag in ("ul", "ol"):

            for index, item in enumerate(
                element.find_all("li", recursive=False),
                start=1,
            ):
                prefix = "•" if tag == "ul" else f"{index}."

                story.append(
                    Paragraph(
                        f"{prefix} {item.get_text(' ', strip=True)}",
                        styles["BodyText"],
                    )
                )

        # Tables
        elif tag == "table":

            rows = []

            for tr in element.find_all("tr"):
                row = [
                    cell.get_text(" ", strip=True)
                    for cell in tr.find_all(["th", "td"])
                ]

                if row:
                    rows.append(row)

            if rows:
                table = Table(
                    rows,
                    repeatRows=1,
                )

                table.setStyle(
                    TableStyle(
                        [
                            (
                                "BACKGROUND",
                                (0, 0),
                                (-1, 0),
                                colors.lightgrey,
                            ),
                            (
                                "GRID",
                                (0, 0),
                                (-1, -1),
                                0.5,
                                colors.grey,
                            ),
                            (
                                "VALIGN",
                                (0, 0),
                                (-1, -1),
                                "TOP",
                            ),
                            (
                                "LEFTPADDING",
                                (0, 0),
                                (-1, -1),
                                6,
                            ),
                            (
                                "RIGHTPADDING",
                                (0, 0),
                                (-1, -1),
                                6,
                            ),
                        ]
                    )
                )

                story.append(table)
                story.append(Spacer(1, 10))

    doc.build(story)

    return buffer.getvalue()