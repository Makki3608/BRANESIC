
#'a foo b -> c'
#
#Add your own Actions !!!!!!
# 
#Here are the rules:
#
#keep in mind, ',' exits EVERYTHING
#
#,t:0, will set the current cell to 0. If it doesn't. Bad things happen. 
#
#Starts on 'workspace' cell 0
#
#'Workspace' moight not be clean. If neccessary, overwrite cells with ,t:0,
#
#_x_ fetches input x (_0_, _1_, etc)
#
#~x~ fetches 'workspace' cell x (~0~, ~1~, etc)
#
#Output of action must be on workspace 0. Must end pointing at workspace 0. 
#
#Unless overwritten in program, g_workspace_size will be set automatically, make sure you "visit" every cell you plan on using

Symbol_Dictionary = {
    "+":        "_0_>_1_[-<+>]<",
    "-":        "_0_>_1_[-<->]<",
    "/":        "_1_>_0_#div#><<~2~",
    "*":        "_1_>_0_#mul#><<~2~",
    "%":        "_1_>_0_#mod#><<~2~",
    "==":       "_0_>_0_>_1_#div#><<_1_#mod#<,t:0,+>>[<<,t:0,>>,t:0,]>-[<<<,t:0,>>>,t:0,]<<<", #TODO handle zeors !
    "!=":       "_0_>_0_>_1_#div#><<_1_#mod#<,t:0,>>[<<+>>,t:0,]>-[<<<,t:0,+>>>,t:0,]<<<", #TODO handle zeors ! (basically all of them)
    "<":        "_0_>_1_-#div#>?#abs#><<<~3~",
    ">":        "_1_>_0_-#div#>?#abs#><<<~3~",
    "<=":       "_0_>_1_#div#>?#abs#><<<~3~",
    ">=":       "_1_>_0_#div#>?#abs#><<<~3~",
    "?z":       ",t:0,+2>_0_#abs#>?[<<->>,t:0,]<_1_#abs#>?[<<->>,t:0,]<<",
    "not":      ",t:0,+>_1_[<->,t:0,]<",#okay i need to find a better way to do this but 'not' gets hardcoded to only take argument _1_. _0_ gets 'voided'
    "nand":     ",t:0,+2>_0_[<->,t:0,]_1_[<->,t:0,]<?",
    "&&":       ",t:0,+2>_0_[<->,t:0,]_1_[<->,t:0,]<?>~0~<,t:0,+>[<->,t:0,]<",
    "||":       ",t:0,>_0_[<+>,t:0,]_1_[<+>,t:0,]<?",
    "^":      "_1_->_0_>_0_><<<[->>#mul#~3~<<]~2~",
}

#Same rules as for Symbols
#
# 'a, b, !foobar! -> c
#
#Names must start and end with '!'
#
#Okay so you can't actually make a function that contains a symbol in its name. Meaning !ferdi*nand*! and !*not*ary! are forbidden.  
#

Function_Dictionary = {
    "!rgb!": ",t:0,+256>_2_#mul#_1_[->+<]~2~#mul#_0_[->+<]<~2~",
    "!reset_palette!": ",t:0,+16777215>,t:0,+12632256>,t:0,+8421504>,t:0,#set_palette#",#to gray, sadly#
    "!save!": "_0_^v",#these let you save 1 number to persistent memory. A better way to do that is TODO. These will stay for simple tasks but they might break the new way ( maybe )
    "!load!": ">^<v",
}

#
#fun fact: symbols actually become functions :)
#

#
#prefixes shoudl always leave the cells as they found them. They should always end at index 0.
#
Prefix_Dictionary = {
    0:  "",#nothing
    1:  ">+60>,g:level_time,#mod#>[.]<,t:0,<,t:0,<",#exits if level time isn't divisible by 60
    2:  ",g:turn_frames,[.]",#exits unless the player has just moved
    3:  ",g:level_time,[.]",#exits unless the level just started
    4:  ",g:death_frames,-[.]",#exits unless the player has just died
}