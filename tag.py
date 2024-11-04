from build123d import *
from ocp_vscode import *
import segno
import braille

def get_qr_code_matrix(url: str) -> list:
    video_qr = segno.make(url)
    return [[bit for bit in byte] for byte in video_qr.matrix]

def get_qr_code_obj(matrix: list, dot_size: float, thickness: float) -> BuildPart:
    with BuildPart() as pixels:
        for (y, rows) in enumerate(matrix):
            for (x, cell) in filter(lambda cell: cell[1] == 1, enumerate(rows)):
                    with BuildSketch() as _:
                        with Locations((y * dot_size, x * dot_size)):
                            Rectangle(dot_size, dot_size)
        extrude(amount=thickness)
        return pixels

def single_braille_obj(char: str, diameter: int, additional_thickness: int, fillet_percent: float) -> BuildPart:
    #small value hack
    fillet_percent = 0.9999 if fillet_percent == 1 and additional_thickness == 0 else fillet_percent
    with BuildPart() as braille_part:
        for (x,y) in map(lambda v1: (v1[0] % 2, 2 - (v1[0] // 2)), filter(lambda v2: v2[1] == '1', enumerate(braille.lookup_table[char]))):
            # 5/3 is close enough to the ration
            with Locations((x * diameter * 5/3, y * diameter * 5/3)):
                Cylinder(radius=diameter/2, height=additional_thickness + diameter/2)
                if fillet_percent != 0:
                    fillet(braille_part.edges().sort_by(Axis.Z)[-1], radius=(diameter/2 * fillet_percent))
        return braille_part

def braile_text_obj(text: str, diameter: int, additional_thickness: int, fillet_percent: float) -> BuildPart:
    text = braille.mk_braille_rdy(text)
    with BuildPart() as braille_part:
        for (i, c) in enumerate(text):
            with Locations((i * diameter * 4.267, 0)):
                add(single_braille_obj(c, diameter, additional_thickness, fillet_percent).part)
        return braille_part


matrix = get_qr_code_matrix('https://gebaerden-archiv.at/sign/30718')
#get_qr_code_obj(matrix, 2, 7)
show(braile_text_obj('abcdefghijklmnopqrstuvwxyz1234567890', 1.5, 0, 0))

#4,125
# 4,26
#4,42
