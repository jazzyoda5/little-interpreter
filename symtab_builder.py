##############################################
# Symbol Table Builder
##############################################


class Symbol(object):
    def __init__(self, name, type=None):
        self.name = name
        self.type = type


# Symbol().name will represent a builtin 
# type like 'INTEGER' or 'STRING'
class BuiltinTypeSymbol(Symbol):
    def __init__(self, name):
        super(BuiltinTypeSymbol, self).__init__(name)
    
    def __str__(self):
        return self.name

    def __repr__(self):
        return "<{class_name}(name='{name}')>".format(
            class_name=self.__class__.__name__,
            name=self.name,
        )


# For a variable Symbol().name will hold the name of 
# the variable and Symbol().type will hold an instance 
# of a BuiltinTypeSymbol() to declare which 
# type the variable is
class VarSymbol(Symbol):
    def __init__(self, name, type):
        super(VarSymbol, self).__init__(name, type)
    
    def __str__(self):
        return "<{class_name}(name='{name}', type='{type}')>".format(
            class_name=self.__class__.__name__,
            name=self.name,
            type=self.type,
        )

    __repr__ = __str__


class SymbolTable(object):
    def __init__(self):
        self._symbols = {}
        self._init_builtin_types()

    def _init_builtin_types(self):
        self.insert(BuiltinTypeSymbol('int'))
        self.insert(BuiltinTypeSymbol('float'))
        self.insert(BuiltinTypeSymbol('str'))
        self.insert(BuiltinTypeSymbol('bool'))

    # Nice way to print the contents of the symbol table
    def __str__(self):
        symtab_header = 'Symbol table contents'
        lines = ['\n', symtab_header, '_' * len(symtab_header)]
        lines.extend(
            ('%7s: %r' % (key, value))
            for key, value in self._symbols.items()
        )
        lines.append('\n')
        s = '\n'.join(lines)
        return s
    
    __repr__ = __str__

    def insert(self, symbol):
        self._symbols[symbol.name] = symbol

    def get_symbol(self, name):
        symbol = self._symbols.get(name)
        return symbol

