#!/usr/bin/env python3

from datetime import datetime
import sys
import xml.etree.ElementTree
import argparse
import sympy
from sympy.functions.elementary.miscellaneous import Max
import math
import re
import collections
import operator
from functools import cmp_to_key
from functools import reduce

class Registers( object ):
    def __init__( self, name, label, prefix, description, skip_index,
            skip_access, skip_reset, depth, licenses ):
        self.name = name
        self.label = label
        self.prefix = prefix or ""
        self.description = description
        self.skip_index = skip_index
        self.skip_access = skip_access
        self.skip_reset = skip_reset
        self.depth = depth
        self.licenses = licenses
        self.registers = []

    def add_register( self, register ):
        self.registers.append( register )
        register.registers = self

def sympy_compare_lowBit( a, b ):
    if sympy.simplify("(%s) > (%s)" % ( a.lowBit, b.lowBit )) == True:
        return 1
    if sympy.simplify("(%s) < (%s)" % ( a.lowBit, b.lowBit )) == True:
        return -1
    return 0

class Register( object ):
    def __init__( self, name, short, description, address, sdesc, define ):
        self.name = name
        self.short = short
        self.description = description
        self.address = address
        self.sdesc = sdesc
        self.define = define
        # Allow user to override our auto-generated register diagram.
        self.diagram = None
        self.fields = []

        self.label = ( short or name ).lower() # TODO: replace spaces etc.

    def add_field( self, field ):
        self.fields.append( field )
        self.fields.sort( key=cmp_to_key(sympy_compare_lowBit), reverse=True )
        field.register = self

    def check( self ):
        previous = None
        for f in self.fields:
            if not previous is None:
                expression = "(%s) > (%s)" % ( previous, f.highBit )
                result = sympy.simplify( expression )
                if type( result ) == bool:
                    assert result, "%s in %s of %s" % ( expression, f, self )

                expression = "(%s) - (%s)" % ( previous, f.highBit )
                delta = sympy.simplify( expression )
                try:
                    delta = int( delta )
                    assert delta == 1, \
                            "%s doesn't have all bits defined above %s (%s)" % ( self, f, expression )
                except TypeError:
                    pass
            previous = f.lowBit
        assert previous is None or int( previous ) == 0, \
                "%s isn't defined down to 0 (%r)" % ( self, previous )

    def width( self ):
        if self.fields:
            return Max(*(f.highBit for f in self.fields)) + 1
        else:
            return 0

    def __str__( self ):
        return self.name

    def symbols( self ):
        return reduce(operator._or, map(lambda f: f.symbols(), self.fields))

    def to_c_filter( self ):
        return self.define and not self.address is None

    def address_define_name( self ):
        return self.registers.prefix + toCIdentifier( self.short or self.label ).upper()

    def ordinal_name( self ):
        return self.address_define_name() + "_ORDINAL"

    def sorted_fields( self ):
        return sorted(filter(lambda f: f.to_c_filter(), self.fields), key=lambda f: f.lowBit)

    @staticmethod
    def c_field_list_type():
        return ("typedef struct riscv_debug_reg_field_list_t {\n" +
                "\triscv_debug_reg_field_info_t field;\n" +
                "\tstruct riscv_debug_reg_field_list_t (*get_next)(riscv_debug_reg_ctx_t context);\n" +
                "} riscv_debug_reg_field_list_t;\n")
    def c_field_getter_names(self):
        fields = list(self.sorted_fields())
        if not len(fields):
            return ["NULL"]
        return (f"{self.address_define_name().lower()}_get_{toCIdentifier(f.name).lower()}" for f in fields)

    def c_field_getters(self, to_c, is_valid):
        field_getters = list(self.c_field_getter_names())
        assert len(field_getters)

        def getter(f, getter_name, next_getter_name):
            syms = f.symbols()
            all_valid = ' && '.join(map(is_valid, syms))
            field = f.c_info(to_c).replace('\n', '\n\t\t')
            return (f"static riscv_debug_reg_field_list_t {getter_name}(riscv_debug_reg_ctx_t context)\n" +
                    "{\n\t" +
                    add_indent((f"assert({all_valid});\n" if syms else "") +
                               f"riscv_debug_reg_field_list_t result = {{\n" +
                               f"\t.field = {{\n\t\t{field}\n\t}},\n" +
                               f"\t.get_next = {next_getter_name}\n" +
                               "};\n" +
                               "return result;") +
                    "\n}\n")
        return "\n".join(reversed(list(
            getter(f, n, next_n) for f, n, next_n in zip(
                self.sorted_fields(),
                field_getters,
                field_getters[1:] + ["NULL"]
                )
            )))

    @staticmethod
    def c_info_type():
        return ("typedef struct {\n" +
                "\tconst char *name;\n"
                "\tstruct riscv_debug_reg_field_list_t (* const get_fields_head)(riscv_debug_reg_ctx_t context);\n" +
                "} riscv_debug_reg_info_t;\n")

    def c_info( self, to_c ):
        return (f'.name = "{self.short or self.label}",\n' +
                f'.get_fields_head = {list(self.c_field_getter_names())[0]}')

