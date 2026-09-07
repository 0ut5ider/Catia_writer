"""Test D: pyiges 0.3.4 is READ-ONLY (finding: no writer API). Used as independent validator of OCC-written IGES."""
import pathlib
import pyiges
from pyiges import Iges

OUT = pathlib.Path("/tmp/dk-writers/out")

f = "b_parts.iges"
ig = Iges(str(OUT / f))
kinds = {}
for e in ig.items:
    k = getattr(e, "entity_number", None) or type(e).__name__
    kinds[k] = kinds.get(k, 0) + 1
print(f, "items:", len(ig.items), "by entity_number:", dict(sorted(kinds.items())))

try:
    m = pyiges.read_as_mesh(str(OUT / f))
    pd = m[0] if isinstance(m, tuple) else m
    print("read_as_mesh -> vtk:", type(pd).__name__, pd.GetNumberOfPoints(), "pts,",
          pd.GetNumberOfPolys(), "polys")
except Exception as e:
    print("read_as_mesh failed:", type(e).__name__, e)
