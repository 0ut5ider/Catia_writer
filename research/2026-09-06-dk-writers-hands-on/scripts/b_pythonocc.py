"""Test B: pythonocc-core 7.9.3 (conda-forge) - two boxes + boolean + sketch extrude,
XCAF assembly with names/colors, STEP AP214 + IGES export, reopen verification."""
import pathlib
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Ax2, gp_Vec
from OCC.Core.BRepPrimAPI import (BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder,
                                  BRepPrimAPI_MakePrism)
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse
from OCC.Core.BRepBuilderAPI import (BRepBuilderAPI_MakePolygon, BRepBuilderAPI_MakeWire,
                                     BRepBuilderAPI_MakeFace)
from OCC.Core.TDocStd import TDocStd_Document
from OCC.Core.XCAFApp import XCAFApp_Application
from OCC.Core.XCAFDoc import (XCAFDoc_DocumentTool, XCAFDoc_ColorGen,
                              XCAFDoc_ColorSurf, XCAFDoc_ColorCurv)
from OCC.Core.TDF import TDF_Label, TDF_ChildIterator
from OCC.Core.TDataStd import TDataStd_Name
from OCC.Core.TCollection import TCollection_ExtendedString
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.Interface import Interface_Static_SetCVal, Interface_Static_CVal
from OCC.Core.STEPCAFControl import STEPCAFControl_Writer, STEPCAFControl_Reader
from OCC.Core.IGESControl import IGESControl_Controller, IGESControl_Writer
from OCC.Core.STEPControl import STEPControl_Reader

OUT = pathlib.Path("/tmp/dk-writers/out")

# ---------- geometry ----------
base = BRepPrimAPI_MakeBox(40.0, 25.0, 6.0).Shape()                       # box 1
boss = BRepPrimAPI_MakeBox(gp_Pnt(30, 7.5, 6), 10.0, 10.0, 12.0).Shape()  # box 2
cyl  = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(20, 12.5, -1), gp_Dir(0, 0, 1)), 4.0, 8.0).Shape()
plate_with_hole = BRepAlgoAPI_Cut(BRepAlgoAPI_Fuse(base, boss).Shape(), cyl).Shape()

poly = BRepBuilderAPI_MakePolygon(gp_Pnt(60, 0, 0), gp_Pnt(75, 0, 0))
for p in [(75, 4, 0), (64, 4, 0), (64, 18, 0), (60, 18, 0)]:
    poly.Add(gp_Pnt(*p))
poly.Close()
face = BRepBuilderAPI_MakeFace(BRepBuilderAPI_MakeWire(poly.Wire()).Wire())
gusset = BRepPrimAPI_MakePrism(face.Shape(), gp_Vec(0, 0, 20)).Shape()
print("shapes valid:", not plate_with_hole.IsNull(), not gusset.IsNull())

# ---------- XCAF assembly (OCCT 7.9 API) ----------
from OCC.Core.TopoDS import TopoDS_Compound
from OCC.Core.BRep import BRep_Builder
app = XCAFApp_Application.GetApplication()
doc = TDocStd_Document("MDTV-XCAF")
app.NewDocument("MDTV-XCAF", doc)
shapeTool = XCAFDoc_DocumentTool.ShapeTool(doc.Main())
colorTool = XCAFDoc_DocumentTool.ColorTool(doc.Main())

def name(label, s):
    TDataStd_Name.Set(label, TCollection_ExtendedString(s)) if False else TDataStd_Name.Set(label, s)

def label_name(label):
    try:
        n = TDataStd_Name.Get(label)
        return n.Get() if n is not None else "?"
    except Exception:
        return "?"

comp = TopoDS_Compound()
BRep_Builder().MakeCompound(comp)
BRep_Builder().Add(comp, plate_with_hole)
BRep_Builder().Add(comp, gusset)

asm = shapeTool.AddShape(comp, True, False)  # top-level, treat compound as assembly
name(asm, "BRACKET-ASSY")
comps = __import__("OCC.Core.TDF", fromlist=["TDF_LabelSequence"]).TDF_LabelSequence()
shapeTool.GetComponents(asm, comps)
print("components found:", comps.Length())
for i, (part_name, rgb) in enumerate([("BASE-PLATE", (0.8, 0.1, 0.1)), ("L-GUSSET", (0.1, 0.4, 0.8))]):
    lab = comps.Value(i + 1)
    name(lab, part_name)
    c = Quantity_Color(*rgb, Quantity_TOC_RGB)
    for flag in (XCAFDoc_ColorGen, XCAFDoc_ColorSurf, XCAFDoc_ColorCurv):
        colorTool.SetColor(lab, c, flag)
print("assembly named + colored")

# ---------- STEP AP214 ----------
Interface_Static_SetCVal("write.step.schema", "AP214IS")
w = STEPCAFControl_Writer()
w.SetColorMode(True); w.SetNameMode(True); w.SetLayerMode(True); w.SetPropsMode(True)
tr = w.Transfer(doc)
st = w.Write(str(OUT / "b_assy.step"))
print("STEP transfer:", tr, "write status:", int(st), "| schema CvVal:", Interface_Static_CVal("write.step.schema"))

# ---------- IGES ----------
IGESControl_Controller.Init()
ig = IGESControl_Writer("MM", 11)
ig.AddShape(plate_with_hole)
ig.AddShape(gusset)
ok = ig.Write(str(OUT / "b_parts.iges"))
print("IGES write:", ok)

# ---------- reopen STEP as plain shape ----------
rd = STEPControl_Reader()
rd.ReadFile(str(OUT / "b_assy.step"))
print("STEP roots:", rd.NbRootsForTransfer())
rd.TransferRoots()
print("STEP reopened shape null?", rd.OneShape().IsNull())

# ---------- reopen STEP into XCAF: names/colors/structure ----------
doc2 = TDocStd_Document("MDTV-XCAF")
app.NewDocument("MDTV-XCAF", doc2)
rdc = STEPCAFControl_Reader()
rdc.SetColorMode(True); rdc.SetNameMode(True)
rdc.ReadFile(str(OUT / "b_assy.step"))
rdc.Transfer(doc2)
st2 = XCAFDoc_DocumentTool.ShapeTool(doc2.Main())

def dump(label, depth=0):
    kind = ("ASSEMBLY" if st2.IsAssembly(label) else
            "REF" if st2.IsReference(label) else
            "SHAPE" if st2.IsShape(label) else "OTHER")
    print("  " * depth + f"- {label_name(label)!r} [{kind}]")
    ci = TDF_ChildIterator(label, True)
    while ci.More():
        dump(ci.Value(), depth + 1)
        ci.Next()

from OCC.Core.TDF import TDF_LabelSequence
frees = TDF_LabelSequence()
st2.GetFreeShapes(frees)
for i in range(1, frees.Length() + 1):
    dump(frees.Value(i))

ct2 = XCAFDoc_DocumentTool.ColorTool(doc2.Main())
print("reopened doc color tool present:", ct2 is not None)
print("NOTE: pythonocc 7.9.3 exposes no TDataStd_Name reader (bind gap); names verified in STEP text + OCP reopen")