class Value( object ):
    def __init__( self, element ):
        self.value = element.get( 'v' )
        self.range = element.get( 'range' )
        if self.range:
            self.low, self.high = self.range.split( ":" )
        self.text = (element.text or "").strip()
        self.tail = element.tail.strip()
        self.name = element.get( "name" )
        self.duplicate = element.get( "duplicate" )

    def to_latex( self ):
        if not self.text:
            return ""
        result = []
        if self.range:
            result.append("%s--%s (%s): %s\n" % ( self.low, self.high, self.name, self.text ))
        else:
            result.append("%s (%s): %s\n" % ( self.value, self.name, self.text ))
        if self.tail:
            result.append( self.tail )
        return "\n".join( result )

    def to_c_definitions( self, prefix ):
        result = []
        name = "%s_%s" % ( prefix, toCIdentifier( self.name.upper() ))
        result.append(( "comment", "%s: %s" % ( self.name, self.text )))
        if self.range:
            result.append(( "%s_LOW" % name, self.low ))
            result.append(( "%s_HIGH" % name, self.high ))
        else:
            result.append(( name, self.value ))
        if self.tail:
            result.append(( "comment", self.tail ))
        return result

class Field( object ):
    def __init__( self, name, lowBit, highBit, reset, access, description,
            sdesc, define, values ):
        self.name = name
        self.lowBit = lowBit
        self.highBit = highBit
        self.reset = reset
        self.access = access
        self.description = description
        self.define = define
        self.values = values

        name_counts = collections.Counter( v.name for v in values if not v.duplicate )
        assert all( v == 1 for v in name_counts.values() ), \
            "Duplicate field name in field %s" % self.name

        value_counts = collections.Counter( v.value for v in values if not v.duplicate )
        assert all( v == 1 for v in value_counts.values() ), \
            "Duplicate field value in field %s" % self.name

    def length( self ):
        return sympy.simplify( "1 + (%s) - (%s)" % ( self.highBit, self.lowBit ) )

    def symbols( self ):
        return sympy.simplify(self.lowBit).atoms(sympy.Symbol) | sympy.simplify(self.highBit).atoms(sympy.Symbol)

    def columnWidth( self ):
        """Return the width of the column in boxes."""
        offsetCharWidth = .26
        nameCharWidth = .33
        xlen_symbol = sympy.symbols('XLEN')
        lengthCharWidth = .22
        try:
            # Pretend XLEN=32. This makes 32-bit registers with just a single
            # field be wide, while registers with XLEN-32 width be narrow.
            length = int(self.length().subs(xlen_symbol, 32))
        except TypeError:
            length = 20
        if self.length() == 1:
            bitText = f"{self.lowBit}"
        else:
            # There is no dash in what we're displaying, but we want some space
            # for separation between the two values.
            bitText = f"{self.highBit} - {self.lowBit}"
        width = math.ceil(max(
            # Minimum length
            1,
            # Make fields with more bits take up more space visually
            1 + math.log(max(length, 0.1), 1.7),
            # Wide enough to accommodate the string showing the field length
            len( str( self.length() )) * lengthCharWidth,
            # Wide enough to accommodate the high/low bit strings
            len( bitText ) * offsetCharWidth,
            # Wide enough to accommodate the name of the field
            len( self.name ) * nameCharWidth))
        # Make longer widths odd, so we can center the bit.
        if width > 1 and width % 2 == 0:
            width += 1
        return width

    def latex_description(self):
        result = [self.description]
        for value in self.values:
            text = value.to_latex()
            if text:
                result.append(text)
        return "\n\n".join(result)

    def __str__( self ):
        return self.name

    def mask(self):
        return ((2 ** sympy.simplify(self.length())) - 1) * (2 ** sympy.simplify(self.lowBit))

    def to_c_filter(self):
        return self.define

    def mask_define_name(self):
        return f"{self.register.address_define_name()}_{toCIdentifier( self.name ).upper()}"

    def c_values_array_name(self):
        return f"{self.mask_define_name().lower()}_values" if len(self.values) else "NULL"

    def c_values_array_def(self):
        assert len(self.values)

        # Remove whitespace from the names, so when they're displayed we can use
        # only ' ' as a separator.
        arr_elem_def = (f'[{v.value}] = "{toCIdentifier(v.name)}"'
                        for v in self.values if v.value is not None)

        #WA for *lo & *hi splitted fields
        if len(self.values) > 2**self.length():
            return f"static const char *{self.c_values_array_name()}[{2**self.length()}] = {{}};"
        return f"static const char *{self.c_values_array_name()}[{2**self.length()}] = {{\n\t" + ",\n\t".join(arr_elem_def) + "\n};"

    def offset_define_name(self):
        return self.mask_define_name() + "_OFFSET"

    @staticmethod
    def c_info_type():
        return ("typedef struct {\n" +
                "\tconst char *name;\n" +
                "\tunsigned int lsb; // inclusive\n" +
                "\tunsigned int msb; // inclusive\n" +
                "\tconst char **values; // If non-NULL, array of human-readable string for each possible value\n" +
                "} riscv_debug_reg_field_info_t;\n")

    def c_info( self, to_c ):
        return f'.name = "{self.name}",\n.lsb = {to_c(self.lowBit)},\n.msb = {to_c(self.highBit)},\n.values = {self.c_values_array_name()}'

