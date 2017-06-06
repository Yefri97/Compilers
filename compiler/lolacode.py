# --------------------------------------------------------------
# compiler: lolacode.py
#
# Generate code SSA - Single Static Assignment
#
# --------------------------------------------------------------

from lolaAST import NodeVisitor
from collections import defaultdict

binary_ops = {
	'+' : 'add',
	'-' : 'sub',
	'*' : 'mul',
	'/' : 'div',
}

class GenerateCode(NodeVisitor):
	
    def __init__(self):
        super(GenerateCode, self).__init__()

        # diccionario de versiones para temporales
        self.version = 1

        # El código generado (lista de tuplas)
        self.code = []

        # Una lista de declaraciones externas (y tipos)
        self.externs = []

    def new_temp(self):
        '''
        Crea una variable temporal del tipo dado
        '''
        name = "reg_%d" % (self.version)
        self.version += 1
        return name

    def visit_Assign(self, node):
        self.visit(node.expr)

        target = node.expr.gen_location
        inst = ('store', target, node.var.id.value)
        self.code.append(inst)

        node.gen_location = target

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)

        target = self.new_temp()

        inst = (binary_ops[node.op], node.left.gen_location, node.right.gen_location, target)
        self.code.append(inst)

        node.gen_location = target

    def visit_Var(self, node):
        target = self.new_temp()

        inst = ('load', node.id.value, target)
        self.code.append(inst)

        node.gen_location = target

    def visit_Int(self, node):
        target = self.new_temp()

        inst = ('literal', node.value, target)
        self.code.append(inst)

        node.gen_location = target

    def generic_visit(self, node):
        self.visit_children(node)
