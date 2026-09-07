import rhino3dm as r3, math
print("rhino3dm version:", getattr(r3, "__version__", "?"))
m = r3.File3dm()

# layers
li = m.Layers.AddLayer("TestLayer", (255, 0, 0, 255))
print("layer add ->", li)

# material table surface
mt = m.Materials
print("material table methods:", [a for a in dir(mt) if not a.startswith("_")])
mat = r3.Material()
mat.Name = "RedMetal"
mat.DiffuseColor = (200, 30, 30, 255)
try:
    print("mat add ->", mt.Add(mat))
except Exception as e:
    print("material Add FAILED:", type(e).__name__, e)

# mesh object with attributes
mesh = r3.Mesh()
for v in [(0,0,0),(1,0,0),(1,1,0),(0,1,0),(0.5,0.5,1.0)]:
    mesh.Vertices.Add(*v)
mesh.Faces.AddFace(0,1,2,3)
mesh.Faces.AddFace(0,1,4)
attrs = r3.ObjectAttributes()
attrs.LayerIndex = li
attrs.Name = "MeshObj"
attrs.Url = "https://example.com/source"
try:
    attrs.MaterialIndex = 0; attrs.MaterialSource = r3.ObjectMaterialSource.MaterialFromObject
    print("set RenderMaterialIndex ok")
except Exception as e:
    print("RenderMaterialIndex fail:", e)
ok1 = m.Objects.AddMesh(mesh, attrs)
print("AddMesh ->", ok1)

# brep object
bbox=r3.BoundingBox(r3.Point3d(0,0,0), r3.Point3d(1,1,1)); box = r3.Box(bbox)
brep = r3.Brep.CreateFromBox(box)
a2 = r3.ObjectAttributes()
a2.LayerIndex = li
a2.Name = "BrepBox"
a2.SetUserString("ParametricRecipe", "extrude:sketch1;d10")
ok2 = m.Objects.AddBrep(brep, a2)
print("AddBrep ->", ok2)

# nurbs curve
ptarray = r3.Point3dList()
for i in range(6):
    ptarray.Add(float(i), float(i*i%5), 0.0)
crv = r3.NurbsCurve.Create(False, 3, ptarray)
print("nurbs curve:", crv is not None)
if crv: print("AddCurve ->", m.Objects.AddCurve(crv))

# extrusion
poly = r3.PolylineCurve([r3.Point3d(0,0,0), r3.Point3d(2,0,0), r3.Point3d(2,2,0), r3.Point3d(0,2,0), r3.Point3d(0,0,0)])
ext = r3.Extrusion.Create(poly, 1.5, True)
print("extrusion:", ext is not None)
if ext: print("AddExtrusion ->", m.Objects.AddExtrusion(ext))

# instance definition
iid = m.InstanceDefinitions.Add("BlockA", "test block", "", "", r3.Point3d(0,0,0), (r3.Mesh(),), (r3.ObjectAttributes(),))
print("InstanceDefinitions.Add ->", iid)

# view
view = r3.ViewInfo()
view.Name = "Top"
try:
    m.Views.Add(view); print("Views.Add ok")
except Exception as e:
    print("Views.Add fail:", e)

# settings / units
try:
    m.Settings.ModelUnitSystem = r3.UnitSystem.Millimeters
    print("units set ok")
except Exception as e:
    print("units fail:", e)

# strings table
try:
    m.Strings  # check
    print("strings methods:", [a for a in dir(m.Strings) if not a.startswith("_")])
except Exception as e:
    print("strings fail:", e)

# plugin data (GH replay?)
print("plugindata methods:", [a for a in dir(m.PlugInData) if not a.startswith("_")])

# write v7
print("write ->", m.Write("/home/outsider/scratch/dkpw/test.3dm", 7))

# read back
m2 = r3.File3dm.Read("/home/outsider/scratch/dkpw/test.3dm")
print("read back objects:", len(m2.Objects))
for o in m2.Objects:
    a = o.Attributes
    print("  obj:", a.Name, "geo:", o.Geometry.ObjectType, "layer:", a.LayerIndex,
          "userstrings:", a.GetUserStrings(), "matidx:", a.MaterialIndex)
print("layers back:", [l.Name for l in m2.Layers])
print("materials back:", [mm.Name for mm in m2.Materials])
print("instances back:", len(list(m2.InstanceDefinitions)))
print("views back:", [v.Name for v in m2.Views])
