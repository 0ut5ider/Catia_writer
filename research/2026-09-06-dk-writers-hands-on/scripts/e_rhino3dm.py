"""Test E: rhino3dm 8.32.2 - write .3dm with layers, mesh, names, user strings; reopen + magic."""
import pathlib
import rhino3dm as r3

OUT = pathlib.Path("/tmp/dk-writers/out")
print("rhino3dm", r3.__version__)

model = r3.File3dm()

l0 = r3.Layer(); l0.Name = "SHEETMETAL"; l0.Color = (255, 80, 80, 255)
i0 = model.Layers.Add(l0)
l1 = r3.Layer(); l1.Name = "MACHINED"; l1.Color = (80, 120, 255, 255)
i1 = model.Layers.Add(l1)
print("layer indices:", i0, i1)

def box_mesh(x0, y0, z0, x1, y1, z1):
    m = r3.Mesh()
    for p in [(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),
              (x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]:
        m.Vertices.Add(*p)
    for f in [(0,2,1,0),(5,4,7,6),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]:
        m.Faces.AddFace(*f)
    m.Normals.ComputeNormals()
    m.Compact()
    return m

attr = r3.ObjectAttributes()
attr.Name = "BASE-PLATE"
attr.LayerIndex = i0
attr.ColorSource = r3.ObjectColorSource.ColorFromObject
attr.ObjectColor = (200, 30, 30, 255)
attr.SetUserString("PART", "BRACKET-001")
guid = model.Objects.AddMesh(box_mesh(0, 0, 0, 40, 25, 6), attr)

attr2 = r3.ObjectAttributes()
attr2.Name = "RISER"
attr2.LayerIndex = i1
model.Objects.AddMesh(box_mesh(30, 0, 6, 40, 10, 26), attr2)

# B-rep primitive: rhino3dm CAN create analytic Breps
try:
    brep = r3.Brep.CreateFromBox(r3.Box(r3.BoundingBox(r3.Point3d(50, 0, 0), r3.Point3d(90, 25, 6))))
    a3 = r3.ObjectAttributes(); a3.Name = "BREP-BOX"; a3.LayerIndex = i1
    g3 = model.Objects.AddBrep(brep, a3)
    print("Brep added:", bool(g3), "| IsSolid:", brep.IsSolid(), "| faces:", len(brep.Faces))
except Exception as e:
    print("Brep.CreateFromBox failed:", type(e).__name__, e)

model.Settings.ModelUnitSystem = r3.UnitSystem.Millimeters

ok = model.Write(str(OUT / "e_model.3dm"), 7)
print("write(7):", ok, (OUT / "e_model.3dm").stat().st_size if ok else "-")

with open(OUT / "e_model.3dm", "rb") as fh:
    print("header:", fh.read(48))

m2 = r3.File3dm.Read(str(OUT / "e_model.3dm"))
print("reopen: layers", [(l.Name, l.Color) for l in m2.Layers],
      "units", m2.Settings.ModelUnitSystem)
for o in m2.Objects:
    a = o.Attributes
    try:
        us = a.GetUserStrings2()
    except Exception as e:
        us = f"ERR {e}"
    geom = o.Geometry
    extra = ""
    if isinstance(geom, r3.Mesh):
        extra = f" {len(geom.Vertices)}v/{len(geom.Faces)}f"
    elif isinstance(geom, r3.Brep):
        extra = f" {len(geom.Faces)}faces solid={geom.IsSolid}"
    print(f"  obj {a.Name!r} layer={a.LayerIndex} geom={type(geom).__name__} us={us}{extra}")
print("file user-string count:", m2.Strings.DocumentUserTextCount())
