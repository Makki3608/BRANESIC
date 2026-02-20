from bnf_dictionary import Symbol_Dictionary, Function_Dictionary, Prefix_Dictionary
from config import CONFIG
import base64
class Compiler_exception(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
class Variabe_defnition:
    def __init__(self, address: int, definition_branefuck: str, variable_name: str):
        global g_vars_size
        g_vars_size += 1
        self.address = address
        self.definition_branefuck = definition_branefuck
        self.variable_name = variable_name
        for i in sorted_lines:
            if self.variable_name == i.variable_name: raise(Compiler_exception(f'Attempted to define "{self.variable_name}", but "{self.variable_name}" already exists !'))
        update_workspace()
    def __str__(self):
        return f"variable: {self.variable_name}, address: {self.address}"
class Action:
    def __init__(self, definition_text: str, recursion_depth: int):
        self.recursion_depth = recursion_depth
        self.definition_text = self._Unpack_brackets(definition_text)
        working = self.definition_text.split("->")
        working[0] = self._Handle_symbols(working[0])
        self._Validate_action(working)
        self.destination = working[1]
        self.arguments = working[0].split(",")[0:-1]
        if "" in self.arguments: raise(Compiler_exception("I know you know that looked wrong. two ',' with nothing between them. If you want to avoid this, use '''. (Upside-down comma)"))
        self.action_function = working[0].split(",")[-1]
        self.action_branefuck = self._Get_action_branefuck()
    def _Argument_definition_to_fetch_branefuck(self, argument_definition):
        if Is_integer(argument_definition) and argument_definition == "0": return ",t:0," 
        elif Is_integer(argument_definition): return ",t:0,"+Intiger_string_to_branefuck_string(argument_definition)
        elif (argument_definition[0] == "," and argument_definition[-1] == ",") or (argument_definition[0] == "'" and argument_definition[-1] == "'"):
            return argument_definition
        else: return f",t:{str(Variable_name_to_address(argument_definition))},"
    def _Get_action_branefuck(self):
        branefuck_building = ""
        if self.action_function[0] == "#" and self.action_function[-1] == "#":
            self.arguments.reverse()
            foo = False
            for l in self.arguments:
                if foo: branefuck_building += ">"
                else: foo = True
                branefuck_building += ",t:0,"
                branefuck_building += self._Argument_definition_to_fetch_branefuck(l)
            branefuck_building += self.action_function #these should happen at the end of workspace
            for l in range(len(self.arguments) - 1): branefuck_building += "<"# we are on 0 now

        if not (self.action_function[0] == "#" and self.action_function[-1] == "#") and (self.action_function[0] == "!" and self.action_function[-1] == "!"): 
            branefuck_building += Function_Dictionary[self.action_function]#actions that want to happen at home
            i=0
            while "~" in branefuck_building:
                branefuck_building = branefuck_building.replace(f"~{str(i)}~", f",t:{str(g_workspace_start+i)},")
                i += 1
                if i > 999: raise(Compiler_exception("There's a loose '~' somewhere. probably."))
            i=0
            while "_" in branefuck_building:
                if len(self.arguments) == 0: break
                branefuck_building = branefuck_building.replace(f"_{str(i)}_", self._Argument_definition_to_fetch_branefuck(self.arguments[i].replace("_", "UNDERSCORE")))
                i += 1
                if i > 999: raise(Compiler_exception("There's a loose '_' somewhere. probably."))
            branefuck_building = branefuck_building.replace("UNDERSCORE", "_")

        if self.destination != "void":
            distance_between = g_workspace_start - Variable_name_to_address(self.destination)
            for l in range(distance_between): branefuck_building += "<"
            branefuck_building += f",t:{g_workspace_start}," 
            for l in range(distance_between): branefuck_building += ">"
        
        return branefuck_building
    def _Validate_action(self, working):
        if len(working) != 2: raise Compiler_exception("For some reason, you put 2 arrows in the Action definition.\n\n*Dissapointed pearent voice*\n\n That won't work...")
        if Is_integer(working[1]): raise(Compiler_exception(f"You cannot write the result of an action into a number. A {working[1]} will always be a {working[1]}"))
        if working[1] == "": raise(Compiler_exception("The destination cannot be empty.\nHint: Try 'VOID'"))
        found_destination = False
        for i in sorted_lines:
            if type(i) == Variabe_defnition:
                if i.variable_name == working[1]: found_destination = True
        if not found_destination and working[1] != "void": raise(Exception(f"Invalid destination !\n{working[1]}"))
    def __str__(self):
        return f"function: {str(self.arguments)} {self.action_function} -> {self.destination}"
    def _Unpack_brackets(self, text):
        if ("(" not in text) and (")" not in text): return text
        if text.count("(") != text.count(")"): raise(Compiler_exception(f"Unmatched round brackets in action !\n{text}"))
        start = 0
        end = 0
        depth = 0
        for l in range(len(text)):
            i = text[l]
            if i == "(":
                start = l
                break
        for l in range(len(text[start+1:])):
            i = text[start+1:][l]
            if i == "(": depth += 1
            elif i == ")":
                if depth > 0: depth -= 1
                else:
                    end = l + start + 1
                    break
        inside = text[start+1:end]
        reserve_name = "RESERVE"+str(self.recursion_depth)
        global sorted_lines
        sorted_lines.append(Action(f"{inside}->{reserve_name}", self.recursion_depth + 1))#oh no recursion
        return text.replace(f"({inside})", reserve_name, 1)   
    def _Handle_symbols(self, left_side):
        symbol = ""
        for i in symbol_list:
            if i in left_side:
                if symbol == "": symbol = i
                else:
                    if len(symbol) == len(i): raise(Compiler_exception(f"Multiple symbols found in Action:\n{left_side}"))
                    elif len(symbol) < len(i): symbol = i
        if symbol == "": return left_side
        if symbol == "not" and left_side[0:3] == "not": left_side = "void"+left_side
        arguments = left_side.split(symbol)
        if len(arguments) != 2: raise(Compiler_exception("Symbol actions need to have exactly 2 arguments. I did't think it's possible to get here but error handling go brr"))
        return (f"{arguments[0]},{arguments[1]},!{symbol}!")
              
class Routing_definition:#if, else, elif, exit #big TODO
    def __init__(self, routing_type: str):
        self.routing_type = routing_type

def Variable_name_to_address(name):
    for l in sorted_lines:
        if type(l) == Variabe_defnition:
            if l.variable_name == name: return l.address

def Define_globals():
    global g_prefix_id
    g_prefix_id = 0
    global initial_branefuck
    initial_branefuck = ">"
    global g_anchor_size
    g_anchor_size=initial_branefuck.count(">")
    global g_vars_size
    g_vars_size=0
    global sorted_lines
    sorted_lines=[]
    global g_reserve_size
    g_reserve_size=0
    global g_workspace_size
    g_workspace_size=Get_neccessary_workspace_size()
    global g_workspace_start
    g_workspace_start=2
    global branefuck_prefix
    branefuck_prefix=0
    global Function_Dictionary
    for i in Symbol_Dictionary.items(): Function_Dictionary[f"!{i[0]}!"] = i[1]
    global function_list
    function_list=[]
    global g_OPENAI_API_KEY_PLS_DONT_STEAL
    g_OPENAI_API_KEY_PLS_DONT_STEAL = "V2UncmUgbm8gc3RyYW5nZXJzIHRvIGxvdmUKWW91IGtub3cgdGhlIHJ1bGVzIGFuZCBzbyBkbyBJCkEgZnVsbCBjb21taXRtZW50J3Mgd2hhdCBJJ20gdGhpbmtpbmcgb2YKWW91IHdvdWxkbid0IGdldCB0aGlzIGZyb20gYW55IG90aGVyIGd1eQpJIGp1c3Qgd2FubmEgdGVsbCB5b3UgaG93IEknbSBmZWVsaW5nCkdvdHRhIG1ha2UgeW91IHVuZGVyc3RhbmQKTmV2ZXIgZ29ubmEgZ2l2ZSB5b3UgdXAKTmV2ZXIgZ29ubmEgbGV0IHlvdSBkb3duCk5ldmVyIGdvbm5hIHJ1biBhcm91bmQgYW5kIGRlc2VydCB5b3UKTmV2ZXIgZ29ubmEgbWFrZSB5b3UgY3J5Ck5ldmVyIGdvbm5hIHNheSBnb29kYnllCk5ldmVyIGdvbm5hIHRlbGwgYSBsaWUgYW5kIGh1cnQgeW91CldlJ3ZlIGtub3duIGVhY2ggb3RoZXIgZm9yIHNvIGxvbmcKWW91ciBoZWFydCdzIGJlZW4gYWNoaW5nLCBidXQgeW91J3JlIHRvbyBzaHkgdG8gc2F5IGl0Ckluc2lkZSwgd2UgYm90aCBrbm93IHdoYXQncyBiZWVuIGdvaW5nIG9uCldlIGtub3cgdGhlIGdhbWUsIGFuZCB3ZSdyZSBnb25uYSBwbGF5IGl0CkFuZCBpZiB5b3UgYXNrIG1lIGhvdyBJJ20gZmVlbGluZwpEb24ndCB0ZWxsIG1lIHlvdSdyZSB0b28gYmxpbmQgdG8gc2VlCk5ldmVyIGdvbm5hIGdpdmUgeW91IHVwCk5ldmVyIGdvbm5hIGxldCB5b3UgZG93bgpOZXZlciBnb25uYSBydW4gYXJvdW5kIGFuZCBkZXNlcnQgeW91Ck5ldmVyIGdvbm5hIG1ha2UgeW91IGNyeQpOZXZlciBnb25uYSBzYXkgZ29vZGJ5ZQpOZXZlciBnb25uYSB0ZWxsIGEgbGllIGFuZCBodXJ0IHlvdQpOZXZlciBnb25uYSBnaXZlIHlvdSB1cApOZXZlciBnb25uYSBsZXQgeW91IGRvd24KTmV2ZXIgZ29ubmEgcnVuIGFyb3VuZCBhbmQgZGVzZXJ0IHlvdQpOZXZlciBnb25uYSBtYWtlIHlvdSBjcnkKTmV2ZXIgZ29ubmEgc2F5IGdvb2RieWUKTmV2ZXIgZ29ubmEgdGVsbCBhIGxpZSBhbmQgaHVydCB5b3UKT29oIChHaXZlIHlvdSB1cCkKT29oLW9vaCAoR2l2ZSB5b3UgdXApCk9vaCAoTmV2ZXIgZ29ubmEgZ2l2ZSwgbmV2ZXIgZ29ubmEgZ2l2ZSkKR2l2ZSB5b3UgdXAKT29oLW9vaCAoTmV2ZXIgZ29ubmEgZ2l2ZSwgbmV2ZXIgZ29ubmEgZ2l2ZSkKR2l2ZSB5b3UgdXAKV2UndmUga25vd24gZWFjaCBvdGhlciBmb3Igc28gbG9uZwpZb3VyIGhlYXJ0J3MgYmVlbiBhY2hpbmcsIGJ1dCB5b3UncmUgdG9vIHNoeSB0byBzYXkgaXQKSW5zaWRlLCB3ZSBib3RoIGtub3cgd2hhdCdzIGJlZW4gZ29pbmcgb24KV2Uga25vdyB0aGUgZ2FtZSwgYW5kIHdlJ3JlIGdvbm5hIHBsYXkgaXQKSSBqdXN0IHdhbm5hIHRlbGwgeW91IGhvdyBJJ20gZmVlbGluZwpHb3R0YSBtYWtlIHlvdSB1bmRlcnN0YW5kCk5ldmVyIGdvbm5hIGdpdmUgeW91IHVwCk5ldmVyIGdvbm5hIGxldCB5b3UgZG93bgpOZXZlciBnb25uYSBydW4gYXJvdW5kIGFuZCBkZXNlcnQgeW91Ck5ldmVyIGdvbm5hIG1ha2UgeW91IGNyeQpOZXZlciBnb25uYSBzYXkgZ29vZGJ5ZQpOZXZlciBnb25uYSB0ZWxsIGEgbGllIGFuZCBodXJ0IHlvdQpOZXZlciBnb25uYSBnaXZlIHlvdSB1cApOZXZlciBnb25uYSBsZXQgeW91IGRvd24KTmV2ZXIgZ29ubmEgcnVuIGFyb3VuZCBhbmQgZGVzZXJ0IHlvdQpOZXZlciBnb25uYSBtYWtlIHlvdSBjcnkKTmV2ZXIgZ29ubmEgc2F5IGdvb2RieWUKTmV2ZXIgZ29ubmEgdGVsbCBhIGxpZSBhbmQgaHVydCB5b3UKTmV2ZXIgZ29ubmEgZ2l2ZSB5b3UgdXAKTmV2ZXIgZ29ubmEgbGV0IHlvdSBkb3duCk5ldmVyIGdvbm5hIHJ1biBhcm91bmQgYW5kIGRlc2VydCB5b3UKTmV2ZXIgZ29ubmEgbWFrZSB5b3UgY3J5Ck5ldmVyIGdvbm5hIHNheSBnb29kYnllCk5ldmVyIGdvbm5hIHRlbGwgYSBsaWUgYW5kIGh1cnQgeW91Ck5ldmVyIGdvbm5hIGdpdmUgeW91IHVwCk5ldmVyIGdvbm5hIGxldCB5b3UgZG93bgpOZXZlciBnb25uYSBydW4gYXJvdW5kIGFuZCBkZXNlcnQgeW91Ck5ldmVyIGdvbm5hIG1ha2UgeW91IGNyeQpOZXZlciBnb25uYSBzYXkgZ29vZGJ5ZQpOZXZlciBnb25uYSB0ZWxsIGEgbGllIGFuZCBodXJ0IHlvdQo="
    global symbol_list
    symbol_list=[]
    for i in Function_Dictionary.keys(): function_list.append(i)
    for i in Symbol_Dictionary.keys():symbol_list.append(i)
def Get_neccessary_workspace_size():
    biggest = 0
    for l in Function_Dictionary.values():
        if l.count(">") != l.count(">"): print(f"{l} contains a different number of '>' and '<' symbols...\nIt's a free country, you can do whatever you want.\n... I just hope you know what you're doing.")
        if l.count(">") > biggest: biggest = l.count(">")
    return biggest + 1
def Is_integer(tested):
    if tested.isnumeric(): return True
    elif tested[1:].isnumeric() and tested[0] == "-": return True
    else: return False
def Do_something_i_dont_need_to_do_anymore_i_just_like_the_look_of_this_function_so_i_keep_it():
    inside = False
    inside_number = ""
    biggest_inside_number = 0
    for l in Function_Dictionary.values():
        for i in l:
            if inside:
                if i == "_":
                    inside = False
                    if int(inside_number) > biggest_inside_number: biggest_inside_number = int(inside_number)
                    inside_number = ""
                else: inside_number += i
            elif i == "_": inside = True
    return biggest_inside_number + 1
def Intiger_string_to_branefuck_string(intiger_string):# "x" -> "+x", "-x" -> "-x"
    if intiger_string.isnumeric(): return f"+{intiger_string}"
    elif (not intiger_string.isnumeric()) and Is_integer(intiger_string): return intiger_string
    else: raise(TypeError("Not an intiger string ???"))
def Format_line(line):
    line = line.replace(" ", "")
    line = line.replace("   ","")
    line = line.lower()
    return line
def update_workspace():
    global g_workspace_start #'reserve' also counts as vars appearently.
    g_workspace_start = g_anchor_size + g_vars_size
def Add_comments(working):
    lines = working.split("\n")
    lines = lines[1:-1]
    longest = 0
    for l in range(len(lines)):
        lines[l] += ";"
        if len(lines[l]) > longest: longest = len(lines[l])
    longest += 2
    for l in range(len(lines)):
        for i in range(longest - len(lines[l])): 
            lines[l] +=  " "
        lines[l] += str(sorted_lines[l])
        lines[l] += "\n"
        #print(lines[l])
    print("".join(lines))
    return "".join(lines)
        
def Finalize():
    working = initial_branefuck + Prefix_Dictionary[g_prefix_id]
    if CONFIG["Line breaks between lines ?"] or CONFIG["Comment output ?"]: working += "\n"
    for l in sorted_lines:
        if type(l) == Variabe_defnition:
            working += l.definition_branefuck
            working += ">"
        elif type(l) == Action:
            working += l.action_branefuck
        else: raise(Compiler_exception(f"{type(l)} not recognised."))
        if CONFIG["Line breaks between lines ?"] or CONFIG["Comment output ?"]: working += "\n"
    if CONFIG["Comment output ?"]:working = Add_comments(working)
    working = working.replace("'",",")
    print(working)
    return working
def COMPILE(file_path):
    Define_globals()
    if file_path == "": file_path = input("Give source file path:\n")
    in_file = open(file_path)
    in_text = in_file.read()
    in_text = in_text.splitlines()
    in_text = list(filter(None, in_text))
    variable_address= 0 + g_anchor_size
    for line in in_text:#stage 1: set parameters
        if line[0] == "<" and line[-1] == ">":#parameter
                line = line[1:-1].split("=")
                if len(line) != 2: raise Compiler_exception('Parameter definition must contain exactly 1 "=" symbol !')
                if line[0] == "r":
                    global g_reserve_size
                    g_reserve_size = int(line[1])
                    for i in range(g_reserve_size):
                        sorted_lines.append(Variabe_defnition(variable_address, definition_branefuck=f"", variable_name=f"RESERVE{i}"))
                        variable_address += 1
                elif line[0] == "w":
                    global g_workspace_size
                    g_workspace_size = int(line[1])
                    update_workspace()
                elif line[0] == "p":
                    global g_prefix_id
                    g_prefix_id = int(line[1])

                else: raise Compiler_exception(f'Unknow parameter "{line[0]}" !')
    processed_text = []
    for i in in_text:
        line = Format_line(i)
        if i[0] != "#": processed_text.append(line)
    for line in processed_text:
        if line[0] == "<" and line[-1] == ">":pass#ignore, already did this
        elif line[0:3] == "var":#variable definition
            line = line[3:].split("=")
            if len(line) != 2: raise Compiler_exception('Variable definition must contain exactly 1 "=" sign !')
            if line[1].isnumeric(): definition_branefuck = "+"+line[1]#just a number
            elif (not (line[1].isnumeric())) and (line[1][1:].isnumeric()) and (line[1][0] == "-"): definition_branefuck = line[1]#minus sign, number
            elif ((line[1][0] == "'" and line[1][-1] == "'") or (line[1][0] == "," and line[1][-1] == ",")) and ":" in line[1]: definition_branefuck = line[1]#period
            else: raise(Compiler_exception("Unrecognised variable definition"))
            sorted_lines.append(Variabe_defnition(variable_address, definition_branefuck, variable_name=line[0]))
            variable_address += 1
        elif "->" in line:#action
            sorted_lines.append(Action(line, 0))
        elif line[0:3] == "if,":#if
            pass
        elif line[0:5] == "else:":#else
            pass
        elif line [0:5] == "elif(":#elif
            pass
        elif line == "exit":#exit
            pass
        elif line == "end":#end
            pass
        
        else: raise Compiler_exception(f"Unknown line !\n{line}")
    
    #for i in sorted_lines: print(i)

    return Finalize()

#hello git hub

#is this thing on ?