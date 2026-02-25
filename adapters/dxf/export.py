"""
DXF export adapter for Archimedean spiral.

Usage:
    python adapters/dxf/export.py [output.dxf]

Requires: ezdxf  (pip install ezdxf)
"""
import sys
import os
import argparse

# Resolve core/ regardless of cwd
_core_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'core')
if _core_path not in sys.path:
    sys.path.insert(0, _core_path)

from spiral import SpiralParams, generate_spiral

# Mini-vinyl defaults (matches scripts/plot.py)
DEFAULT_R_START = 40
DEFAULT_R_END   = 95
DEFAULT_TURNS   = 30
DEFAULT_PTS     = 360
DEFAULT_OUTPUT  = 'spiral.dxf'


def export_dxf(params: SpiralParams, output_path: str) -> None:
    try:
        import ezdxf
    except ImportError:
        sys.exit("ezdxf not found — run: pip install ezdxf")

    points = generate_spiral(params)

    doc = ezdxf.new(dxfversion='R2010')
    msp = doc.modelspace()
    msp.add_lwpolyline(points, dxfattribs={'layer': 'SPIRAL'})

    doc.saveas(output_path)
    print(f"Saved: {output_path}  ({len(points)} points)")


def main():
    parser = argparse.ArgumentParser(description='Export Archimedean spiral to DXF')
    parser.add_argument('output',         nargs='?',      default=DEFAULT_OUTPUT,   help='Output .dxf file')
    parser.add_argument('--r-start',      type=float,     default=DEFAULT_R_START,  help='Inner radius (mm)')
    parser.add_argument('--r-end',        type=float,     default=DEFAULT_R_END,    help='Outer radius (mm)')
    parser.add_argument('--turns',        type=int,       default=DEFAULT_TURNS,    help='Number of turns')
    parser.add_argument('--pts-per-turn', type=int,       default=DEFAULT_PTS,      help='Points per turn')
    args = parser.parse_args()

    params = SpiralParams(
        r_start=args.r_start,
        r_end=args.r_end,
        turns=args.turns,
        points_per_turn=args.pts_per_turn,
    )
    export_dxf(params, args.output)


if __name__ == '__main__':
    main()
