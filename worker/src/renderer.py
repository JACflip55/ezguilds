import drawsvg as draw
import cairosvg


CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
SCALE = 6  # multiply plan coordinates by this


def render_svg(plan: dict) -> str:
    d = draw.Drawing(CANVAS_WIDTH, CANVAS_HEIGHT)

    # Background
    d.append(draw.Rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, fill="#1a1f1a"))

    # Title
    d.append(draw.Text(
        plan.get("title", "Site Plan"),
        x=CANVAS_WIDTH / 2, y=30,
        font_size=20, fill="#e8e0d0", text_anchor="middle",
        font_family="sans-serif",
    ))

    # Zones
    for zone in plan.get("zones", []):
        bounds = zone.get("bounds", {})
        x = bounds.get("x", 0) * SCALE
        y = bounds.get("y", 0) * SCALE + 50  # offset for title
        w = bounds.get("width", 50) * SCALE
        h = bounds.get("height", 50) * SCALE
        color = zone.get("color", "#4a6a30")

        # Zone rectangle
        d.append(draw.Rectangle(
            x, y, w, h,
            fill=color, fill_opacity=0.3,
            stroke=color, stroke_width=2,
            rx=8,
        ))

        # Zone label
        d.append(draw.Text(
            zone.get("name", ""),
            x=x + 8, y=y + 18,
            font_size=14, fill="#e8e0d0",
            font_family="sans-serif", font_weight="bold",
        ))

        # Elements within zone
        for elem in zone.get("elements", []):
            ex = elem.get("x", 0) * SCALE
            ey = elem.get("y", 0) * SCALE + 50
            radius = elem.get("radius", 5) * SCALE / 2
            elem_type = elem.get("type", "plant")

            if elem_type == "plant":
                d.append(draw.Circle(
                    ex, ey, radius,
                    fill="#8ab060", fill_opacity=0.6,
                    stroke="#8ab060", stroke_width=1,
                ))
            elif elem_type == "structure":
                d.append(draw.Rectangle(
                    ex - radius, ey - radius, radius * 2, radius * 2,
                    fill="#a89880", fill_opacity=0.5,
                    stroke="#a89880", stroke_width=1,
                ))
            elif elem_type == "water":
                d.append(draw.Circle(
                    ex, ey, radius,
                    fill="#4a7a9a", fill_opacity=0.5,
                    stroke="#4a7a9a", stroke_width=1,
                ))
            elif elem_type == "path":
                d.append(draw.Rectangle(
                    ex - radius, ey - 2, radius * 2, 4,
                    fill="#706850", fill_opacity=0.6,
                ))
            else:
                d.append(draw.Circle(
                    ex, ey, radius,
                    fill=color, fill_opacity=0.4,
                ))

            # Element label
            d.append(draw.Text(
                elem.get("name", ""),
                x=ex, y=ey + radius + 12,
                font_size=10, fill="#d4c8a8",
                text_anchor="middle", font_family="sans-serif",
            ))

    # Annotations
    for ann in plan.get("annotations", []):
        ax = ann.get("x", 0) * SCALE
        ay = ann.get("y", 0) * SCALE + 50
        d.append(draw.Text(
            ann.get("text", ""),
            x=ax, y=ay,
            font_size=12, fill="#a89880",
            font_family="sans-serif", font_style="italic",
        ))

    return d.as_svg()


def svg_to_png(svg_string: str) -> bytes:
    return cairosvg.svg2png(bytestring=svg_string.encode("utf-8"))
