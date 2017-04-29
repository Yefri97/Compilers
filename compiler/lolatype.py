# --------------------------------------------------------------
# compiler: lolatype.py
#
# List of types allowed
#
# --------------------------------------------------------------

# CLASS LolaType
class LolaType(object):

    def __init__(self, name, bin_ops=set(), un_ops=set()):
    	self.name = name
    	self.bin_ops = bin_ops
    	self.un_ops = un_ops

# Instances of types allowed by lola
logicvalue_type = LolaType('logicvalue',
                            set(('+', '-', '*',)),
                            set(('~')),
)

integer_type = LolaType('integer',
                            set(('+', '-', '*', '/', 'DIV', 'MOD')),
                            set(('↑')),
)