def parse_bits( field ):
    """Return high, low (inclusive)."""
    text = field.get( 'bits' )
    parts = text.split( ':' )
    if len( parts ) == 1:
        return parts * 2
    elif len( parts ) == 2:
        return parts
    else:
        assert False, text

def parse_spdx( path ):
    with open( path ) as f:
        data = f.read(4096)
        return set(re.findall(r"SPDX-License-Identifier:\s*(.+?)\s*(?:-->.*)?$", data, re.MULTILINE))

def parse_xml( path ):
    licenses = parse_spdx(path)
    e = xml.etree.ElementTree.parse( path ).getroot()
    if e.text:
        description = e.text.strip()
    else:
        description = ""
    registers = Registers( e.get( 'name' ), e.get( 'label' ),
            e.get( 'prefix' ), description,
            int( e.get( 'skip_index', 0 ) ),
            int( e.get( 'skip_access', 0 ) ),
            int( e.get( 'skip_reset', 0 ) ),
            int( e.get( 'depth', 1 )),
            licenses)
    for r in e.findall( 'register' ):
        name = r.get( 'name' )
        short = r.get( 'short' )
        if r.text:
            description = r.text.strip()
        else:
            description = ""
        register = Register( name, short, description,
                r.get( 'address' ), r.get( 'sdesc' ),
                int( r.get( 'define', '1' ) ) )

        fields = r.findall( 'field' )
        for f in fields:
            highBit, lowBit = parse_bits( f )
            if f.text:
                description = f.text.strip()
            else:
                description = ""
            if f.get( 'name' ) == '0':
                define = int( f.get( 'define', '0' ) )
            else:
                define = int( f.get( 'define', '1' ) )
            values = [ Value( v ) for v in f.findall( 'value' ) ]
            field = Field( f.get( 'name' ), lowBit, highBit, f.get( 'reset' ),
                    f.get( 'access' ), description, f.get( 'sdesc' ),
                    define, values )
            register.add_field( field )

        for diagram in r.findall( 'diagram' ):
            register.diagram = diagram.text.strip()

        register.check()
        registers.add_register( register )
    return registers

def toLatexIdentifier( *args ):
    replacements = (
            ( '/', '' ),
            ( '\\_', '' ),
            ( ' ', '' ),
            ( '-', '' ),
            ( '_', '' ),
            ( '(', '' ),
            ( ')', '' ),
            ( '64', 'Sixtyfour' ),
            ( '32', 'Thirtytwo' ),
            ( '28', 'Twentyeight' ),
            ( '16', 'Sixteen' ),
            ( '15', 'Fifteen' ),
            ( '11', 'Eleven' ),
            ( '9', 'Nine' ),
            ( '8', 'Eight' ),
            ( '7', 'Seven' ),
            ( '6', 'Six' ),
            ( '5', 'Five' ),
            ( '4', 'Four' ),
            ( '3', 'Three' ),
            ( '2', 'Two' ),
            ( '1', 'One' ),
            ( '0', 'Zero' )
            )
    text = ""
    for arg in args:
        arg = (arg or "").lower()
        for frm, to in replacements:
            arg = arg.replace( frm, to )
        if arg and text:
            arg = arg[0].upper() + arg[1:]
        text += arg
    return text

def toAdocIdentifier( *args ):
    text = "-".join(
        filter(
            lambda a: a,
            [(a or "")
                .lower()
                .rstrip("_")
                .rstrip(")")
                .replace("(", "_")
                for a in args]
        ))
    text = re.sub( "\s+", "", text )
    return text

def toCIdentifier( text ):
    return re.sub( "[^\w]", "_", text )

def write_definitions( fd, registers ):
    for r in registers.registers:
        regid = r.short or r.label
        if r.define:
            macroName = toLatexIdentifier( registers.prefix, regid )
            fd.write( "\\defregname{\\R%s}{\\hyperref[%s]{%s}}\n" % (
                macroName, toLatexIdentifier( registers.prefix, r.label ), r.short or r.label ) )
        for f in r.fields:
            if f.define:
                fd.write( "\\deffieldname{\\F%s}{\\hyperref[%s]{%s}}\n" % (
                        toLatexIdentifier( registers.prefix, regid, f.name ),
                        toLatexIdentifier( registers.prefix, regid, f.name ),
                        f.name ) )

def write_adoc_definitions( fd, registers ):
    for r in registers.registers:
        regid = r.short or r.label
        if r.define:
            macroName = toAdocIdentifier( registers.prefix, regid )
            if r.fields or r.description:
                fd.write( f":{macroName}: <<{macroName},{r.short or r.label}>>\n" )
            else:
                fd.write( f":{macroName}: {r.short or r.label}\n" )
        for f in r.fields:
            if f.define:
                macroName = toAdocIdentifier( regid, f.name )
                fd.write( f":{macroName}: <<{macroName},{f.name}>>\n" )

class Macro:
    def __init__(self, name, expressionText):
        self.name = name
        self.expression = sympy.simplify(expressionText)
        self.atoms = self.expression.atoms(sympy.Symbol)

    def prototype(self):
        if self.atoms:
            return "%s(%s)" % (self.name, ", ".join(str(a) for a in self.atoms))
        else:
            return self.name

    def body(self):
        return self.expression

