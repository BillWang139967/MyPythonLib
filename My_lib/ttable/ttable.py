#!/usr/bin/python
# coding=utf8
"""
# Author: meetbill
# Created Time : 2017-08-14 11:17:33
# last change  : 2017-09-03 13:44:25

# File Name:Ttable.py
# Description:

version: 1.0.1

"""
import sys
import os


class Ttable:
    def __init__(self, title, ccnt, defattr=""):
        #########################################
        # ttableframes 0(+-),1,2,3
        ttableframes = 0
        if ttableframes == 1:
            if sys.version_info[0] < 3:
                self.frames = ['\xe2\x94\x8f', '\xe2\x94\xb3', '\xe2\x94\x93', '\xe2\x94\xa3', '\xe2\x95\x8b', '\xe2\x94\xab', '\xe2\x94\x97',
                               '\xe2\x94\xbb', '\xe2\x94\x9b', '\xe2\x94\x81', '\xe2\x94\x83', '\xe2\x95\xb8', '\xe2\x95\xb9', '\xe2\x95\xba', '\xe2\x95\xbb', ' ']
            else:
                self.frames = ['\u250f', '\u2533', '\u2513', '\u2523', '\u254b', '\u252b', '\u2517',
                               '\u253b', '\u251b', '\u2501', '\u2503', '\u2578', '\u2579', '\u257a', '\u257b', ' ']
        elif ttableframes == 2:
            if sys.version_info[0] < 3:
                self.frames = ['\xe2\x94\x8c', '\xe2\x94\xac', '\xe2\x94\x90', '\xe2\x94\x9c', '\xe2\x94\xbc', '\xe2\x94\xa4', '\xe2\x94\x94',
                               '\xe2\x94\xb4', '\xe2\x94\x98', '\xe2\x94\x80', '\xe2\x94\x82', '\xe2\x95\xb4', '\xe2\x95\xb5', '\xe2\x95\xb6', '\xe2\x95\xb7', ' ']
            else:
                self.frames = ['\u250c', '\u252c', '\u2510', '\u251c', '\u253c', '\u2524', '\u2514',
                               '\u2534', '\u2518', '\u2500', '\u2502', '\u2574', '\u2575', '\u2576', '\u2577', ' ']
        elif ttableframes == 3:
            if sys.version_info[0] < 3:
                self.frames = ['\xe2\x95\x94', '\xe2\x95\xa6', '\xe2\x95\x97', '\xe2\x95\xa0', '\xe2\x95\xac', '\xe2\x95\xa3', '\xe2\x95\x9a',
                               '\xe2\x95\xa9', '\xe2\x95\x9d', '\xe2\x95\x90', '\xe2\x95\x91', ' ', '\xe2\x95\x91', ' ', '\xe2\x95\x91', ' ']
            else:
                self.frames = ['\u2554', '\u2566', '\u2557', '\u2560', '\u256c', '\u2563', '\u255a',
                               '\u2569', '\u255d', '\u2550', '\u2551', ' ', '\u2551', ' ', '\u2551', ' ']
        else:
            self.frames = ['+', '+', '+', '+', '+', '+', '+',
                           '+', '+', '-', '|', ' ', '|', ' ', '|', ' ']
        self.title = title
        self.ccnt = ccnt
        self.head = []
        self.body = []
        self.defattrs = []
        self.cwidth = []
        for i in range(ccnt):
            self.defattrs.append(defattr)
            self.cwidth.append(0)

        self.ttymode = 1
        if self.ttymode:
            try:
                import curses
                curses.setupterm()
                if curses.tigetnum("colors") >= 256:
                    colors256 = 1
                else:
                    colors256 = 0
            except Exception:
                colors256 = 1 if 'TERM' in os.environ and '256color' in os.environ['TERM'] else 0
            # colors: 0 - white,1 - red,2 - orange,3 - yellow,4 - green,5 -
            # cyan,6 - blue,7 - violet,8 - gray
            CSI = "\x1B["
            if colors256:
                self.ttyreset = CSI + "0m"
                self.colorcode = [CSI + "38;5;196m", CSI + "38;5;208m", CSI + "38;5;226m", CSI +
                                  "38;5;34m", CSI + "38;5;30m", CSI + "38;5;19m", CSI + "38;5;55m", CSI + "38;5;244m"]
            else:
                ttysetred = CSI + "31m"
                ttysetyellow = CSI + "33m"
                ttysetgreen = CSI + "32m"
                ttysetcyan = CSI + "36m"
                ttysetblue = CSI + "34m"
                ttysetmagenta = CSI + "35m"
                self.ttyreset = CSI + "0m"
                # no orange - use red, no gray - use white
                self.colorcode = [ttysetred, ttysetred, ttysetyellow,
                                  ttysetgreen, ttysetcyan, ttysetblue, ttysetmagenta, ""]
        else:
            self.colorcode = ["", "", "", "", "", "", "", ""]

    def combineattr(self, attr, defattr):
        attrcolor = ""
        for c in ("0", "1", "2", "3", "4", "5", "6", "7", "8"):
            if c in defattr:
                attrcolor = c
        for c in ("0", "1", "2", "3", "4", "5", "6", "7", "8"):
            if c in attr:
                attrcolor = c
        attrjust = ""
        for c in ("l", "L", "r", "R", "c", "C"):
            if c in defattr:
                attrjust = c
        for c in ("l", "L", "r", "R", "c", "C"):
            if c in attr:
                attrjust = c
        return attrcolor + attrjust

    def header(self, *rowdata):
        ccnt = 0
        for celldata in rowdata:
            if isinstance(celldata, tuple):
                if len(celldata) == 3:
                    ccnt += celldata[2]
                else:
                    if celldata[0] is not None:
                        cstr = str(celldata[0])
                        if len(cstr) > self.cwidth[ccnt]:
                            self.cwidth[ccnt] = len(cstr)
                    ccnt += 1
            else:
                if celldata is not None:
                    cstr = str(celldata)
                    if len(cstr) > self.cwidth[ccnt]:
                        self.cwidth[ccnt] = len(cstr)
                ccnt += 1
        if ccnt != self.ccnt:
            raise IndexError
        self.head.append(rowdata)

    def defattr(self, *rowdata):
        if len(rowdata) != self.ccnt:
            raise IndexError
        self.defattrs = rowdata

    def append(self, *rowdata):
        ccnt = 0
        rdata = []
        for celldata in rowdata:
            if isinstance(celldata, tuple):
                if celldata[0] is not None:
                    cstr = str(celldata[0])
                else:
                    cstr = ""
                if len(celldata) == 3:
                    rdata.append((cstr, self.combineattr(
                        celldata[1], self.defattrs[ccnt]), celldata[2]))
                    ccnt += celldata[2]
                else:
                    if len(cstr) > self.cwidth[ccnt]:
                        self.cwidth[ccnt] = len(cstr)
                    if len(celldata) == 2:
                        rdata.append((cstr, self.combineattr(
                            celldata[1], self.defattrs[ccnt])))
                    else:
                        rdata.append((cstr, self.defattrs[ccnt]))
                    ccnt += 1
            else:
                if celldata is not None:
                    cstr = str(celldata)
                    if len(cstr) > self.cwidth[ccnt]:
                        self.cwidth[ccnt] = len(cstr)
                    rdata.append((cstr, self.defattrs[ccnt]))
                else:
                    rdata.append(celldata)
                ccnt += 1
        if ccnt != self.ccnt:
            raise IndexError
        self.body.append(rdata)

    def attrdata(self, cstr, cattr, cwidth):
        retstr = ""
        #######################################
        colorcode = self.colorcode
        if "1" in cattr:
            retstr += colorcode[0]
            needreset = 1
        elif "2" in cattr:
            retstr += colorcode[1]
            needreset = 1
        elif "3" in cattr:
            retstr += colorcode[2]
            needreset = 1
        elif "4" in cattr:
            retstr += colorcode[3]
            needreset = 1
        elif "5" in cattr:
            retstr += colorcode[4]
            needreset = 1
        elif "6" in cattr:
            retstr += colorcode[5]
            needreset = 1
        elif "7" in cattr:
            retstr += colorcode[6]
            needreset = 1
        elif "8" in cattr:
            retstr += colorcode[7]
            needreset = 1
        else:
            needreset = 0
        if cstr == "--":
            retstr += " " + "-" * cwidth + " "
        elif cstr == "---":
            retstr += "-" * (cwidth + 2)
        elif "L" in cattr or "l" in cattr:
            retstr += " " + cstr.ljust(cwidth) + " "
        elif "R" in cattr or "r" in cattr:
            retstr += " " + cstr.rjust(cwidth) + " "
        else:
            retstr += " " + cstr.center(cwidth) + " "
        if needreset:
            retstr += self.ttyreset
        return retstr

    def lines(self):
        outstrtab = []
        ####################################
        plaintextseparator = "\t"
        if self.ttymode:
            tabdata = []
            # upper frame
            tabdata.append((("---", "", self.ccnt),))
            # title
            tabdata.append(((self.title, "", self.ccnt),))
            # header
            if len(self.head) > 0:
                tabdata.append((("---", "", self.ccnt),))
                tabdata.extend(self.head)
            # head and data separator
            tabdata.append((("---", "", self.ccnt),))
            # data
            if len(self.body) == 0:
                tabdata.append((("no data", "", self.ccnt),))
            else:
                tabdata.extend(self.body)
            # bottom frame
            tabdata.append((("---", "", self.ccnt),))
            # check col-spaned headers and adjust column widths if necessary
            for rowdata in tabdata:
                ccnt = 0
                for celldata in rowdata:
                    if isinstance(celldata, tuple) and len(
                            celldata) == 3 and celldata[0] is not None:
                        cstr = str(celldata[0])
                        clen = len(cstr)
                        cwidth = sum(
                            self.cwidth[ccnt:ccnt + celldata[2]]) + 3 * (celldata[2] - 1)
                        if clen > cwidth:
                            add = clen - cwidth
                            adddm = divmod(add, celldata[2])
                            cadd = adddm[0]
                            if adddm[1] > 0:
                                cadd += 1
                            for i in range(celldata[2]):
                                self.cwidth[ccnt + i] += cadd
                        ccnt += celldata[2]
                    else:
                        ccnt += 1
            separators = []
            # before tab - no separators
            seplist = []
            for i in range(self.ccnt + 1):
                seplist.append(0)
            separators.append(seplist)
            for rowdata in tabdata:
                seplist = [1]
                for celldata in rowdata:
                    if isinstance(celldata, tuple) and len(celldata) == 3:
                        for i in range(celldata[2] - 1):
                            seplist.append(1 if celldata[0] == '---' else 0)
                    seplist.append(1)
                separators.append(seplist)
            # after tab - no separators
            seplist = []
            for i in range(self.ccnt + 1):
                seplist.append(0)
            separators.append(seplist)
            # add upper and lower separators:
            updownsep = [[a * 2 + b for (a, b) in zip(x, y)]
                         for (x, y) in zip(separators[2:], separators[:-2])]
            # create ttable
            for (rowdata, sepdata) in zip(tabdata, updownsep):
                #				print rowdata,sepdata
                ccnt = 0
                line = ""
                nsep = 0  # self.frames[10]
                for celldata in rowdata:
                    cpos = ccnt
                    cattr = ""
                    if isinstance(celldata, tuple):
                        if celldata[1] is not None:
                            cattr = celldata[1]
                        if len(celldata) == 3:
                            cwidth = sum(
                                self.cwidth[ccnt:ccnt + celldata[2]]) + 3 * (celldata[2] - 1)
                            ccnt += celldata[2]
                        else:
                            cwidth = self.cwidth[ccnt]
                            ccnt += 1
                        cstr = celldata[0]
                    else:
                        cstr = celldata
                        cwidth = self.cwidth[ccnt]
                        ccnt += 1
                    if cstr is None:
                        cstr = ""
                    if not isinstance(cstr, str):
                        cstr = str(cstr)
                    if cstr == "---":
                        if nsep == 0:
                            line += self.frames[(13, 6, 0, 3)[sepdata[cpos]]]
                            #line += self.frames[(15,6,0,3)[sepdata[cpos]]]
                        else:
                            line += self.frames[(9, 7, 1, 4)[sepdata[cpos]]]
                        nsep = 1  # self.frames[4]
                        for ci in range(cpos, ccnt - 1):
                            line += self.frames[9] * (self.cwidth[ci] + 2)
                            line += self.frames[(9, 7, 1, 4)[sepdata[ci + 1]]]
                        line += self.frames[9] * (self.cwidth[ccnt - 1] + 2)
                    else:
                        if nsep == 0:
                            line += self.frames[(15, 12, 14, 10)
                                                [sepdata[cpos]]]
                            #line += self.frames[(15,10,10,10)[sepdata[cpos]]]
                        else:
                            line += self.frames[(11, 8, 2, 5)[sepdata[cpos]]]
                            #line += self.frames[(15,8,2,5)[sepdata[cpos]]]
                        nsep = 0
                        line += self.attrdata(cstr, cattr, cwidth)
                if nsep == 0:
                    line += self.frames[(15, 12, 14, 10)[sepdata[ccnt]]]
                    #line += self.frames[(15,10,10,10)[sepdata[ccnt]]]
                else:
                    line += self.frames[(11, 8, 2, 5)[sepdata[ccnt]]]
                    #line += self.frames[(15,8,2,5)[sepdata[ccnt]]]
                outstrtab.append(line)
        else:
            for rowdata in self.body:
                row = []
                for celldata in rowdata:
                    if isinstance(celldata, tuple):
                        cstr = str(celldata[0])
                    elif celldata is not None:
                        cstr = str(celldata)
                    else:
                        cstr = ""
                    row.append(cstr)
                outstrtab.append("%s:%s%s" % (
                    self.title, plaintextseparator, plaintextseparator.join(row)))
        return outstrtab

    def __str__(self):
        return "\n".join(self.lines())


