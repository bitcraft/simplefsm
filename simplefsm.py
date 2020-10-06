""" Small FSM Implementation

https://github.com/bitcraft/simplefsm

Copyright (c) 2018-2020 Leif Theden

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from collections import namedtuple

Event = namedtuple('Event', 'name src dst event')
Event.__new__.__defaults__ = (None, None, None, None)


class SimpleFSM:
    def __init__(self, events, initial=None):
        self.state = initial
        self.graph = dict()
        self.program(events)

    def program(self, events):
        for in_event, src, dst, out_event in (Event(*i) for i in events):
            trans = self.graph.setdefault(in_event, dict())
            if type(out_event) == str:
                out_event = [out_event]
            trans[src] = dst, out_event

    def __call__(self, event):
        src = self.state
        graph = self.graph
        try:
            state, out = ((src in graph[event] and graph[event][src]) or
                          ('*' in graph[event] and graph[event]['*']) or
                          (graph['ThisIsMostCertainlyNotHandled!1']))
        except KeyError:
            try:
                state, out = graph['*'][src]
            except KeyError:
                raise ValueError(event, self.state)

        self.state = src if state == '=' else state
        return self.state, out
