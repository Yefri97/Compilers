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

    	self.dot.set_node_defaults(shape='box', color='lightgray', style='filled')
    	self.dot.set_edge_defaults(arrowhead='none')

    def __repr__(self):
        return self.dot.to_string()

    def new_node(self, node, label=None):
    	if label is None: label = node.__class__.__name__
    	self.id += 1
    	return pgv.Node('n{}'.format(self.id), label=label)

    def generic_visit(self, node):
        curr = self.new_node(node)
        self.dot.add_node(curr)
        self.stack.append(curr)
        NodeVisitor.generic_visit(self, node)
        self.stack.pop()
        if len(self.stack):
            self.dot.add_edge(pgv.Edge(self.stack[len(self.stack)-1], curr))
