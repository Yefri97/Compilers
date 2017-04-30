# --------------------------------------------------------------
# compiler: lolacheck.py
#
# Check the program
#
# --------------------------------------------------------------

from lolaAST import NodeVisitor
import lolatype

# CLASS SymbolTable
class SymbolTable(object):

  class SymbolDefinedError(Exception):
    # Symbol already defined
    pass

  class SymbolConflictError(Exception):
    # Symbol already defined and the type is different
    pass

  def __init__(self, parent=None):
    # Create a symbol table empty with the given parent table
    self.symtab = {}
    self.parent = parent
    if self.parent != None:
      self.parent.children.append(self)
    self.children = []

  def add(self, a, v):
    # Add a symbol with the value given to the symbol table
    if a in self.symtab:
      if self.symtab[a].type.get_string() != v.type.get_string():
        raise SymbolTable.SymbolConflictError()
      else:
        raise SymbolTable.SymbolDefinedError()
    self.symtab[a] = v

  def lookup(self, a):
    # Find a symbol with the value given in the symbol table
    if a in self.symtab:
      return self.symtab[a]
    else:
      if self.parent != None:
        return self.parent.lookup(a)
      else:
        return None

# CLASS CheckProgramVisitor
class CheckProgramVisitor(NodeVisitor):

    def __init__(self):
      # Init the symbol table
        self.curr = None

    def push_symtab(self):
        self.curr = SymbolTable(self.curr)

    def pop_symtab(self):
        self.curr = self.curr.parent

    def visit_Module(self, node):
        if node.id0.value != node.id1.value:
            print ("Linea",node.line,"Error en la declaración del modulo")

        self.push_symtab()

        self.curr.add('integer', lolatype.integer_type)
        self.curr.add('logicvalue', lolatype.logicvalue_type)

        self.visit_children(node)

        self.pop_symtab()

    def visit_TypeDec(self, node):
        if node.id0.value != node.id1.value:
            print ("Linea",node.line,"Error en la declaración del tipo")

        if self.curr.lookup(node.id0.value):
            print ("Linea",node.line,"Tipo %s ya definido" % node.id0.value)
        elif self.curr.lookup(node.id1.value):
            print ("Linea",node.line,"Tipo %s ya definido" % node.id1.value)
        else:
            self.push_symtab()

            self.visit_children(node)
            module = self.curr.parent
            module.add(node.id0.value, self.curr)

            self.pop_symtab()

    def visit_ConstDec(self, node):
        if self.curr.lookup(node.id.value):
            print ("Linea",node.line,"Símbolo %s ya definido" % node.id.value)
            exit()
        self.visit(node.expr)
        if node.expr.type.name != 'integer':
            print ("Linea",node.line,"Constante debe ser de tipo entero")
        node.id.type = self.curr.lookup('integer')
        self.curr.add(node.id.value, node.id)

    def visit_VarsDec(self, node):
        typeName = node.type.simpleType
        for var in node.idList.list:
            if self.curr.lookup(var.value):
                print ("Linea",node.line,"Símbolo %s ya definido" % var.value)
            elif typeName == 'BIT' or typeName == 'TS' or typeName == 'OC':
                var.type = self.curr.lookup('logicvalue')
                self.curr.add(var.value, var)
            elif self.curr.lookup(typeName):
                var.type = self.curr.lookup(typeName)
                self.curr.add(var.value, var)
            else:
                print("Tipo %s no declarado" % typeName)

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)
        if node.left.type.name != node.right.type.name:
            print("Error en la operación: diferencia de tipos")
        node.type = node.left.type
        if not node.op in node.type.bin_ops:
            print("Error en la operación: operador '%s' no soportado" % node.op)

    def visit_Boolean(self, node):
        node.type = self.curr.lookup('logicvalue')

    def visit_Int(self, node):
        node.type = self.curr.lookup('integer')

    def visit_Var(self, node):
        if not self.curr.lookup(node.id.value):
            print("Variable %s asignado a un sym desconocido" % node.id.value)
            exit()
            #raise SymbolTable.SymbolConflictError("Variable '%s' asignado a un sym desconocido" % node.id.value)
        else:
            identifier = self.curr.lookup(node.id.value)
            node.type = identifier.type

    def visit_For(self, node):
        self.push_symtab()

        self.visit_children(node)

        if self.curr.lookup(node.id.value):
            print("Linea",node.line,"Símbolo %s ya definido" % node.id.value)
        else:
            node.id.type = self.curr.lookup('integer')
            self.curr.add(node.id.value, node.id)

        self.visit(node.expr0)
        self.visit(node.expr1)
        if node.expr0.type.name != 'integer' or node.expr1.type.name != 'integer':
            print("Linea",node.line,"Error en el FOR: Limites deben ser de tipo entero")

        self.pop_symtab()

    def visit_Assign(self, node):
        self.visit(node.var)
        self.visit(node.expr)
        if isinstance(node.var.type, lolatype.LolaType) and isinstance(node.expr.type, lolatype.LolaType):
            if node.var.type.name != node.expr.type.name:
                print("Linea",node.line,"Error en la asignación")

    def generic_visit(self, node):
        self.visit_children(node)
