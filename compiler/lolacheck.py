# --------------------------------------------------------------
# compiler: lolacheck.py
#
# Check the program
#
# --------------------------------------------------------------

from lolaAST import NodeVisitor

# CLASS SymbolTable
class SymbolTable(object):

  class SymbolDefinedError(Exception):
    # Symbol already defined
    pass

  class SymbolConflictError(Exception):
    # Symbol already defined and the type is different
    pass

  def __init__(self, name, parent):
    # Create a symbol table empty with the given parent table
    self.symtab = {}
    self.parent = parent
    if self.parent != None:
      self.parent.children[name] = self;
    self.children = {}

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

    def push_symtab(self, name):
        self.curr = SymbolTable(name, self.curr)

    def pop_symtab(self):
        self.curr = self.curr.parent

    def visit_Module(self, node):
        if node.id0.value != node.id1.value:
            print("Error en la declaración del modulo")

        self.push_symtab('module')

        self.visit_children(node)

        self.pop_symtab()

    def visit_TypeDec(self, node):
        if node.id0.value != node.id1.value:
            print("Error en la declaración del tipo")

        self.push_symtab(node.id0.value)

        self.visit_children(node)

        module = self.curr.parent
        module.add(node.id0.value, self.curr)

        self.pop_symtab()

    def visit_ConstDec(self, node):
        if self.curr.lookup(node.id.value):
            print("Símbolo %s ya definido" % node.id.value)
        else:
            self.curr.add(node.id.value, node.id)

    def visit_VarsDec(self, node):
        for var in node.idList.list:
            if self.curr.lookup(var.value):
                print("Símbolo %s ya definido" % var.value)
            else:
                var.type = self.curr.lookup(node.type.simpleType)
                self.curr.add(var.value, var)

        if not self.curr.lookup(node.type.simpleType):
            print("Tipo %s no declarado" % node.type.simpleType)
    #
    # def visit_BinaryOp(self, node):
	# 	self.visit(node.left)
	# 	self.visit(node.right)
	# 	if node.left.type != node.right.type:
	# 		error
	# 	node.type = node.left.type
	# 	if not node.op in node.type.bin_ops:
	# 		error
    #
    # def visit_For(self, node):
    #     self.push_symtab()
    #
    #     if self.symtab.lookup(node.id.value):
    #         print("Símbolo %s ya definido" % node.id.value)
    #     else:
    #         self.symtab.add(node.id.value, node.id)
    #
    #     self.visit_children(node)
    #
    #     self.pop_symtab()
    #
    # def visit_Var(self, node):
    #     if not self.symtab.lookup(node.id.value):
    #         print("Variable %s asignado a un sym desconocido" % node.id.value)

    def generic_visit(self, node):
        self.visit_children(node)
