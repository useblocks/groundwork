"""Docstring parser implementation.

Copyright: Marcin Kurczewski (rr-)
Source: https://github.com/rr-/docstring_parser
License: MIT
Used commit/stand: efda62e

Changes:

 * Added support for sphinx like docstring regarding type definition
 * Removed type annotations to work with Python 2.x
"""

import inspect
import re


class ParseError(RuntimeError):
    """Base class for all parsing related errors."""
    pass


class DocstringMeta:
    """
    Docstring meta information.

    Symbolizes lines in form of

        :param arg: description
        :raises ValueError: if something happens
    """
    def __init__(self, args, description, type=None):
        """
        Initialize self.

        :param args: list of arguments before delimiting colon.
        :param description: associated docstring description.
        """
        self.args = args
        self.description = description
        self._type = type

    @classmethod
    def from_meta(cls, meta, meta_all=None):
        """Copy DocstringMeta from another instance."""
        if len(meta.args) == 2:
            name = meta.args[1]
            meta_type = None
            for x in meta_all:
                if x.args[1] == name and x.args[0] == 'type':
                    meta_type = x.description
                    break

            return cls(args=meta.args, description=meta.description, type=meta_type)
        else:
            return cls(args=meta.args, description=meta.description)


class DocstringTypeMeta(DocstringMeta):
    """Docstring meta whose only optional arg contains type information."""

    @property
    def type_name(self):
        """Return type name associated with given docstring metadata."""
        return self.args[1] if len(self.args) > 1 else None


class DocstringParam(DocstringMeta):
    """DocstringMeta symbolizing :param metadata."""

    @property
    def arg_name(self):
        """Return argument name associated with given param."""
        if len(self.args) > 2:
            return self.args[2]
        elif len(self.args) > 1:
            return self.args[1]
        return None

    @property
    def type_name(self):
        """Return type name associated with given param."""
        if len(self.args) > 2:
            return self.args[1]
        else:
            return self._type
        return


class DocstringReturns(DocstringTypeMeta):
    """DocstringMeta symbolizing :returns metadata."""

    pass


class DocstringRaises(DocstringTypeMeta):
    """DocstringMeta symbolizing :raises metadata."""

    pass


class Docstring:
    """Docstring object representation."""

    def __init__(self):
        """Intializes self."""
        self.short_description = None
        self.long_description = None
        self.blank_after_short_description = False
        self.blank_after_long_description = False
        self.meta = []

    @property
    def params(self):
        """Return list of :param meta."""
        return [
            DocstringParam.from_meta(meta, self.meta)
            for meta in self.meta
            if meta.args[0] in {
                'param', 'parameter', 'arg', 'argument', 'key', 'keyword'
            }
        ]

    @property
    def raises(self):
        """Return list of :raises meta."""
        return [
            DocstringRaises.from_meta(meta)
            for meta in self.meta
            if meta.args[0] in {'raises', 'raise', 'except', 'exception'}
        ]

    @property
    def returns(self):
        """Return :returns meta, if available."""
        try:
            return next(
                DocstringReturns.from_meta(meta)
                for meta in self.meta
                if meta.args[0] in {'return', 'returns'}
            )
        except StopIteration:
            return None


def parse(text):
    """
    Parse the docstring into its components.

    :returns: parsed docstring
    """
    ret = Docstring()
    if not text:
        return ret

    text = inspect.cleandoc(text)
    match = re.search('^:', text, flags=re.M)
    if match:
        desc_chunk = text[:match.start()]
        meta_chunk = text[match.start():]
    else:
        desc_chunk = text
        meta_chunk = ''

    parts = desc_chunk.split('\n', 1)
    ret.short_description = parts[0] or None
    if len(parts) > 1:
        long_desc_chunk = parts[1] or ''
        ret.blank_after_short_description = long_desc_chunk.startswith('\n')
        ret.blank_after_long_description = long_desc_chunk.endswith('\n\n')
        ret.long_description = long_desc_chunk.strip() or None

    for match in re.finditer(
            r'(^:.*?)(?=^:|\Z)', meta_chunk, flags=re.S | re.M
    ):
        chunk = match.group(0)
        if not chunk:
            continue
        try:
            args_chunk, desc_chunk = chunk.lstrip(':').split(':', 1)
        except ValueError:
            raise ParseError(
                'Error parsing meta information near "{}".'.format(chunk)
            )
        args = args_chunk.split()
        desc = desc_chunk.strip()
        if '\n' in desc:
            first_line, rest = desc.split('\n', 1)
            desc = first_line + '\n' + inspect.cleandoc(rest)
        ret.meta.append(DocstringMeta(args, description=desc, type=None))

    return ret