def sympy_to_c(expression, sym_to_c = lambda s: f"({s})", unsigned=True):
    """Implement our own string function, so we can replace 2** with 1<<."""
    stc = lambda x : sympy_to_c(x, sym_to_c, unsigned)
    if isinstance(expression, str):
        return expression
    if isinstance(expression, sympy.Number):
        suffix = "ULL" if unsigned else ""
        if (expression < 10 and expression > -10):
            return "%d%s" % (expression, suffix)
        else:
            return "%#0x%s" % (expression, suffix)
    elif isinstance(expression, sympy.Symbol):
        return sym_to_c(expression)
    elif isinstance(expression, sympy.Add):
        return "(" + " + ".join(stc(t) for t in reversed(expression.args)) + ")"
    elif isinstance(expression, sympy.Mul):
        return "(" + " * ".join(stc(t) for t in expression.args) + ")"
    elif isinstance(expression, sympy.Pow):
        base, exponent = expression.as_base_exp()
        assert base == 2, "Power must have base of two, not %r" % base
        return "(1ULL << %s)" % stc(exponent)
    elif isinstance(expression, Max):
        args = list(map(stc, expression.args))
        def c_max(args):
            if len(args) == 1:
                return args[0]
            if len(args) == 2:
                return f"{args[0]} > {args[1]} ? {args[0]} : {args[1]}"
            return f"{args[0]} > {args[1]} ? {[args[0]] + [args[2:]]} : {args[1:]}"
        return c_max(args)
    raise Exception("Unsupported sympy object %r of type %r" % (expression, type(expression)))

def write_c_licenses( fd, licenses ):
    for license in licenses:
        fd.write(f"/* SPDX-License-Identifier: {license} */\n")

def write_cheader( fd, registers ):
    definitions = []
    for r in registers.registers:
        if r.to_c_filter():
            definitions.append((r.address_define_name(), r.address))
        try:
            if r.width() <= 32:
                suffix = "U"
            else:
                suffix = "ULL"
        except TypeError:
            suffix = "ULL"
        for f in r.fields:
            if f.to_c_filter():
                if f.description:
                    definitions.append(( "comment", f.description ))
                offset = Macro(
                    f.offset_define_name(),
                    f.lowBit
                )
                definitions.append(( offset.prototype(), offset.body() ))
                length = Macro(
                    "%s_LENGTH" % f.mask_define_name(),
                    f.length()
                )
                definitions.append(( length.prototype(), length.body() ))
                # sympy doesn't support a bit shift (<<) operator, so here we
                # use power (**) instead.
                mask = Macro(
                    f.mask_define_name(),
                    f.mask()
                )
                definitions.append(( mask.prototype(), mask.body() ))

                for v in f.values:
                    definitions += v.to_c_definitions(f.mask_define_name())

    counted = collections.Counter(name for name, value in definitions)
    for name, value in definitions:
        if name == "comment":
            fd.write( "/*\n" )
            for line in value.splitlines():
                fd.write( (" * %s" % line.strip()).rstrip() + "\n" )
            fd.write( " */\n" )
            continue
        if counted[name] == 1:
            value = sympy_to_c(value)
            fd.write( "#define %-35s %s\n" % ( name, value ) )

def add_indent( s ):
    return s.replace("\n", "\n\t")

def print_cgetters( registers_list, fd_h, fd_c):
    all_regs = [r for registers in registers_list for r in registers.registers if r.to_c_filter and len(r.fields)]
    fd_h.write("enum riscv_debug_reg_ordinal {\n\t" +
               ",\n\t".join(
                   r.ordinal_name()
                   for r in all_regs
                   ) +
               "\n};\n")

    all_symbols = reduce(
            operator.or_,
            (f.symbols()
             for r in all_regs for f in r.fields if f.to_c_filter()))

    gen_sym_struct = lambda s: "struct {\n\t\tunsigned int value; int is_set;\n\t} " + s
    fd_h.write("typedef struct {\n\t" +
               ";\n\t".join(gen_sym_struct(s) for s in sorted((map(lambda sym: str(sym), all_symbols)))) +
               ";\n} riscv_debug_reg_ctx_t;\n\n")

    fd_h.write(Field.c_info_type())
    fd_h.write(Register.c_field_list_type())
    fd_h.write(Register.c_info_type())

    to_c = lambda string: sympy_to_c(sympy.simplify(string), lambda s: f"context.{s}.value", False)
    is_valid = lambda s: f"context.{s}.is_set"

    for r in all_regs:
        if len(r.fields):
            for f in r.fields:
                if f.to_c_filter() and len(f.values):
                    fd_c.write(f.c_values_array_def() + "\n");
            fd_c.write(r.c_field_getters(to_c, is_valid) + "\n");

    get_info_func = "riscv_debug_reg_info_t get_riscv_debug_reg_info(enum riscv_debug_reg_ordinal reg_ordinal)"
    fd_h.write(get_info_func + ";\n")
    fd_c.write(get_info_func + "\n" +
               "{\n\t" +
               add_indent("static const riscv_debug_reg_info_t debug_reg_info[] = {\n\t" +
                          add_indent("\n".join(f"[{r.ordinal_name()}] = {{\n\t{add_indent(r.c_info(to_c))}\n}},"
                                               for r in all_regs)) +
                          "\n};\n" +
                          "return debug_reg_info[reg_ordinal];") +
               "\n}\n")

