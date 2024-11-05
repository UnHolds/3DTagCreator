from build123d import *
from ocp_vscode import *
import segno
import braille

def get_qr_code_matrix(url: str) -> list:
    video_qr = segno.make(url)
    return [[bit for bit in byte] for byte in video_qr.matrix]

def get_qr_code_obj(url: str, pixel_size: float, thickness: float) -> BuildPart:
    matrix = get_qr_code_matrix(url)
    with BuildPart() as pixels:
        for (y, rows) in enumerate(matrix):
            for (x, cell) in filter(lambda cell: cell[1] == 1, enumerate(rows)):
                    with BuildSketch() as _:
                        with Locations((y * pixel_size, x * pixel_size)):
                            Rectangle(pixel_size, pixel_size)
        extrude(amount=thickness)
        return pixels

def single_braille_obj(char: str, dot_diameter: int, additional_thickness: int, fillet_percent: float) -> BuildPart:
    #small value hack
    fillet_percent = 0.9999 if fillet_percent == 1 and additional_thickness == 0 else fillet_percent
    with BuildPart() as braille_part:
        for (x,y) in map(lambda v1: (v1[0] % 2, 2 - (v1[0] // 2)), filter(lambda v2: v2[1] == '1', enumerate(braille.lookup_table[char]))):
            # 5/3 is close enough to the ration
            with Locations((x * dot_diameter * 5/3, y * dot_diameter * 5/3)):
                Cylinder(radius=dot_diameter/2, height=additional_thickness + dot_diameter/2, align=Align.MIN)
                if fillet_percent != 0:
                    fillet(braille_part.edges().sort_by(Axis.Z)[-1], radius=(dot_diameter/2 * fillet_percent))
        return braille_part

def braile_text_obj(text: str, dot_diameter: int, additional_thickness: int, fillet_percent: float) -> BuildPart:
    text = braille.mk_braille_rdy(text)
    with BuildPart() as braille_part:
        for (i, c) in enumerate(text):
            with Locations((i * dot_diameter * 4.267, 0)):
                add(single_braille_obj(c, dot_diameter, additional_thickness, fillet_percent).part)
        return braille_part

def get_text_obj(text: str, font_size: int, thickness: float, font="Overpass", fillet_radius=0.2) -> BuildPart:
    with BuildPart() as text_part:
        with BuildSketch() as _:
            Text(text, font_size=font_size, align=(Align.MIN, Align.MIN), font=font)
        extrude(amount=thickness, both=False)
        if fillet_radius > 0:
            edges = text_part.edges().sort_by(Axis.Z)
            top_edge = edges[-1]
            top_edges = ShapeList(filter(lambda e: abs(top_edge.position.Z - e.position.Z) < 0.001, edges))
            fillet(top_edges, radius=fillet_radius)
        return text_part

def get_plate_obj(length: float, width: float, thickness: float, fillet_radius: float) -> BuildPart:
    with BuildPart() as plate:
        Box(length, width, thickness, align=Align.MIN)
        fillet(plate.edges().filter_by(Axis.Z), radius=fillet_radius)
        return plate


def assemble_plate():
    qr_code_obj = get_qr_code_obj(url='https://gebaerden-archiv.at/sign/30913', pixel_size=2, thickness=2)
    qr_code_length = bounding_box(qr_code_obj.part).edges().sort_by(Axis.Z)[0].length

    # the following length calculation assume that the length in the x-axis is always bigger than in the y-axis
    # sorted by: [y (smaller), x (bigger)]
    braille_obj = braile_text_obj(text='Kaffee', dot_diameter=4, additional_thickness=0, fillet_percent=0)
    braille_length = sorted(map(lambda e: e.length, bounding_box(braille_obj.part).edges().sort_by(Axis.Z)[:4]))[1:3]

    text_obj = get_text_obj(text="hello", font_size=10, thickness=2)
    text_length = sorted(map(lambda e: e.length, bounding_box(text_obj.part).edges().sort_by(Axis.Z)[:4]))[1:3]

    x_length = qr_code_length + max(braille_length[1], text_length[1])
    y_length = max(qr_code_length, braille_length[0], text_length[0])

    plate_obj = get_plate_obj(length=x_length, width=y_length, thickness=1, fillet_radius=1)

    show_all()
assemble_plate()
