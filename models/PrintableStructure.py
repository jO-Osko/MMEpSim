#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PrintableStructure
"""

__author__ = "Filip Koprivec"
__email__ = "koprivec.filip+template@gmail.com"

from typing import Iterable

"""
Moj standardno uporabljan objekt za razhroščevanje in lepši izpis uporabniško definiranih objektov
"""


class PrintableStructure:
    # Object methods
    __printable_fields__ = ()  # type: Iterable[str]
    __printable_name__ = "PrintableStructure"
    _formatter = "{name}({data})"

    __slots__ = ()  # type: Iterable[str]

    def _str_fields(self) -> str:
        return ", ".join(map(lambda x: repr(self.__getattribute__(x)), self.__printable_fields__))

    def _str_pairs(self) -> str:
        return ", ".join(map(lambda x: x + "=" + repr(self.__getattribute__(x)), self.__printable_fields__))

    def pp(self) -> str:
        return self._formatter.format(name=self.__printable_name__, data=self._str_pairs())

    def __repr__(self) -> str:
        return self._formatter.format(name=self.__printable_name__, data=self._str_fields())

    # For convenience
    def __str__(self) -> str:
        return self.__repr__()
