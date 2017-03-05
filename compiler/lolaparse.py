# --------------------------------------------------------------
# compiler: lolaparse.py
#
# Grammar analyzer of lola lenguage
#
# --------------------------------------------------------------

# import modules
from sly import Parser
from lolalex import LolaLexer

# CLASS LolaParser
class LolaParser(Parser):
    # Get the token list from the lexer (required)
    tokens = LolaLexer.tokens

    # Grammar rules and actions
    @_('INTEGER')
    def expr(self, p):
        return p.INTEGER
