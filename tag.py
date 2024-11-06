from build123d import *
from ocp_vscode import *
import segno
import braille

def get_qr_code_matrix(url: str) -> list:
    video_qr = segno.make(url)
    return [[bit for bit in byte] for byte in video_qr.matrix]

def get_qr_code_obj(url: str, pixel_size: float, thickness: float) -> BuildPart:
    matrix = get_qr_code_matrix(url)
    with BuildPart() as qr_code:
        for (y, rows) in enumerate(matrix):
            for (x, _) in filter(lambda cell: cell[1] == 1, enumerate(rows[::-1])):
                    with BuildSketch() as _:
                        with Locations((y * pixel_size + pixel_size, x * pixel_size)):
                            Rectangle(pixel_size, pixel_size, align=(Align.MAX, Align.MIN))
        extrude(amount=thickness)
        qr_code.part.label = 'QR-Code'
        return qr_code

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
        braille_part.part.label = f'Braille-Letter ({char})'
        return braille_part

def braille_text_obj(text: str, dot_diameter: int, additional_thickness: int, fillet_percent: float) -> BuildPart:
    text = braille.mk_braille_rdy(text)
    with BuildPart() as braille_part:
        for (i, c) in enumerate(text):
            with Locations((i * dot_diameter * 4.267, 0)):
                add(single_braille_obj(c, dot_diameter, additional_thickness, fillet_percent).part)
        braille_part.part.label = 'Braille-Text'
        return braille_part

def get_text_obj(text: str, font_size: int, thickness: float, font="Arial", font_style=FontStyle.BOLD, fillet_radius=0.2) -> BuildPart:
    with BuildPart() as text_part:
        with BuildSketch() as _:
            Text(text, font_size=font_size, align=(Align.MIN, Align.MIN), font=font, font_style=font_style)
        extrude(amount=thickness, both=False)
        if fillet_radius > 0:
            edges = text_part.edges().sort_by(Axis.Z)
            top_edge = edges[-1]
            top_edges = ShapeList(filter(lambda e: abs(top_edge.position.Z - e.position.Z) < 0.001, edges))
            try:
                fillet(top_edges, radius=fillet_radius)
            except ValueError:
                max_fillet = text_part.part.max_fillet(top_edges, tolerance=10, max_iterations=100)
                print(f"Fillet radius could not been fulfilled using size max fillet size of: {max_fillet}")
                fillet(top_edges, radius=max_fillet)
        return text_part

def get_plate_obj(length: float, width: float, thickness: float, fillet_radius: float) -> BuildPart:
    with BuildPart() as plate:
        Box(length, width, thickness, align=Align.MIN)
        fillet(plate.edges().filter_by(Axis.Z), radius=fillet_radius)
        plate.part.label = 'Plate'
        return plate


def get_assembled_plate(text: str, url: str, plate_tickness = 1.5, thickness = 1.5, qr_code_pixel_size = 1, braile_dot_diameter = 1.6, font_size = 15, font="Arial", font_style=FontStyle.BOLD, braile_fillet_percent = 1, text_fillet_mm = 0, plate_fillet_mm = 5):
    qr_code_obj = get_qr_code_obj(url=url, pixel_size=qr_code_pixel_size, thickness=thickness)
    qr_code_length = bounding_box(qr_code_obj.part).edges().sort_by(Axis.Z)[0].length

    # the following length calculation assume that the length in the x-axis is always bigger than in the y-axis
    # sorted by: [y (smaller), x (bigger)]
    braille_obj = braille_text_obj(text=text, dot_diameter=braile_dot_diameter, additional_thickness=max(thickness - braile_dot_diameter / 2, 0), fillet_percent=braile_fillet_percent)
    braille_length = sorted(map(lambda e: e.length, bounding_box(braille_obj.part).edges().sort_by(Axis.Z)[:4]))[1:3]

    text_obj = get_text_obj(text=text, font_size=font_size, thickness=thickness, font=font, font_style=font_style, fillet_radius=text_fillet_mm)
    text_length = sorted(map(lambda e: e.length, bounding_box(text_obj.part).edges().sort_by(Axis.Z)[:4]))[1:3]

    x_length = qr_code_length + max(braille_length[1], text_length[1]) + 10 + 5 # 10 = offset both sides; 5 = spacee betwenn qr and text
    y_length = max(qr_code_length, braille_length[0] + text_length[0]) + 10 # 10 = offset both sides;

    plate_obj = get_plate_obj(length=x_length, width=y_length, thickness=plate_tickness, fillet_radius=plate_fillet_mm)

    # move qr code
    qr_code_obj.part.color = Color("blue")
    qr_code_obj.part.move(Location((x_length - qr_code_length - 5, (y_length - qr_code_length) / 2, plate_tickness)))


    print(text_length)
    # move text
    text_obj.part.color = Color("green")
    text_y_pos = (y_length - 5 - braille_length[0]) / 2 - text_length[0]/2 + braille_length[0] + 5
    text_x_pos = (max(braille_length[0], text_length[0]) - text_length[0]) / 2 + 5
    text_obj.part.move(Location((text_x_pos, text_y_pos, plate_tickness)))

    #move braille
    braille_obj.part.color = Color("red")
    braille_x_pos = (max(braille_length[0], text_length[0]) - braille_length[0]) / 2 + 5
    braille_obj.part.move(Location((braille_x_pos, 5, plate_tickness)))

    assembly = Compound(children=[plate_obj.part, qr_code_obj.part, text_obj.part, braille_obj.part])
    assembly.label = 'Tag'

    show(assembly)
get_assembled_plate('Kaffee', 'https://gebaerden-archiv.at/sign/30913')