def write_chisel( fd, registers ):
    fd.write("package freechips.rocketchip.devices.debug\n\n")
    fd.write("import chisel3._\n\n")

    fd.write("// This file was auto-generated from the repository at https://github.com/riscv/riscv-debug-spec.git,\n")
    fd.write("// 'make chisel'\n\n")

    fd.write("object " + registers.prefix + "RegAddrs {\n")

    for r in registers.registers:
        name = toCIdentifier( r.short or r.label ).upper()
        prefname = registers.prefix + name
        if (r.define and r.address):
            if r.description:
                fd.write ("  /* " + r.description + "\n  */\n")
            fd.write ("  def " + prefname + " =  "+ r.address + "\n\n")

    fd.write("}\n\n")

    for r in registers.registers:
        name = toCIdentifier( r.short or r.label ).upper()

        if (r.fields and r.define) :
            sorted_fields = sorted(r.fields, key = lambda x: int(x.lowBit), reverse = True)
            topbit = 31
            reserved = 0
            fd.write("class " + name + "Fields extends Bundle {\n\n")
            for f in sorted_fields:

                # These need try-catch blocks in the general case,
                # but for DM1 Registers it's fine.

                fieldlength = int(f.length())
                lowbit = int(f.lowBit)

                newtopbit = lowbit + fieldlength - 1

                if (newtopbit != topbit):
                    reservedwidth = topbit - newtopbit
                    print(reserved)
                    print(reservedwidth)
                    fd.write("  val reserved%d = UInt(%d.W)\n\n" % (reserved, reservedwidth))
                    reserved = reserved + 1
                if not f.define:
                    reservedwidth = fieldlength
                    fd.write("  val reserved%d = UInt(%d.W)\n\n" % (reserved, reservedwidth))
                    reserved = reserved + 1
                else:
                    if f.description:
                        fd.write("  /* " + f.description + "\n  */\n")

                    fd.write("  val " + toCIdentifier(f.name) + " = ")
                    if (int(fieldlength) > 1):
                        fd.write("UInt(%d.W)\n\n" % fieldlength)
                    else:
                        fd.write("Bool()\n\n")

                topbit = int(lowbit) - 1

            lastlowbit = int(sorted_fields[-1].lowBit)
            if (lastlowbit > 0 ):
                fd.write("  val reserved" + reserved + "= UInt(" + lastlowbit + ".W)\n")

            fd.write("}\n\n")

def address_value( address ):
    if type( address ) == str:
        try:
            return int( address, 0 )
        except ValueError:
            return address
    return address

def compare_address(a, b):
    try:
        return int(sympy.simplify("%s-(%s)" % (a, b)))
    except TypeError:
        return cmp(a, b)

def print_latex_index( registers ):
    print(registers.description)

    columns = [
        ("Address", "r"),
        ("Name", "l")]
    if any(r.sdesc for r in registers.registers):
        columns.append(("Description", "l"))
    columns.append(("Page", "l"))

    # Force this table HERE so that it doesn't get moved into the next section,
    # which will be the description of a register.
    print("   \\begin{longtable}{|%s|}" % "|".join(b for a, b in columns))
    print("      \\caption{%s \\label{%s}}\\\\" %
            (registers.name, toLatexIdentifier(registers.prefix, registers.label)))
    print("      \\hline")
    print("      %s \\\\" % (" & ".join(a for a, b in columns)))
    print("      \\hline")
    print("      \\endhead")

    print("      \\multicolumn{%d}{r}{\\textit{Continued on next page}} \\\\" %
            len(columns))
    print("      \\endfoot")
    print("      \\endlastfoot")
    for r in sorted( registers.registers,
            key=cmp_to_key(lambda a, b: compare_address(a.address, b.address))):
        if r.short and (r.fields or r.description):
            page = "\\pageref{%s}" % toLatexIdentifier(registers.prefix, r.short)
        else:
            page = ""
        if r.short:
            name = "%s ({\\tt %s})" % (r.name, r.short)
        else:
            name = r.name
        if r.sdesc:
            print("%s & %s & %s & %s \\\\" % ( r.address, name, r.sdesc, page ))
        else:
            print("%s & %s & %s \\\\" % ( r.address, name, page ))
    print("         \hline")
    print("   \end{longtable}")

