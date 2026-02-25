import adsk.core, adsk.fusion, traceback
import sys, os

# Allow importing from src/ when running inside Fusion 360
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
from spiral import SpiralParams, generate_spiral


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)
        root = design.rootComponent

        sketch = root.sketches.add(root.xYConstructionPlane)
        splines = sketch.sketchCurves.sketchFittedSplines

        params = SpiralParams(r_start=50, r_end=146, turns=25)
        spiral_points = generate_spiral(params)

        collection = adsk.core.ObjectCollection.create()
        for x, y in spiral_points:
            # Fusion 360 uses cm internally; spiral coords are in mm
            collection.add(adsk.core.Point3D.create(x / 10, y / 10, 0))

        splines.add(collection)

    except Exception:
        if ui:
            ui.messageBox("Archimedean spiral failed:\n" + traceback.format_exc())
