#!/usr/bin/env python
"""
Copyright (c) 2014, katonori All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are
permitted provided that the following conditions are met:

  1. Redistributions of source code must retain the above copyright notice, this list
     of conditions and the following disclaimer.
  2. Redistributions in binary form must reproduce the above copyright notice, this
     list of conditions and the following disclaimer in the documentation and/or other
     materials provided with the distribution.
  3. Neither the name of the katonori nor the names of its contributors may be used to
     endorse or promote products derived from this software without specific prior
     written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
DAMAGE.
"""
import re, sys, commands, getopt, os

CXXFILT = "c++filt"

class CmdNm():
    def Run(self, lib, word, isDemangle):
        cmd = "nm " + lib
        if isDemangle != 0:
            cmd += " | " + CXXFILT
        (rv, out) = commands.getstatusoutput(cmd)
        if rv != 0:
            print "ERROR while executing command: " + cmd
            print out
        objName = ""
        for l in out.split("\n"):
            m = re.match(r"^(\S+):", l)
            if m:
                objName = m.group(1)
            else:
                m = re.search(word, l)
                if m:
                    print "%s: %s: "%(lib, objName),
                    print l

class CmdReadElf():
#    Num:    Value          Size Type    Bind   Vis      Ndx Name
# 49: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND _ZN21WPXPropertyListVecto
    def Run(self, lib, word, isDemangle):
        cmd = "readelf -s -W " + lib
        if isDemangle != 0:
            cmd += " | " + CXXFILT
        (rv, out) = commands.getstatusoutput(cmd)
        if rv != 0:
            print "ERROR while executing command: " + cmd
            print out
        objName = ""
        for l in out.split("\n"):
            row = re.split("\s+", l)
            try:
                row.remove("")
            except ValueError as e:
                pass
            if len(row) == 8:
                ndx = row[6]
                name = row[7]
                if ndx != "UND":
                    m = re.search(word, name)
                    if m:
                        print "%s: %s: "%(lib, objName),
                        print l
def usage():
    print "usage: %s [-nC] word file0 [file1 ...]"%(os.path.basename(sys.argv[0]))

def search_symbol(isDemangle, cmdClass):
    # check if c++filt exists
    if isDemangle != 0:
        (rv, out) = commands.getstatusoutput("which " + CXXFILT)
        if rv != 0:
            print('ERRRO: %s not found. The option "-C" uses %s'%(CXXFILT, CXXFILT))
            sys.exit(1)

    word = argv[0]
    for lib in argv[1:]:
        cmdClass.Run(lib, word, isDemangle)

if __name__ == "__main__":
    if len(sys.argv) <= 2:
        usage()
        sys.exit(1)

    isDemangle = 0
    cmdClass = None

    try:
        opts, argv = getopt.getopt(sys.argv[1:], "Cn", [])
    except getopt.GetoptError:
        usage()
        sys.exit(1)
    for o, a in opts:
        if o == "-C":
            isDemangle = 1
        elif o == "-n":
            cmdClass = CmdNm()
    if cmdClass == None:
        cmdClass = CmdReadElf()
    search_symbol(isDemangle, cmdClass)