def print_latex_custom( registers ):
    sub = "sub" * registers.depth
    for r in registers.registers:
        if not r.fields and not r.description:
            continue

        if r.short:
            if r.address:
                print("\\%ssection{%s ({\\tt %s}, at %s)}" % ( sub, r.name,
                        r.short, r.address ))
            else:
                print("\\%ssection{%s ({\\tt %s})}" % ( sub, r.name, r.short ))
            print("\index{%s}" % r.short)
        else:
            if r.address:
                print("\\%ssection{%s (at %s)}" % ( sub, r.name, r.address ))
            else:
                print("\\%ssection{%s}" % ( sub, r.name ))
            print("\index{%s}" % r.name)
        if r.label and r.define:
            print("\\label{%s}" % toLatexIdentifier(registers.prefix, r.label))
        print(r.description)
        print()

        if r.fields:
            if registers.prefix == "CSR_":
                if int(r.address, 0) >= 0xc00:
                    print("This CSR is read-only.")
                elif all(f.access in ('R', '0') for f in r.fields):
                    print("Writing this read/write CSR has no effect.")
                else:
                    print("This CSR is read/write.")
            elif all(f.access in ('R', '0') for f in r.fields):
                print("This entire register is read-only.")

            print("\\begin{center}")

            totalWidth = sum( ( 3 + f.columnWidth() ) for f in r.fields )
            split = int( math.ceil( totalWidth / 80. ) )
            fieldsPerSplit = int( math.ceil( float( len( r.fields ) ) / split ) )
            subRegisterFields = []
            for s in range( split ):
                subRegisterFields.append( r.fields[ s*fieldsPerSplit : (s+1)*fieldsPerSplit ] )

            for registerFields in subRegisterFields:
                tabularCols = ""
                for f in registerFields:
                    fieldLength = str( f.length() )
                    lowLen = float( len( f.lowBit ) )
                    highLen = float( len( f.highBit ) )
                    tabularCols += "p{%.1f ex}" % ( f.columnWidth() * highLen / ( lowLen + highLen ) )
                    tabularCols += "p{%.1f ex}" % ( f.columnWidth() * lowLen / ( lowLen + highLen ) )
                print("\\begin{tabular}{%s}" % tabularCols)

                first = True
                for f in registerFields:
                    if not first:
                        print("&")
                    first = False
                    if f.highBit == f.lowBit:
                        print("\\multicolumn{2}{c}{\\scriptsize %s}" % f.highBit)
                    else:
                        print("{\\scriptsize %s} &" % f.highBit)
                        print("\\multicolumn{1}{r}{\\scriptsize %s}" % f.lowBit)

                # The actual field names
                print("\\\\")
                print("         \hline")
                first = True
                for f in registerFields:
                    if first:
                        cols = "|c|"
                    else:
                        cols = "c|"
                        print("&")
                    first = False
                    print("\\multicolumn{2}{%s}{$|%s|$}" % ( cols, f.name ))
                print("\\\\")
                print("         \hline")

                # Size of each field in bits
                print(" & ".join( "\\multicolumn{2}{c}{\\scriptsize %s}" % f.length() for f in registerFields ))
                print("\\\\")

                print("   \\end{tabular}")

            print("\\end{center}")

        columns = [("l", "Field", lambda f: f.name)]
        columns += [("p{0.5\\textwidth}", "Description", lambda f: f.latex_description())]
        if not registers.skip_access:
            columns += [("c", "Access", lambda f: f.access)]
        if not registers.skip_reset:
            columns += [("l", "Reset", lambda f: f.reset)]

        if any( f.description for f in r.fields ):
            print("\\tabletail{\\hline \\multicolumn{%d}{|r|}" % len(columns))
            print("   {{Continued on next page}} \\\\ \\hline}")
            print("   \\begin{longtable}{|%s|}" % "|".join(c[0] for c in columns))

            print("   \\hline")
            print("   %s\\\\" % " & ".join(c[1] for c in columns))
            print("   \\hline")
            print("   \\endhead")

            print("   \\multicolumn{%d}{r}{\\textit{Continued on next page}} \\\\" % \
                    len(columns))
            print("   \\endfoot")
            print("   \\endlastfoot")

            for f in r.fields:
                if f.description or f.values:
                    print("\\label{%s}" % toLatexIdentifier(registers.prefix, r.short or r.label, f.name))
                    print("\\index{%s}" % f.name)
                    print("   |%s| &" % str(columns[0][2](f)), end=' ')
                    print("%s\\\\" % " & ".join(str(c[2](f)) for c in columns[1:]))
                    print("   \\hline")

            print("   \\end{longtable}")
        print()

def print_latex_register( registers ):
    print("%\\usepackage{register}")
    sub = "sub" * registers.depth
    for r in registers.registers:
        if not r.fields and not r.description:
            continue

        if r.short:
            print("\\%ssection{%s (%s)}" % ( sub, r.name, r.short ))
        else:
            print("\\%ssection{%s}" % ( sub, r.name ))
        print(r.description)

        if not r.fields:
            continue
        print("\\begin{register}{H}{%s}{%s}" % ( r.name, r.address ))
        print("   \\label{reg:%s}{}" % r.label)
        for f in r.fields:
            length = f.length()
            if length is None:
                # If we don't know the length, draw it as 10 bits.
                length = 10
            print("   \\regfield{%s}{%d}{%s}{{%s}}" % (
                    f.name, length, f.lowBit, f.reset ))

        print("   \\begin{regdesc}")
        print("      \\begin{reglist}")
        for f in r.fields:
            if f.description:
                print("      \\item[%s] (%s) %s" % ( f.name, f.access,
                        f.description ))
        print("      \\end{reglist}")
        print("   \\end{regdesc}")

        print("\\end{register}")
        print()

def remove_indent( text ):
    return "\n".join( line.lstrip() for line in text.splitlines() )


def add_continuations(text):
    lines = text.splitlines()
    result = []
    for i in range(len(lines)):
        current_line = lines[i].rstrip()
        if len(current_line) > 0 and i < len(lines) - 1 and lines[i + 1].strip() != "":
            current_line += " +"
        result.append(current_line)
    return "\n".join(result)

