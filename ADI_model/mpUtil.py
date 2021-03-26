#! /usr/bin/python

#Copyright  2021 <Analog Devices>
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import re
import sys
import math

def decodeEngineeringNotation(num):
    m = re.match('[-+]?(\d+(\.\d*)?|\.\d+)([fpnumkMGTP])',num)
    if(m):
        mult = m.group(3)
        num = float(m.group(1))
        multiplier = 1
        if   mult is 'f' :
            multiplier = 1e-15
        elif mult is 'p' :
            multiplier = 1e-12
        elif mult is 'n' :
            multiplier = 1e-09
        elif mult is 'u' :
            multiplier = 1e-06
        elif mult is 'm' :
            multiplier = 1e-03
        elif mult is ' ' :
            multiplier = 1e0
        elif mult is 'k' :
            multiplier = 1e3
        elif mult is 'M' :
            multiplier = 1e6
        elif mult is 'G' :
            multiplier = 1e9
        elif mult is 'T' :
            multiplier = 1e12
        elif mult is 'P' :
            multiplier = 1e15

        num = multiplier * num

    return num

def toEngineeringNotation(num):
    #need to scanf the number
    if (is_number(num)):
        num = float(num)
    else:
        m = re.match('[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?',num)
        if(m):
            num = float(num)
            print( num)
        else:
            return num
    
    refdes="%9.3f%s"
    if(num == 0):
        return refdes % (num, "")

    #print( self.num)
    size = 6;
    precision = 3
    power = math.log10(abs(num))

    if(-15 <= power and power < -12): 
        multiplier=1e15
        suffix='f'
    elif(-12 <= power and power < -9): 
        multiplier=1e12
        suffix='p'
    elif(-9 <= power and power < -6): 
        multiplier=1e9
        suffix='n'
    elif(-6 <= power and power < -3): 
        multiplier=1e6
        suffix='u'
    elif(-3 <= power and power < -1): 
        multiplier=1e3
        suffix='m'
    elif(-1 <= power and power < 3): 
        multiplier=1
        suffix=''
    elif(3 <= power and power < 6): 
        multiplier=1e-3
        suffix='k'
    elif(6 <= power and power < 9): 
        multiplier=1e-6
        suffix='M'
    elif(9 <= power and power < 12): 
        multiplier=1e-9
        suffix='G'
    elif(12 <= power and power < 15): 
        multiplier=1e-12
        suffix='T'
    elif(15 <= power and power < 18): 
        multiplier=1e-15
        suffix='P'
    else:
        multiplier=1
        suffix=''

    refdes="%9.3f%s"
    return refdes % (num * multiplier, suffix)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def aoaPrint(aoa):
    table = []
    a = transpose(aoa)
    for col in a:
        width = columnWidth(col)
        refdes = "%%%ds" % width
        row = []
        for i,x in enumerate(col):
            row.append(refdes % x)
        table.append(row)

    b = transpose(table)
    for row in b:
        line = ""
        for col in row:
            line = line + col + " "
        print( line)

def aoa2csv(aoa):
    output = ""
    for row in aoa:
        output += ",".join(str(x) for x in row)
        output += "\n"
    return output

def aoa2String(aoa):
    str = ""
    table = []
    a = transpose(aoa)
    for col in a:
        width = columnWidth(col)
        refdes = "%%%ds" % width
        row = []
        for i,x in enumerate(col):
            row.append(refdes % x)
        table.append(row)

    b = transpose(table)
    for row in b:
        line = ""
        for col in row:
            line = line + col + " "
        str += line + "\n"
    return str

#passing a name and toggle=True makes a hidden table that appears when the 
# 'show_data' text is clicked.
def aoa2HtmlTable(aoa,name="",toggle=False):
    table = ""
    if toggle:
        table += "<p class=text>"
        table += "<a onclick=\"toggleItem('%s')\" >show data</a></p>\n" % name
        table += "<TABLE class=\"promistable\">"
        table += "<tbody id=\"%s\" style='display:none'>\n" % name
    else:
        table += "<TABLE class=\"promistable\"\><TBODY>\n"

    for i,row in list(enumerate(aoa)):
        if i == 0:
            table += makeHtmlTableRow(row,'TH')
        else:
            table += makeHtmlTableRow(row,'TD')

    return  table + "</TBODY></TABLE>"

def makeHtmlTableRow(row, cell_separator='TD'):
    txt = "<TR>"
    for cell in row:
        txt += "<%s>%s</%s>" % (cell_separator, cell, cell_separator)
    txt += "</TR>\n"
    return txt


#this flips an array along the y=-x direction so that info at 0,0 goes to the
#top right corner of the array.  calling it twice is equal to calling it 0 times
def transpose(aoa):
    if not aoa: return []
    return map(lambda *a: list(a), *aoa)

#finds the max length thing in a list so that the list can be printed as a
#column with a fixed width
def columnWidth(a):
    length=0
    for x in a:
        if(x == None): continue
        l = len("%s" % x)
        if(l > length): length = l
    return length

def errorPrint(refdes,message):
    msg = refdes % message
    colorCode = "\x1b[1;31m";
    #colorCode = "\e[1;31m"; #linux/pi style
    normCode = "\x1b[0m";
    #colorCode = "\e[1;31m"; #linux/pi style
    string = colorCode+msg+normCode
    print( string)

def warningPrint(refdes,message):
    msg = refdes % message
    colorCode = "\x1b[1;33m";
    #colorCode = "\e[1;31m"; #linux/pi style
    normCode = "\x1b[0m";
    #colorCode = "\e[1;31m"; #linux/pi style
    string = colorCode+msg+normCode
    print( string)


#30 black
#31 red
#32 green
#33 yellow
#34 blue
#35 magenta
#36 cyan
#37 white
