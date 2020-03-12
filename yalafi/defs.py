#
#   YaLafi: Yet another LaTeX filter
#   Copyright (C) 2020 Matthias Baumann
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

class Printable:
    def __repr__(self):
        vars = list(v for v in dir(self) if not v.startswith('_'))
        vars.sort()
        def get(v):
            return self.__getattribute__(v)
        is_not_list = list(v + '=' + repr(get(v)) for v in vars
                                    if type(get(v)) is not list)
        is_list = list(v + '=' + repr(get(v)) for v in vars
                                    if type(get(v)) is list)
        cls = self.__class__.__name__
        return cls + '(' + ', '.join(is_not_list + is_list) + ')'

class TextToken(Printable):
    def __init__(self, pos, txt):
        self.pos = pos
        self.txt = txt
        self.pos_fix = False

class SpaceToken(TextToken):
    def __init__(self, pos, txt):
        super().__init__(pos, txt)

class ParagraphToken(TextToken):
    def __init__(self, pos, txt):
        super().__init__(pos, txt)

class CommentToken(TextToken):
    def __init__(self, pos, txt):
        super().__init__(pos, txt)

class SpecialToken(TextToken):
    def __init__(self, pos, txt):
        super().__init__(pos, txt)

class MacroToken(TextToken):
    def __init__(self, pos, txt):
        super().__init__(pos, txt)

class AccentToken(TextToken):
    def __init__(self, pos, txt):
        super().__init__(pos, txt)

class VerbatimToken(TextToken):
    def __init__(self, pos, txt):
        super().__init__(pos, txt)

class ArgumentToken(TextToken):
    def __init__(self, pos, txt, arg):
        super().__init__(pos, txt)
        self.arg = arg

class ActionToken(TextToken):
    def __init__(self, pos):
        super().__init__(pos, '')

class VoidToken(TextToken):
    def __init__(self, pos):
        super().__init__(pos, '')

class Macro(Printable):
    def __init__(self, name, args='', repl='', opts=[], scanned=False):
        self.name = name
        self.args = args
        if scanned:
            self.repl = repl
            self.opts = opts
            return
        if callable(repl):
            self.repl = repl
        else:
            self.repl = scanner.Scanner(repl).all()
        self.opts = []
        for op in opts:
            self.opts.append(scanner.Scanner(op).all())

