from build123d import *
from ocp_vscode import *
import segno


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

matrix = get_qr_code_matrix('https://gebaerden-archiv.at/sign/30718')
show(get_qr_code_obj(matrix, 2, 7))
