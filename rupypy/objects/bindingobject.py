from rupypy.astcompiler import SymbolTable
from rupypy.module import ClassDef
from rupypy.objects.objectobject import W_Object


class W_BindingObject(W_Object):
    classdef = ClassDef("Binding", W_Object.classdef)

    def __init__(self, space, names, cells, w_self, w_scope):
        W_Object.__init__(self, space)
        self.names = names
        self.cells = cells
        self.w_self = w_self
        self.w_scope = w_scope

    classdef.undefine_allocator()

    @classdef.method("eval", source="str")
    def method_eval(self, space, source):
        symtable = SymbolTable()
        for name in self.names:
            symtable.cells[name] = symtable.FREEVAR
        bc = space.compile(source, "", symtable=symtable)
        frame = space.create_frame(bc, w_self=self.w_self, w_scope=self.w_scope)
        for idx, cell in enumerate(self.cells):
            frame.cells[idx + len(bc.cellvars)] = cell
        with space.getexecutioncontext().visit_frame(frame):
            return space.execute_frame(frame, bc)
