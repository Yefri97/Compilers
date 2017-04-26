# Lola - Dibujar AST + graphviz

import pydotplus as pgv
from lolaAST import NodeVisitor

class DotCode(NodeVisitor):
    def __init__(self):
        super(DotCode, self).__init__()

        # Secuencia para los nombres de nodos
        self.id = 0

        # Stack para retornar nodos procesados
        self.stack = []

        # Inicializacion del grafo para Dot
        self.dot = pgv.Dot('AST', graph_type='digraph')

        self.dot.set_edge_defaults(arrowhead='empty')

    def __repr__(self):
        return self.dot.to_string()

    def new_node(self, node, shape, color, style, label=None):
    	if label is None: label = node.__class__.__name__
    	self.id += 1
    	return pgv.Node('n{}'.format(self.id), label=label, shape=shape, color=color, style=style)

    def push_node(self, curr, node):
        self.dot.add_node(curr)
        self.stack.append(curr)
        self.visit_children(node)
        self.stack.pop()
        if len(self.stack):
            self.dot.add_edge(pgv.Edge(self.stack[len(self.stack)-1], curr))

    def visit_Module(self, node):
        curr = self.new_node(node, 'box', 'blue', 'filled')
        self.push_node(curr, node)

    def visit_TypeDec(self, node):
        curr = self.new_node(node, 'box', 'blue', 'filled')
        self.push_node(curr, node)

    def visit_ConstDec(self, node):
        curr = self.new_node(node, 'circle', 'green', 'filled')
        self.push_node(curr, node)

    def visit_VarsDec(self, node):
        curr = self.new_node(node, 'circle', 'green', 'filled')
        self.push_node(curr, node)

    def visit_Id(self, node):
        curr = self.new_node(node, 'box', 'lightgray', 'dash', 'value={}'.format(node.value))
        self.push_node(curr, node)

    def visit_For(self, node):
        curr = self.new_node(node, 'circle', 'green', 'filled')
        self.push_node(curr, node)

    def visit_Var(self, node):
        curr = self.new_node(node, 'diamond', 'red', 'filled')
        self.push_node(curr, node)

    def visit_Empty(self, node):
        pass

    def generic_visit(self, node):
        curr = self.new_node(node, 'box', 'lightgray', 'dash')
        self.push_node(curr, node)
