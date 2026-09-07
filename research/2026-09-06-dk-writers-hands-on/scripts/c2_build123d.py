"""Test C2: build123d 0.11.1 + OCP reopen + STEP->OBJ."""
import pathlib, sys
from build123d import *
import build123d as b12d
import importlib.metadata as md

OUT = pathlib.Path("/tmp/dk-writers/out")
print("build123d", md.version("build123d"), "| OCP", md.version("cadquery-ocp"))

with BuildPart() as bp:
    Box(40, 25, 6, align=(Align.MIN, Align.MIN, Align.MIN))
    with Locations((20, 12.5, 6)):
        Box(10, 10, 12, align=(Align.CENTER, Align.CENTER, Align.MIN))
    with Locations((20, 12.5, 0)):
        Cylinder(4, 10, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)
export_step(bp.part, str(OUT / "c_b123d.step"), unit=b12d.Unit.MM)
print("build123d part step size:", (OUT / "c_b123d.step").stat().st_size)

# FINDING: build123d 0.11.1 has NO Assembly class (removed upstream).
# Fallback tested here: single STEP with multiple solids via Compound (no names/colors/tree).
with BuildPart() as p1:
    Box(40, 25, 6)
with BuildPart() as p2:
    Box(8, 8, 15)
comp = Compound([p1.part, p2.part.moved(b12d.Location((20, 0, 6)))])
export_step(comp, str(OUT / "c_b123d_compound.step"), unit=b12d.Unit.MM)
print("build123d compound step size:", (OUT / "c_b123d_compound.step").stat().st_size)

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from ocp_reopen import make_walker, mcall
open_caf, walk = make_walker()
for f in ["c_b123d.step", "c_b123d_compound.step"]:
    try:
        walk(OUT / f)
    except Exception as e:
        print("reopen FAILED for", f, type(e).__name__, e)

# STEP -> OBJ via OCP RWObj
try:
    from OCP.RWObj import RWObj_CafWriter
    from OCP.Message import Message_ProgressRange
    doc = open_caf(OUT / "c_assy.step")
    w = RWObj_CafWriter(str(OUT / "c_assy.obj"), True)
    ok = mcall(w, "Perform", doc, Message_ProgressRange())
    print("STEP->OBJ via RWObj:", ok, (OUT / "c_assy.obj").stat().st_size if ok else "-")
except Exception as e:
    print("RWObj path failed:", type(e).__name__, e)
