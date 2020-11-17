#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   transform.py
@Time    :   2020/11/17 15:32:59
@Author  :   Kyle Wang
@Version :   1.0
@Contact :   wrk15835@gmail.com
@License :   (C)Copyright 2020-2021, Kyle Wang
@Desc    :   None
'''

import os
import subprocess
import re

from subprocess import PIPE
from conf import *
from util import *


class Line(object):

    def __init__(self, lineno=0, text='', color=-1):
        self.lineno = lineno 
        self.text = text
        self.color = color      # the index of color, -1 when no need to colorize

class Document(object):

    """
    document are a lists of lines
    """

    def __init__(self, lines = [], docbegin=None, docend=None, file="", 
                    commits=[], outfile=""):
        self.lines = lines
        self.docbegin = docbegin
        self.docend = docend
        self.file = file
        self.lines = lines
        self.commits = commits

        self.path = ""        # the directory containing the file
        self.outfile = outfile
        self.active = False
        self.envstack = []

    def clear(self):
        self.lines.clear()
        self.commits.clear()
        self.docbegin = None 
        self.docend = None
        self.active = False 

    def load(self, filename=""):
        self.clear()
        lines = self.lines 

        if not os.path.exists(filename):
            raise OSError(filename + " does not exist")

        self.path = os.path.dirname(filename)
        self.file = filename

        if not self.outfile:
            self.outfile = os.path.join(self.path, "target/" + os.path.basename(filename))

        self.load_commits()
        
        with open(filename, 'r', encoding='utf-8') as f:
            for lineno, line in enumerate(f):
                text = line[:-1]        # ignore the '\n' at the end
                newline = Line(lineno+1, text)
                lines.append(newline)

        # identify the line containing \begin{document}
        self.update_lineno()
        
        # identify the line containing \end{document}
        if not self.docbegin:
            raise TransformError("\\begin{document} not found")

        if not self.docend:
            raise TransformError("\\end{document} not found")

    def load_commits(self):
        if not self.path:
            raise OSError 
            
        if not os.path.exists(os.path.join(self.path, ".git")):
            return 
        
        self.active = True
        cmd = "git log --pretty=oneline"
        r = subprocess.run(args=cmd, cwd=self.path, shell=True, check=True, stdout=PIPE, encoding='utf-8')
        commits = r.stdout.split('\n')

        for commit in commits:
            if commit:
                self.commits.append(commit)

        if LEVEL < len(self.commits):
            self.commits = self.commits[:LEVEL]


    def mark(self):
        if not self.active:
            return 
        for line in self.lines[self.docbegin.lineno:self.docend.lineno-1]:
            self.mark_line(line)

    def mark_line(self, line):
        """"""
        text = line.text.lstrip()
        if text.startswith('\\begin{'):

            text = text[7:]
            for env in SKIP_ENVS:
                if text.startswith(env):
                    self.envstack.append(line)
                    return 

        if text.startswith('\\end{'):
            text = text[5:]
            for env in SKIP_ENVS:
                if text.startswith(env):
                    self.envstack.pop()
                    return 

        if self.envstack:       # we are inside some environment
            return 


        ### skip the blank lines 
        ### and the comments 

        if line.text.startswith("%"):
            return 

        if text.startswith("\\"):
            return 

        if not text:
            return 


        cmd = "git blame -L %d,%d samplepaper.tex --full-history --pretty=oneline --date-order --skip=0 --max-count=10" % (line.lineno, line.lineno)
        
        r = subprocess.run(args=cmd, cwd=self.path, shell=True, check=True, stdout=PIPE, encoding='utf-8')
        lines = r.stdout.split('\n')
        
        commit = lines[0]
        if commit.startswith("^"):
            commit = commit[1:]
        commit = commit[:7]

        for i,c in enumerate(self.commits):
            if c.startswith(commit):
                line.color = i
                break 



    def output(self):
        outfile = self.outfile
        outpath = os.path.dirname(outfile)
        if not os.path.exists(outpath):
            os.mkdir(outpath)
        
        strings = [line.text for line in self.lines]
        with open(self.outfile, "w", encoding="utf-8") as f:
            f.write("\n".join(strings))

    def insert_colors(self):
        """
        insert colors before the `\\begin{document}`
        """

        split = self.docbegin.lineno - 1
        lines = self.lines 
        length = len(self.commits)

        for key, val in zip(COLOR_KEYS[:length], COLOR_VALS[:length]):
            colordef = "\\definecolor{%s}{HTML}{%s}" % (key, val)
            line = Line(text=colordef)
            lines.insert(split, line)


        # if xcolor is not used, add it
        has_xcolor = False
        for line in lines:
            text = line.text.lstrip() 
            if text.startswith('\\usepackage{xcolor}'):
                has_xcolor = True 
                break 
        
        if not has_xcolor:
            line = Line(text='\\usepackage{xcolor}')
            lines.insert(split, line)

        self.update_lineno()
        
    def update_lineno(self):
        for i, line in enumerate(self.lines):
            line.lineno = i+1

            res = re.search("\\\\begin\{document\}", line.text)
            if res:
                self.docbegin = line 

            res = re.search("\\\\end\{document\}", line.text)
            if res:
                self.docend = line 
    
    def colorize(self):
        self.insert_colors()
        for line in self.lines[self.docbegin.lineno:self.docend.lineno-1]:
            self.colorize_line(line)


    def colorize_line(self, line):
        text = line.text 
        color = line.color 
        if color == -1:
            return              # no need to modify 
        
        newtext = "\\color{%s} %s \\color{black}" % (COLOR_KEYS[color], text)
        line.text = newtext

class TransformError(Exception):
    pass
