import adsk.core, adsk.fusion, traceback
import sys, os

# Vinyl record defaults (Neumann SX-74 standard)
VINYL_R_START      = 50.0  # mm — innermost groove radius
VINYL_R_END        = 146.0 # mm — outermost groove radius
VINYL_TURNS        = 25    # groove count
VINYL_PTS_PER_TURN = 36    # angular resolution (every 10° — smooth without freezing)

# Global handler list — keeps event handlers alive and prevents GC
_handlers = []


def _import_spiral():
    """
    Lazy import of core/spiral.py via sys.path.
    Deferred to call-time so any failure is caught by the caller's try/except
    rather than silently preventing the add-in from loading.
    """
    core_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'core'
    )
    if core_path not in sys.path:
        sys.path.insert(0, core_path)
    from spiral import SpiralParams, generate_spiral
    return SpiralParams, generate_spiral


def _build_point_collection(inputs) -> adsk.core.ObjectCollection:
    """Read dialog inputs and return a Fusion 360 ObjectCollection of Point3D (in cm)."""
    SpiralParams, generate_spiral = _import_spiral()

    r_start         = inputs.itemById('r_start').value * 10   # cm → mm
    r_end           = inputs.itemById('r_end').value * 10     # cm → mm
    turns           = inputs.itemById('turns').value
    points_per_turn = inputs.itemById('points_per_turn').value

    params = SpiralParams(
        r_start=r_start,
        r_end=r_end,
        turns=turns,
        points_per_turn=points_per_turn,
    )
    spiral_points = generate_spiral(params)

    collection = adsk.core.ObjectCollection.create()
    for x, y in spiral_points:
        collection.add(adsk.core.Point3D.create(x / 10, y / 10, 0))  # mm → cm
    return collection


def _get_plane(inputs):
    """Return the selected plane, falling back to XY construction plane."""
    plane_input = inputs.itemById('plane')
    if plane_input.selectionCount > 0:
        return plane_input.selection(0).entity
    design = adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    return design.rootComponent.xYConstructionPlane


class _CommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
        self._origin_state = False

    def notify(self, args):
        try:
            cmd    = adsk.core.Command.cast(args.command)
            inputs = cmd.commandInputs

            app    = adsk.core.Application.cast(adsk.core.Application.get())
            design = adsk.fusion.Design.cast(app.activeProduct)
            units  = design.fusionUnitsManager.defaultLengthUnits

            # Show construction planes so user can select XY/XZ/YZ
            active_component = design.activeComponent
            self._origin_state = active_component.isOriginFolderLightBulbOn
            active_component.isOriginFolderLightBulbOn = True

            plane_sel = inputs.addSelectionInput(
                'plane', 'Plane', 'Select sketch plane'
            )
            plane_sel.addSelectionFilter('PlanarFaces')
            plane_sel.addSelectionFilter('ConstructionPlanes')
            plane_sel.setSelectionLimits(1, 1)

            inputs.addValueInput('r_start', 'Inner Radius', units,
                                 adsk.core.ValueInput.createByReal(VINYL_R_START / 10))
            inputs.addValueInput('r_end', 'Outer Radius', units,
                                 adsk.core.ValueInput.createByReal(VINYL_R_END / 10))
            inputs.addIntegerSpinnerCommandInput(
                'turns', 'Turns', 1, 1000, 1, VINYL_TURNS
            )
            inputs.addIntegerSpinnerCommandInput(
                'points_per_turn', 'Points per Turn', 4, 72, 4, VINYL_PTS_PER_TURN
            )

            on_execute = _ExecuteHandler()
            cmd.execute.add(on_execute)
            _handlers.append(on_execute)

            on_destroy = _DestroyHandler(active_component, self._origin_state)
            cmd.destroy.add(on_destroy)
            _handlers.append(on_destroy)

        except Exception:
            adsk.core.Application.get().userInterface.messageBox(
                'CommandCreated failed:\n' + traceback.format_exc()
            )


class _DestroyHandler(adsk.core.CommandEventHandler):
    def __init__(self, component, origin_state):
        super().__init__()
        self._component    = component
        self._origin_state = origin_state

    def notify(self, args):
        try:
            self._component.isOriginFolderLightBulbOn = self._origin_state
        except Exception:
            pass


class _ExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            cmd    = adsk.core.Command.cast(args.firingEvent.sender)
            inputs = cmd.commandInputs

            design = adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
            plane  = _get_plane(inputs)
            sketch = design.rootComponent.sketches.add(plane)

            collection = _build_point_collection(inputs)
            sketch.sketchCurves.sketchFittedSplines.add(collection)

        except Exception:
            adsk.core.Application.get().userInterface.messageBox(
                'Execute failed:\n' + traceback.format_exc()
            )


class ArchimedeanCommand:
    def __init__(self, cmd_def, debug=False):
        self._cmd_def = cmd_def
        self._debug   = debug

    def on_run(self):
        app = adsk.core.Application.cast(adsk.core.Application.get())
        ui  = app.userInterface

        try:
            cmd_id   = self._cmd_def['cmd_id']
            existing = ui.commandDefinitions.itemById(cmd_id)
            if existing:
                existing.deleteMe()

            cmd_def = ui.commandDefinitions.addButtonDefinition(
                cmd_id,
                self._cmd_def['cmd_name'],
                self._cmd_def['cmd_description'],
            )

            on_created = _CommandCreatedHandler()
            cmd_def.commandCreated.add(on_created)
            _handlers.append(on_created)

            workspace = ui.workspaces.itemById(self._cmd_def['workspace'])
            panel     = workspace.toolbarPanels.itemById(self._cmd_def['toolbar_panel_id'])
            control   = panel.controls.addCommand(cmd_def)
            control.isVisible = True

        except Exception:
            ui.messageBox('AddIn Start Failed:\n' + traceback.format_exc())

    def on_stop(self):
        app = adsk.core.Application.cast(adsk.core.Application.get())
        ui  = app.userInterface

        try:
            workspace = ui.workspaces.itemById(self._cmd_def['workspace'])
            panel     = workspace.toolbarPanels.itemById(self._cmd_def['toolbar_panel_id'])

            control = panel.controls.itemById(self._cmd_def['cmd_id'])
            if control:
                control.deleteMe()

            cmd_def = ui.commandDefinitions.itemById(self._cmd_def['cmd_id'])
            if cmd_def:
                cmd_def.deleteMe()

            _handlers.clear()

        except Exception:
            ui.messageBox('AddIn Stop Failed:\n' + traceback.format_exc())
