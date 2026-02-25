import adsk.core, traceback
from .ArchimedeanCommand import ArchimedeanCommand

commands = []
command_definitions = []

cmd = {
    'cmd_name':         'Archimedean Spiral',
    'cmd_description':  'Create an Archimedean spiral (default: vinyl record groove pattern)',
    'cmd_id':           'ArchimedeanSpiralCmd',
    'workspace':        'FusionSolidEnvironment',
    'toolbar_panel_id': 'SolidCreatePanel',
    'class':            ArchimedeanCommand,
}
command_definitions.append(cmd)

for cmd_def in command_definitions:
    command = cmd_def['class'](cmd_def)
    commands.append(command)


def run(context):
    try:
        for run_command in commands:
            run_command.on_run()
    except Exception:
        adsk.core.Application.get().userInterface.messageBox(
            'run() failed:\n' + traceback.format_exc()
        )


def stop(context):
    try:
        for stop_command in commands:
            stop_command.on_stop()
    except Exception:
        adsk.core.Application.get().userInterface.messageBox(
            'stop() failed:\n' + traceback.format_exc()
        )
