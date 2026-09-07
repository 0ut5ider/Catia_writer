"""Shared OCP XCAF reopen helper (works on any OCP build)."""
import re

def mcall(obj, base, *args):
    names = ([base, base + "_s"]
             + sorted(n for n in dir(obj)
                      if re.fullmatch(base + r"_(s_)?\d+", n) or n == base + "_s"))
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

def make_walker():
    from OCP.TDocStd import TDocStd_Document
    from OCP.XCAFApp import XCAFApp_Application
    from OCP.XCAFDoc import XCAFDoc_DocumentTool
    from OCP.STEPCAFControl import STEPCAFControl_Reader
    from OCP.TDF import TDF_ChildIterator, TDF_LabelSequence
    from OCP.TDataStd import TDataStd_Name
    from OCP.Message import Message_ProgressRange

    app = mcall(XCAFApp_Application, "GetApplication")

    def open_caf(path):
        from OCP.TCollection import TCollection_ExtendedString
        doc = TDocStd_Document(TCollection_ExtendedString("MDTV-XCAF"))
        mcall(app, "NewDocument", TCollection_ExtendedString("MDTV-XCAF"), doc)
        rd = STEPCAFControl_Reader()
        rd.SetNameMode(True)
        rd.SetColorMode(True)
        if not rd.ReadFile(str(path)):
            raise RuntimeError("read failed")
        mcall(rd, "Transfer", doc, Message_ProgressRange())
        return doc

    def name_of(label):
        nm = TDataStd_Name()
        if mcall(label, "FindAttribute", mcall(TDataStd_Name, "GetID"), nm):
            ext = mcall(nm, "Get")
            for m in ("ToExtString", "ToCString"):
                try:
                    return getattr(ext, m)()
                except Exception:
                    pass
            return str(ext)
        return None

    def walk(path):
        print("=== reopen", path.name)
        doc = open_caf(path)
        st = mcall(XCAFDoc_DocumentTool, "ShapeTool", doc.Main())
        ct = mcall(XCAFDoc_DocumentTool, "ColorTool", doc.Main())
        frees = TDF_LabelSequence()
        mcall(st, "GetFreeShapes", frees)

        def is_a(m, lab):
            try:
                return bool(mcall(st, m, lab))
            except Exception:
                return False

        def dump(label, depth=0):
            kind = "ASSY" if is_a("IsAssembly", label) else "SHAPE" if is_a("IsShape", label) else "OTHER"
            print("  " * depth + f"- {name_of(label)!r} [{kind}]")
            ci = TDF_ChildIterator(label, True)
            while ci.More():
                c = ci.Value()
                real = c
                if is_a("IsReference", c):
                    from OCP.TDF import TDF_Label
                    out = TDF_Label()
                    try:
                        if mcall(st, "GetReferredShape", c, out):
                            real = out
                    except Exception:
                        pass
                nm = name_of(c) or name_of(real)
                kind2 = "REF" if is_a("IsReference", c) else ("ASSY" if is_a("IsAssembly", c) else "SHAPE")
                col = ""
                try:
                    from OCP.Quantity import Quantity_Color
                    from OCP.XCAFDoc import XCAFDoc_ColorGen
                    q = Quantity_Color()
                    res = mcall(ct, "GetColor", real, q, XCAFDoc_ColorGen)
                    ok = res[0] if isinstance(res, tuple) else bool(res)
                    if ok:
                        col = f" rgb({q.Red():.2f},{q.Green():.2f},{q.Blue():.2f})"
                except Exception:
                    pass
                print("  " * (depth + 1) + f"- {nm!r} [{kind2}]{col}")
                ci.Next()

        for i in range(1, frees.Length() + 1):
            dump(frees.Value(i))

    return open_caf, walk