if __name__ == "__main__":
    x = Ttable("Test title", 4)
    x.header("column1", "column2", "column3", "column4")
    x.append("t1", "t2", "very long entry", "test")
    x.append(("r", "r3"), ("l", "l2"), "also long entry", "test")
    print x

    x = Ttable("Very long ttable title", 2)
    x.defattr("l", "r")
    x.append("key", "value")
    x.append("other key", 123)
    y = []
    y.append(("first", "1"))
    y.append(("second", "4"))
    x.append(*y)
    print x

    x = Ttable("ttable with complicated header", 14, "r")
    x.header(("", "", 3), ("I/O stats last min", "", 8), ("", "", 3))
    x.header(("info", "", 3), ("---", "", 8), ("space", "", 3))
    x.header(("", "", 3), ("transfer", "", 2),
             ("max time", "", 3), ("# of ops", "", 3), ("", "", 3))
    x.header(("---", "", 14))
    x.header("IP", "last error", "status", "read", "write", "read", "write",
             "fsync", "read", "write", "fsync", "used", "total", "used %")
    x.append("192.168.1.1", "no errors", "ok", "19 MiB/s", "27 MiB/s", "263625 us",
             "43116 us", "262545 us", 3837, 3295, 401, "1.0 TiB", "1.3 TiB", "76.41%")
    x.append("192.168.1.2", "no errors", "ok", "25 MiB/s", "29 MiB/s", "340303 us",
             "89168 us", "223610 us", 2487, 2593, 366, "1.0 TiB", "1.3 TiB", "75.93%")
    x.append("192.168.1.3", ("2012-10-12 07:27", "2"), ("damaged", "1"), "-",
             "-", "-", "-", "-", "-", "-", "-", "1.2 TiB", "1.3 TiB", "87.18%")
    x.append("192.168.1.4", "no errors", ("marked for removal", "4"), "-",
             "-", "-", "-", "-", "-", "-", "-", "501 GiB", "1.3 TiB", "36.46%")
    x.append("192.168.1.5", "no errors", "ok", "17 MiB/s", "11 MiB/s", "417292 us",
             "76333 us", "1171903 us", "2299", "2730", "149", "1.0 TiB", "1.3 TiB", "76.61%")
    print x

    x = Ttable("Colors", 1, "r")
    x.append(("white", "0"))
    x.append(("red", "1"))
    x.append(("orange", "2"))
    x.append(("yellow", "3"))
    x.append(("green", "4"))
    x.append(("cyan", "5"))
    x.append(("blue", "6"))
    x.append(("magenta", "7"))
    x.append(("gray", "8"))
    print x

    x = Ttable("Adjustments", 1)
    x.append(("left", "l"))
    x.append(("right", "r"))
    x.append(("center", "c"))
    print x

    x = Ttable("Special entries", 3)
    x.defattr("l", "r", "r")
    x.header("entry", "effect", "extra column")
    x.append("-- ", "--", "")
    x.append("--- ", "---", "")
    x.append("('--','',2)", ('--', '', 2))
    x.append("('','',2)", ('', '', 2))
    x.append("('---','',2)", ('---', '', 2))
    x.append("('red','1')", ('red', '1'), '')
    x.append("('orange','2')", ('orange', '2'), '')
    x.append("('yellow','3')", ('yellow', '3'), '')
    x.append("('green','4')", ('green', '4'), '')
    x.append("('cyan','5')", ('cyan', '5'), '')
    x.append("('blue','6')", ('blue', '6'), '')
    x.append("('magenta','7')", ('magenta', '7'), '')
    x.append("('gray','8')", ('gray', '8'), '')
    x.append(('---', '', 3))
    x.append("('left','l',2)", ('left', 'l', 2))
    x.append("('right','r',2)", ('right', 'r', 2))
    x.append("('center','c',2)", ('center', 'c', 2))
    print x

    # loop
    x = Ttable("host info", 2)
    x.defattr("l", "l")
    x.header("host_group", "host")
    elements = {
        "host_group1": ["127.0.0.1", "127.0.0.2", "127.0.0.3"],
        "host_group2": ["127.0.0.1", "127.0.0.2"]
    }
    lastpos = len(elements) - 1
    for i, host_group in enumerate(elements):
        ip_list = elements[host_group]
        for j, ip in enumerate(ip_list):
            # 填充数据
            if j == 0:
                x.append(host_group, ip)
            else:
                x.append("", ip)
            # 分割线
            if j < (len(ip_list) - 1):
                x.append("", "---")
        # 分割线
        if i < lastpos:
            x.append("---", "---")
    print x
