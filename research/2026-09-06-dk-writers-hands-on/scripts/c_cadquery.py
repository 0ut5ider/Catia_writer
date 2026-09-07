"""Test C: cadquery 2.8.0 + build123d - STEP export; OCP reopen (names/colors/assembly); STEP->OBJ."""
import pathlib, re
import cadquery as cq
import importlib.metadata as md

OUT = pathlib.Path("/tmp/dk-writers/out")
print("cadquery", cq.__version__, "| OCP", md.version("cadquery-ocp"))

def mcall(obj, base, *args):
    """Call method on obj trying base then base_N overloads."""
    names = [base] + sorted(n for n in dir(obj) if re.fullmatch(base + r"_\d+", n))
    last = None
    for n in names:
        f = getattr(obj, n, None)
        if f is None:
            continue
        try:
            return f(*args)
        except Exception as e:
            last = e
    raise last if last else AttributeError(base)

# ---------- part via workplane feature chain ----------
part = (
    cq.Workplane("XY")
      .box(40, 25, 6, centered=(True, True, False))
      .faces(">Z").workplane(centerOption="CenterOfBoundBox")
      .circle(4).cutBlind(-6)
      .faces(">Z").workplane(centerOption="CenterOfBoundBox", offset=0)
      .box(10, 10, 12, centered=(True, True, False))
)
cq.exporters.export(part, str(OUT / "c_part.step"))
print("part step size:", (OUT / "c_part.step").stat().st_size)

# ---------- assembly with names + colors ----------
assy = cq.Assembly(name="CQ-ASSY")
assy.add(part, name="BASE-PLATE", color=cq.Color(0.8, 0.1, 0.1, 1))
box2 = cq.Workplane("XY").box(10, 10, 20, centered=(True, True, False)).translate((30, 0, 6))
assy.add(box2, name="RISER", location=cq.Location(cq.Vector(10, 0, 0)), color=cq.Color(0.1, 0.4, 0.8, 1))
assy.save(str(OUT / "c_assy.step"), exportType="STEP")
print("assy step size:", (OUT / "c_assy.step").stat().st_size)

# ---------- build123d ----------
import build123d as b12d
print("build123d", md.version("build123d"))
with b12d.BuildPart() as bp:
    base = b12d.Box(40, 25, 6)
    with b12d.Align(CENTER, CENTER, TOP):
        b12d.Box(10, 10, 12)
    with b12d.Align(CENTER, CENTER, BOTTOM):
        b12d.Cylinder(4, 10, mode=Mode.SUBTRACT)
b12d.export_step(bp.part, str(OUT / "c_b123d.step"), unit=Unit.MM)
print("build123d step size:", (OUT / "c_b123d.step").stat().st_size)

with b12d.BuildPart() as p1:
    b12d.Box(40, 25, 6)
with b12d.BuildPart() as p2:
    b12d.Box(8, 8, 15)
ass = b12d.Assembly(name="B123-ASSY")
ass.add(p1.part, name="PLATE", color=(0.9, 0.2, 0.2, 1.0))
ass.add(p2.part, name="PIN", location=b12d.Placement((20, 0, 6)), color=(0.2, 0.4, 0.9, 1.0))
ass.export_step(str(OUT / "c_b123d_assy.step"))
print("build123d assy step size:", (OUT / "c_b123d_assy.step").stat().st_size)

# ---------- OCP reopen: names + colors + structure ----------
from OCP.TDocStd import TDocStd_Document
from OCP.XCAFApp import XCAFApp_Application
from OCP.XCAFDoc import XCAFDoc_DocumentTool
from OCP.STEPCAFControl import STEPCAFControl_Reader
from OCP.TDF import TDF_ChildIterator, TDF_LabelSequence
from OCP.TDataStd import TDataStd_Name
from OCP.Message import Message_ProgressRange

app = XCAFApp_Application.GetApplication()

def open_caf(path):
    doc = TDocStd_Document("MDTV-XCAF")
    mcall(app, "NewDocument", "MDTV-XCAF", doc)
    rd = STEPCAFControl_Reader()
    rd.SetNameMode(True); rd.SetColorMode(True)
    if not rd.ReadFile(str(path)):
        raise RuntimeError("read failed")
    mcall(rd, "Transfer", doc, Message_ProgressRange())
    return doc

def name_of(label):
    nm = TDataStd_Name()
    if mcall(label, "FindAttribute", mcall(TDataStd_Name, "GetID"), nm):
        ext = mcall(nm, "Get")
        try:
            return ext.ToCString()
        except Exception:
            return str(ext)
    return None

def walk(path):
    print("=== reopen", path.name)
    doc = open_caf(path)
    st = mcall(XCAFDoc_DocumentTool, "ShapeTool", doc.Main())
    ct = mcall(XCAFDoc_DocumentTool, "ColorTool", doc.Main())
    frees = TDF_LabelSequence()
    mcall(st, "GetFreeShapes", frees)
    def dump(label, depth=0):
        kind = "ASSY" if st.IsAssembly(label) else "SHAPE" if st.IsShape(label) else "OTHER"
        print("  " * depth + f"- {name_of(label)!r} [{kind}]")
        ci = TDF_ChildIterator(label, True)
        while ci.More():
            c = ci.Value()
            real = c
            if st.IsReference(c):
                res = mcall(st, "GetReferredShape", c)
                if isinstance(res, tuple) and res[0]:
                    real = res[1]
            nm = name_of(c) or name_of(real)
            kind2 = "REF" if st.IsReference(c) else ("ASSY" if st.IsAssembly(c) else "SHAPE")
            col = ""
            try:
                cc = mcall(ct, "GetColor", real)
                if cc is not None:
                    col = f" rgb({cc.Red():.2f},{cc.Green():.2f},{cc.Blue():.2f})"
            except Exception:
                pass
            print("  " * (depth + 1) + f"- {nm!r} [{kind2}]{col}")
            ci.Next()
    for i in range(1, frees.Length() + 1):
        dump(frees.Value(i))

for f in ["c_assy.step", "c_part.step", "c_b123d_assy.step", "b_assy.step"]:
    try:
        walk(OUT / f)
    except Exception as e:
        print("reopen FAILED for", f, type(e).__name__, e)

# ---------- STEP -> OBJ via OCP RWObj ----------
try:
    from OCP.RWObj import RWObj_CafWriter
    doc = open_caf(OUT / "c_assy.step")
    w = RWObj_CafWriter(str(OUT / "c_assy.obj"), True)
    ok = mcall(w, "Perform", doc, Message_ProgressRange())
    print("STEP->OBJ via RWObj:", ok, (OUT / "c_assy.obj").stat().st_size if ok else "-")
except Exception as e:
    print("RWObj path failed:", type(e).__name__, e)
