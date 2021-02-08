from typing import Dict, Any, Callable
from xml.etree.ElementTree import Element


class Int:
    def __call__(self, elem: Element):
        return int(elem.text)


class Float:
    def __call__(self, elem: Element):
        return float(elem.text)


class Str:
    def __call__(self, elem: Element):
        return elem.text


class Coordinates:
    def __call__(self, elem: Element):
        x, y = elem.text.split(',')
        return {'x': int(x), 'y': int(y)}


class Rectangle:
    def __call__(self, elem: Element):
        point0, point1 = elem.text.split(':')
        point00, point01 = point0.split(',')
        point10, point11 = point1.split(',')
        return {'x0y0': int(point00), 'x0y1': int(point01), 'x1y0': int(point10), 'x1y1': int(point11)}


class Entity:
    def __init__(self,
                 main_fields: Dict[str, Callable[[Element], None]],
                 multiple_fields: Dict[str, Callable[[Element], None]]):
        self._main_fields = main_fields
        self._multiple_fields = multiple_fields

    def __call__(self, elem: Element) -> Dict[str, Any]:
        j_obj = {}
        sub_cols = {}
        for child in elem:  # type: Element
            tag = child.tag
            if tag in self._main_fields:
                j_obj[tag] = self._main_fields[tag](child)
            else:
                sub_cols[tag] = child.text
        if len(sub_cols) > 0:
            for name, value in sub_cols.items():
                print('*** Missing def', elem.tag, name)
        return j_obj


class List:
    def __init__(self, elem: Entity):
        self._elem = elem

    def __call__(self, elem: Element):
        entities = []
        for child in elem:  # type: Element
            entities.append(self._elem(child))
        return entities