def write_bytefield_row( fd, fields ):
    # Have a minimum width, otherwise small registers look huge.
    totalWidth = sum( f.columnWidth() for f in fields )
    padding = max(0, 24 - totalWidth)
    fd.write("[bytefield]\n")
    fd.write("----\n")
    fd.write("(def row-height 45)\n")
    fd.write("(def row-header-fn nil)\n")
    fd.write(f"(def boxes-per-row {totalWidth + padding})\n")
    # TODO: column headers

    headers = [""] * padding
    columnOffset = 0
    for f in reversed(fields):
        columnWidth = f.columnWidth()
        if f.length() == 1:
            if columnWidth > 1:
                before = columnWidth // 2
                after = columnWidth - before - 1
                headers += [""] * before
                headers.append(f.lowBit)
                headers += [""] * after
            else:
                headers.append(f.lowBit)
        else:
            # If low/high bit need more than 2 characters, place them one in
            # from the end so they don't overflow into the neighboring field.
            # Really this should be done with right/left alignment, but
            # bytefield doesn't seem to support that.
            if len(f.lowBit) > 2:
                start = ["", f.lowBit]
            else:
                start = [f.lowBit]
            if len(f.highBit) > 2:
                end = [f.highBit, ""]
            else:
                end = [f.highBit]
            assert columnWidth >= len(start) + len(end)
            headers += start
            headers += [""] * (columnWidth - len(start) - len(end))
            headers += end
        columnOffset += columnWidth
    # remove whitespace to save space
    headers = [h.replace(" ", "") for h in headers]
    fd.write('(draw-column-headers {:font-size 15 :height 17 :labels [%s]})\n' % " ".join(f'"{h}"' for h in reversed(headers)))

    for f in fields:
        fd.write('(draw-box (text "%s" {:font-size 20}) {:span %s})\n' % ( f.name, f.columnWidth() ))
    if padding:
        fd.write('(draw-box "" {:span %s :borders {}})\n' % ( padding ))

    for f in fields:
        fd.write('(draw-box "%s" {:span %s :borders {}})\n' % ( f.length(), f.columnWidth() ))
    if padding:
        fd.write('(draw-box "" {:span %s :borders {}})\n' % ( padding ))

    fd.write("----\n")

def write_bytefield( fd, register ):
    """Return a bytefield representation of the register."""
    totalWidth = sum( f.columnWidth() for f in register.fields )

    maxWidth = 40
    if totalWidth > maxWidth:
        rowCount = math.ceil(totalWidth / maxWidth)
    else:
        rowCount = 1

    rowWidth = totalWidth / rowCount
    rows = [[]]
    offset = 0
    for f in register.fields:
        if rowWidth - offset > f.columnWidth() / 2 or len(rows) >= rowCount:
            rows[-1].append(f)
            offset += f.columnWidth()
        else:
            rows.append([])
            rows[-1].append(f)
            offset = f.columnWidth()

    # Provide separation from a previous ordered list.
    fd.write("\n")
    for row in rows:
        write_bytefield_row(fd, row)

def write_adoc( fd, registers ):
    sub = "=" * registers.depth
    for r in registers.registers:
        if not r.fields and not r.description:
            continue

        if r.label and r.define:
            fd.write("[[%s]]\n" % toAdocIdentifier(registers.prefix, r.label))
        if r.short:
            # TODO: Check that (((foo))) renders as ((foo)) inside parens
            if r.address:
                fd.write(f"==={sub} {r.name} ((({r.short})), at {r.address})\n")
            else:
                fd.write(f"==={sub} {r.name} ((({r.short})))\n")
            # TODO: confirm that index works
        else:
            if r.address:
                fd.write(f"==={sub} ((`{r.name}`)) (at {r.address})\n")
            else:
                fd.write(f"==={sub} ((`{r.name}`))\n")
        fd.write("\n")
        fd.write(remove_indent(r.description))
        fd.write("\n\n")

        if r.fields or r.diagram:
            if registers.prefix == "CSR_":
                if int(r.address, 0) >= 0xc00:
                    fd.write("This CSR is read-only.\n")
                elif all(f.access in ('R', '0') for f in r.fields):
                    fd.write("Writing this read/write CSR has no effect.\n")
                else:
                    fd.write("This CSR is read/write.\n")
            elif all(f.access in ('R', '0') for f in r.fields):
                fd.write("This entire register is read-only.\n")

            if r.diagram:
                fd.write(f"{remove_indent(r.diagram)}\n")
            else:
                write_bytefield( fd, r )

        columns = [("<23", "Field", lambda f: f"(({f.name}))")]
        columns += [("<61", "Description", lambda f: f.latex_description())]
        if not registers.skip_access:
            columns += [("^10", "Access", lambda f: f"*{f.access}*")]
        if not registers.skip_reset:
            columns += [("^10", "Reset", lambda f: f.reset)]

        if any( f.description for f in r.fields ):
            cols = ",".join(c[0] for c in columns)
            fd.write(f'[float="center",align="center",cols="{cols}",options="header"]\n')
            fd.write("|===\n")

            fd.write("|" + " |".join(c[1] for c in columns) + "\n")

            for f in r.fields:
                if f.description or f.values:
                    identifier = toAdocIdentifier(r.short or r.label, f.name)
                    fd.write(f"|[[{identifier}]] `{columns[0][2](f)}`\n")
                    for c in columns[1:]:
                        fd.write("a|" + remove_indent( c[2](f) ) + "\n")

            fd.write("|===\n")
        fd.write("\n")

