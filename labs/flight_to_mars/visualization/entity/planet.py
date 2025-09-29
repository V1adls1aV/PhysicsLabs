import base64
from pathlib import Path
from typing import Any


def planet_shape(planet_filename: str, x: float, y: float, radius: float) -> dict[str, Any]:
    image_path = Path(__file__).parent.parent / "image" / planet_filename

    with image_path.open("rb") as img_file:
        img_data = base64.b64encode(img_file.read()).decode()

    img_url = f"data:image/png;base64,{img_data}"

    return {
        "source": img_url,
        "xref": "x",
        "yref": "y",
        "x": x - radius,
        "sizex": radius * 2,
        "y": y + radius,
        "sizey": radius * 2,
        "sizing": "stretch",
        "opacity": 1.0,
        "layer": "below",
    }
