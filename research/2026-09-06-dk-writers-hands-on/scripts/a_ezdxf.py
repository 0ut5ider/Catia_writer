"""Test A: ezdxf DXF + ACIS writes. ezdxf 1.4.4."""
import sys, pathlib
import ezdxf
from ezdxf.render.mesh import MeshBuilder

def box_builder(x=10, y=20, z=30):
    """Axis-aligned box (0,0,0)-(x,y,z) as MeshBuilder, quads unified CCW."""
    mb = MeshBuilder()
    v = [(0,0,0),(x,0,0),(x,y,0),(0,y,0),(0,0,z),(x,0,z),(x,y,z),(0,y,z)]
    for f in [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]:
        mb.add_face([v[i] for i in f])
    mb.optimize_vertices()
    return mb
import ezdxf.acis.api as acis_api
from ezdxf.entities import Body, Solid3d

OUT = pathlib.Path("/tmp/dk-writers/out")
OUT.mkdir(exist_ok=True)

print("ezdxf", ezdxf.__version__)
print("Body DXFTYPE:", Body.DXFTYPE, "| Solid3d DXFTYPE:", Solid3d.DXFTYPE)

# ---------- 1. DXF R2018 with rich 2D semantics ----------
doc = ezdxf.new("R2018", setup=True)
msp = doc.modelspace()

doc.layers.add("STRUCTURE", color=1)          # red
doc.layers.add("MECHANICAL", color=3)         # green
doc.layers.add("ANNOTATION", color=5)         # blue

msp.add_lwpolyline(
    [(0, 0), (40, 0), (40, 25), (0, 25)], close=True,
    dxfattribs={"layer": "STRUCTURE", "color": 6})  # magenta override

msp.add_circle((20, 12.5), 6, dxfattribs={"layer": "MECHANICAL"})
msp.add_text("HELD-OUT 0.1", dxfattribs={"layer": "ANNOTATION", "height": 2.5}).set_placement((2, 30))

# Block with ATTDEF -> INSERT with ATTRIB values
att = doc.blocks.new("TITLEBLOCK")
att.add_attdef("PART", insert=(5, 15))
att.add_attdef("REV", insert=(5, 10))
att.add_line((0, 0), (60, 0), dxfattribs={"layer": "STRUCTURE"})
ins = msp.add_blockref("TITLEBLOCK", (50, 0), dxfattribs={"layer": "ANNOTATION"})
ins.add_auto_attribs({"PART": "BRACKET-001", "REV": "C"})

# XDATA
doc.appids.add("DK_TEST")
ent = msp.add_line((0, 0), (10, 10), dxfattribs={"layer": "MECHANICAL"})
ent.set_xdata("DK_TEST", [
    (1000, "source=python"),
    (1040, 3.14),
    (1070, 42),
])

# MESH entity (3D)
mb = box_builder(10, 20, 30)
m2 = msp.add_mesh()
m2.vertices = mb.vertices
m2.faces = mb.faces
m2.dxf.layer = "MECHANICAL"
mesh_ok = True

# ---------- 2. 3DSOLID carrying ACIS body ----------
body_ok = False
mb2 = box_builder(10, 20, 30)
try:
    body = acis_api.body_from_mesh(mb2, precision=6)
    print("ACIS body:", body)
    solid = msp.add_3dsolid()
    acis_api.export_dxf(solid, [body])
    body_ok = True
except Exception as e:
    print("3DSOLID/ACIS write FAILED:", type(e).__name__, e)

dxf_path = OUT / "a_rich.dxf"
doc.saveas(dxf_path)
print("saved", dxf_path, dxf_path.stat().st_size, "bytes")

# ---------- 3. direct ACIS SAT + SAB export ----------
sat_ok = sab_ok = False
if body_ok:
    try:
        lines = acis_api.export_sat([body], version=700)
        sat_path = OUT / "a_box.sat"
        sat_path.write_text("\n".join(lines))
        sat_ok = True
        print("saved", sat_path, sat_path.stat().st_size, "bytes")
    except Exception as e:
        print("SAT export FAILED:", type(e).__name__, e)
    try:
        sab = acis_api.export_sab([body], version=21800)
        sab_path = OUT / "a_box.sab"
        sab_path.write_bytes(sab)
        sab_ok = True
        print("saved", sab_path, len(sab), "bytes")
    except Exception as e:
        print("SAB export FAILED:", type(e).__name__, e)

# ---------- 4. round-trips ----------
doc2 = ezdxf.readfile(dxf_path)
msp2 = doc2.modelspace()
counts = {}
for e in msp2:
    counts[e.dxftype()] = counts.get(e.dxftype(), 0) + 1
print("REOPEN DXF entity counts:", counts)
ins2 = [e for e in msp2 if e.dxftype() == "INSERT"][0]
print("ATTRIB values on reopen:", {a.dxf.tag: a.dxf.text for a in ins2.attribs})
ln2 = [e for e in msp2 if e.dxftype() == "LINE"][0]
xd = ln2.get_xdata("DK_TEST")
print("XDATA reopened:", [(d.code, d.value) for d in xd])

if body_ok:
    try:
        ents = acis_api.load_dxf(solid)
        print("ACIS reloaded from DXF entity:", len(ents), "body(ies)")
    except Exception as e:
        print("load_dxf FAILED:", type(e).__name__, e)
if sat_ok:
    text = sat_path.read_text()
    ents = acis_api.load(text)
    print("SAT reload:", len(ents), "body(ies)")
    for b in ents[:1]:
        ents_list = list(b.entities() if callable(b.entities) else b.entities)
        print("SAT body entity count:", len(ents_list), "types:", sorted({type(e).__name__ for e in ents_list}))

print("RESULT:", {"dxf": True, "mesh": mesh_ok, "3dsolid_acis": body_ok, "sat": sat_ok, "sab": sab_ok})