def write_adoc_index( fd, registers ):
    fd.write(remove_indent(registers.description) + "\n")

    columns = [
        ("Address", "1"),
        ("Name", "6")]
    if any(r.sdesc for r in registers.registers):
        columns.append(("Description", "6"))
    columns.append(("Section", "2"))

    fd.write(f"[[tab:{registers.label}]]\n")
    fd.write(f".{registers.name}\n")
    fd.write('[cols="' + ",".join(c[1] for c in columns) + '",options="header"]\n')
    fd.write("|===\n")
    fd.write("|" + " |".join(c[0] for c in columns) + "\n")

    for r in sorted( registers.registers,
            key=cmp_to_key(lambda a, b: compare_address(a.address, b.address))):
        identifier = toAdocIdentifier(registers.prefix, r.short or r.name)
        if r.short:
            name = "%s ({%s})" % (r.name, identifier)
        else:
            name = "{%s}" % identifier
        if r.fields or r.description:
            link = f"xref:{identifier}[]"
        else:
            link = ""
        if r.sdesc:
            fd.write("|%s |%s |%s| %s\n" % ( r.address, name, r.sdesc, link ))
        else:
            fd.write("|%s |%s| %s\n" % ( r.address, name, link ))
    fd.write("|===\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument( 'path' )
    parser.add_argument( '--register', action='store_true',
            help='Use the LaTeX register module. No support for symbolic bit '
            'start/end positions.' )
    parser.add_argument( '--custom', action='store_true',
            help='Use custom LaTeX.' )
    parser.add_argument( '--adoc',
            help='Write asciidoc registers to the named file.' )
    parser.add_argument( '--adoc-definitions',
            help='Write asciidoc register style definitions to the named file.' )
    parser.add_argument( '--definitions',
            help='Write register style definitions to the named file.' )
    parser.add_argument( '--cheader',
            help='Write C #defines to the named file.' )
    parser.add_argument( '--chisel',
            help='Write Scala Classes to the named file.' )
    parser.add_argument( '--cgetters', dest='xml_paths', nargs='+')
    parser.add_argument( '--create',
            help='Line included in the output described how the file was created.' )
    parsed = parser.parse_args()

    if (parsed.xml_paths):
        registers_list = [parse_xml( xml_path ) for xml_path in parsed.xml_paths]
        license_lists = [registers.licenses for registers in registers_list]
        # Assert every license list is the same
        assert all(license_lists[0] == license_list for license_list in license_lists), \
                "All XML files must have the same SPDX-License-Identifier"
        fd_h = open( parsed.path + ".h", "w" )
        write_c_licenses( fd_h, license_lists[0] )
        if (parsed.create):
            fd_h.write(f"/* {parsed.create} */\n\n")
        fd_h.write("#ifndef DEBUG_DEFINES_H\n#define DEBUG_DEFINES_H\n")
        fd_c = open( parsed.path + ".c", "w" )
        write_c_licenses( fd_c, license_lists[0] )
        if (parsed.create):
            fd_c.write(f"/* {parsed.create} */\n\n")
        fd_c.write(f'#include "{parsed.path}.h"\n#include <stddef.h>\n#include <assert.h>\n')
        for registers in registers_list:
            write_cheader( fd_h, registers )
        print_cgetters(registers_list, fd_h, fd_c)
        fd_h.write("#endif\n")
        return

    registers = parse_xml( parsed.path )
    if parsed.definitions:
        write_definitions( open( parsed.definitions, "w" ), registers )
    if parsed.cheader:
        with open( parsed.cheader, "w" ) as fd:
            write_c_licenses( fd, registers.licenses )
            write_cheader( fd, registers )
    if parsed.chisel:
        write_chisel( open( parsed.chisel, "w" ), registers )
    if not registers.skip_index and not parsed.adoc:
        print_latex_index( registers )
    if parsed.register:
        assert(0)
        print_latex_register( registers )
    if parsed.custom:
        print_latex_custom( registers )
    if parsed.adoc:
        with open( parsed.adoc, "w" ) as fd:
            fd.write(f"// Auto-generated on {datetime.now()} from {parsed.path}\n")
            if not registers.skip_index:
                write_adoc_index( fd, registers )
            write_adoc( fd, registers )
    if parsed.adoc_definitions:
        with open( parsed.adoc_definitions, "w" ) as fd:
            fd.write(f"// Auto-generated on {datetime.now()} from {parsed.path}\n")
            write_adoc_definitions( fd, registers )

    #sed_convert(registers)

def sed_convert( registers ):
    for r in registers.registers:
        regid = r.short or r.label
        if r.define:
            latex = "\\\\R" + toLatexIdentifier( registers.prefix, regid )
            adoc = "{" + toAdocIdentifier( registers.prefix, regid ) + "}"
            print(f"s/{latex}/{adoc}/g")
        for f in r.fields:
            if f.define:
                latex = "\\\\F" + toLatexIdentifier( registers.prefix, regid, f.name )
                adoc = "{" + toAdocIdentifier( regid, f.name ) + "}"
                print(f"s/{latex}/{adoc}/g")

sys.exit( main() )
