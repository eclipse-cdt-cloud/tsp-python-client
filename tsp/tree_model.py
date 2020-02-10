# The MIT License (MIT)
#
# Copyright (C) 2020 - Ericsson
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


class TreeModel(object):

    def __init__(self, entries):
        id_map = {}
        orphands = []
        self._root = None
        for entry in entries:
            if entry.parent_id != -1:
                if (entry.id in id_map.keys()):
                    elem = id_map[entry.id]
                    elem.set_entry(entry)
                else:
                    elem = TreeItem(entry)
                    if (entry.parent_id in id_map.keys()):
                        parent = id_map[entry.parent_id]
                        parent.add_child(elem)
                    else:
                        orphands.append(elem)
                    id_map[entry.id] = elem
            else:
                if (entry.id in id_map.keys()):
                    elem = id_map[entry.id]
                    elem.set_entry(entry)
                else:
                    elem = TreeItem(entry)
                    elem.set_trace("TODO")
                    id_map[entry.id] = elem
                    self._root = elem

        for orphand in orphands:
            if orphand.get_entry().parent_id in id_map.keys():
                parent = id_map[orphand.get_entry().parent_id]
                parent.add_child(orphand)

    def print(self):
        self._root.print()


class TreeItem(object):
    def __init__(self, entry=None):
        self._entry = entry
        self._parent = None
        self._children = []
        self._trace = None

    def set_parent(self, parent):
        self._parent = parent

    def get_parent(self):
        return self._parent

    def set_entry(self, entry):
        self._entry = entry

    def get_entry(self):
        return self._entry

    def set_trace(self, trace):
        self._trace = trace

    def add_child(self, child):
        self._children.append(child)

    def get_children(self):
        return self._children

    def print(self, depth=0):
        for x in range(depth):
            print("", end=" ")
        if self._entry is not None:
            other = ""
            others = self._entry.others
            prefix = ""
            if depth > 0:
                prefix = "|- "
            # TODO print TimeGraphEntry specific fields
            for k in others:
                other = ('{0} ({1}, {2})'.format(other, k, others.get(k)))
            print("{0}{1} ({1}, {2}) {3} {4}".format(prefix, self._entry.labels[0], self._entry.id, self._entry.parent_id, other))
        for child in self.get_children():
            child.print(depth + 4)
