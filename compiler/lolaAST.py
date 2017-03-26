# --------------------------------------------------------------
# compiler: lolaAST.py
#
# AST - Abstract Syntax Tree
# This file defines the classes for the different
# types of nodes in the abstract syntax tree.
#
# --------------------------------------------------------------

# Base class for all AST nodes.
class AST(object):
	# Lists the names of stored attributes
	_fields = []

	# It takes positional arguments and assigns it to the appropriate fields
	def __init__(self, *args, **kwargs):
		assert len(args) == len(self._fields)
		for name,value in zip(self._fields,args):
			setattr(self,name,value)

		# Assign additional arguments (keywords) if supplied
		for name,value in kwargs.items():
			setattr(self,name,value)

	def __repr__(self):
		return self.__class__.__name__

	def pprint(self):
		for depth, node in flatten(self):
			print("%s%s" % (" "*(4*depth),node))


def validate_fields(**fields):
	def validator(cls):
		old_init = cls.__init__
		def __init__(self, *args, **kwargs):
			old_init(self, *args, **kwargs)
			for field,expected_type in fields.items():
				assert isinstance(getattr(self, field), expected_type)
		cls.__init__ = __init__
		return cls
	return validator

# ----------------------------------------------------------------------
# Specific AST nodes
#
# _fields = [] Indicates which fields should be stored.
#
# ----------------------------------------------------------------------



# Usted deberá añadir mas nodos aquí.  Algunos nodos sugeridos son
# BinaryOperator, UnaryOperator, ConstDeclaration, VarDeclaration,
# AssignmentStatement, etc...

# ----------------------------------------------------------------------
#                  NO MODIFIQUE NADA AQUI ABAJO
# ----------------------------------------------------------------------

# Las clase siguientes para visitar y reescribir el AST son tomadas
# desde el módulo ast de python .

# NO MODIFIQUE
class NodeVisitor(object):
	'''
	Clase para visitar nodos del árbol de sintaxis.  Se modeló a partir
	de una clase similar en la librería estándar ast.NodeVisitor.  Para
	cada nodo, el método visit(node) llama un método visit_NodeName(node)
	el cual debe ser implementado en la subclase.  El método genérico
	generic_visit() es llamado para todos los nodos donde no hay
	coincidencia con el método visit_NodeName().

	Es es un ejemplo de un visitante que examina operadores binarios:

	class VisitOps(NodeVisitor):
		visit_Binop(self,node):
			print("Operador binario", node.op)
			self.visit(node.left)
			self.visit(node.right)
		visit_Unaryop(self,node):
			print("Operador unario", node.op)
			self.visit(node.expr)

	tree = parse(txt)
	VisitOps().visit(tree)
	'''
	def visit(self,node):
		'''
		Ejecuta un método de la forma visit_NodeName(node) donde
		NodeName es el nombre de la clase de un nodo particular.
		'''
		if node:
			method = 'visit_' + node.__class__.__name__
			visitor = getattr(self, method, self.generic_visit)
			return visitor(node)
		else:
			return None

	def generic_visit(self,node):
		'''
		Método ejecutado si no se encuentra médodo aplicable visit_.
		Este examina el nodo para ver si tiene _fields, es una lista,
		o puede ser recorrido completamente.
		'''
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, AST):
						self.visit(item)
			elif isinstance(value, AST):
				self.visit(value)

# NO MODIFICAR
class NodeTransformer(NodeVisitor):
	'''
	Clase que permite que los nodos del arbol de sintaxis sean
	reemplazados/reescritos.  Esto es determinado por el valor retornado
	de varias funciones visit_().  Si el valor retornado es None, un
	nodo es borrado. Si se retorna otro valor, reemplaza el nodo
	original.

	El uso principal de esta clase es en el código que deseamos aplicar
	transformaciones al arbol de sintaxis.  Por ejemplo, ciertas
	optimizaciones del compilador o ciertas reescrituras de pasos
	anteriores a la generación de código.
	'''
	def generic_visit(self,node):
		for field in getattr(node, "_fields"):
			value = getattr(node,field, None)
			if isinstance(value, list):
				newvalues = []
				for item in value:
					if isinstance(item, AST):
						newnode = self.visit(item)
						if newnode is not None:
							newvalues.append(newnode)
					else:
						newvalues.append(n)
				value[:] = newvalues
			elif isinstance(value, AST):
				newnode = self.visit(value)
				if newnode is None:
					delattr(node, field)
				else:
					setattr(node, field, newnode)
		return node

# NO MODIFICAR
def flatten(top):
	'''
	Aplana el arbol de sintaxis dentro de una lista para efectos
	de depuración y pruebas.  Este retorna una lista de tuplas de
	la forma (depth, node) donde depth es un entero representando
	la profundidad del arból de sintaxis y node es un node AST
	asociado.
	'''
	class Flattener(NodeVisitor):
		def __init__(self):
			self.depth = 0
			self.nodes = []
		def generic_visit(self,node):
			self.nodes.append((self.depth,node))
			self.depth += 1
			NodeVisitor.generic_visit(self,node)
			self.depth -= 1

	d = Flattener()
	d.visit(top)
	return d.nodes
