from abc import ABC, abstractmethod
from typing import Dict, Any
from xml.etree.ElementTree import Element


class ParsingType(ABC):
    @abstractmethod
    def parse(self, elem: Element, *, parent_fields: Dict[str, Any] = None):
        pass

    @abstractmethod
    def merge(self, origin, override):
        pass


class Bool(ParsingType):
    def parse(self, *args, **kwargs):
        return True

    def merge(self, origin, override):
        return True


class Int(ParsingType):
    def parse(self, elem: Element, **kwargs):
        return int(elem.text)

    def merge(self, origin, override):
        return override


class Float(ParsingType):
    def parse(self, elem: Element, **kwargs):
        return float(elem.text)

    def merge(self, origin, override):
        return override


class Str(ParsingType):
    def parse(self, elem: Element, **kwargs):
        return elem.text

    def merge(self, origin, override):
        return override


class Population(ParsingType):
    def parse(self, elem: Element, **kwargs):
        race, population = elem.text.split(':')
        return {'race': race, 'population': int(population)}

    def merge(self, origin, override):
        return override


class Coordinates(ParsingType):
    def parse(self, elem: Element, **kwargs):
        if '|' in elem.text:
            raise ValueError()
        x, y = elem.text.split(',')
        return {'x': int(x), 'y': int(y)}

    def merge(self, origin, override):
        return override


class Path(ParsingType):
    def __init__(self, *, points: int = 2):
        self._points = points
        if points > 3:
            self._origin_point = ord('a')
        else:
            self._origin_point = ord('x')

    def parse(self, elem: Element, **kwargs):
        ord_a = ord('a')
        path = []
        for coord in elem.text.split('|'):
            if coord:
                points = coord.split(',')
                coords = {}
                for index in range(len(points)):
                    coords[chr((self._origin_point - ord_a + index) % 26 + ord_a)] = int(points[index])
                path.append(coords)
        return path

    def merge(self, origin, override):
        return override


class Rectangle(ParsingType):
    def parse(self, elem: Element, **kwargs):
        point0, point1 = elem.text.split(':')
        point00, point01 = point0.split(',')
        point10, point11 = point1.split(',')
        return {'x0y0': int(point00), 'x0y1': int(point01), 'x1y0': int(point10), 'x1y1': int(point11)}

    def merge(self, origin, override):
        return override


class Entity(ParsingType):
    def __init__(self, merge_id: str, fields: Dict[str, ParsingType], *, transforms: Dict[str, str] = None):
        self._merge_id = merge_id
        self._fields = fields
        self._transforms = transforms

    @property
    def merge_id(self):
        return self._merge_id

    def parse(self, elem: Element, **kwargs):
        fields = {}
        for child in elem:  # type: Element
            tag = child.tag
            if self._transforms is not None and tag in self._transforms:
                tag = self._transforms[tag]
            if tag in self._fields:
                res = self._fields[tag].parse(child, parent_fields=fields)
                if res is not None:
                    if tag in fields:
                        print('*** Duplicated key', elem.tag, tag)
                    fields[tag] = res
            else:
                print('*** Missing def', elem.tag, tag)
        return fields

    def merge(self, origin, override):
        new_obj = {}
        for key, value in self:
            if isinstance(value, (GroupBy, LinkToPreviousGroupBy)):
                key = value.group_key
            if key in origin and key not in override:
                new_obj[key] = origin[key]
            elif key not in origin and key in override:
                new_obj[key] = override[key]
            elif key in origin and key in override:
                new_obj[key] = value.merge(origin[key], override[key])
        return new_obj

    def __getitem__(self, key: str):
        return self._fields[key]

    def __iter__(self):
        return ((key, value) for key, value in self._fields.items())

    def __contains__(self, key):
        return key in self._fields


class List(ParsingType):
    def __init__(self, elem: Entity):
        self._elem = elem

    def parse(self, elem: Element, **kwargs):
        entities = []
        for child in elem:  # type: Element
            entities.append(self._elem.parse(child))
        return entities

    def merge(self, origin, override):
        new_list = []
        origin_items = dict(map(lambda e: (e[self._elem.merge_id], e), origin))
        override_items = dict(map(lambda e: (e[self._elem.merge_id], e), override))
        for _id in origin_items | override_items:
            if _id in origin_items and _id not in override_items:
                new_list.append(origin_items[_id])
            elif _id not in origin_items and _id in override_items:
                new_list.append(override_items[_id])
            elif _id in origin_items and _id in override_items:
                new_list.append(self._elem.merge(origin_items[_id], override_items[_id]))
        return new_list


class GroupBy(ParsingType):
    def __init__(self, key: str, elem: ParsingType):
        self._key = key
        self._elem = elem

    @property
    def group_key(self):
        return self._key

    def parse(self, elem: Element, *, parent_fields=None):
        if parent_fields is None:
            return None
        if self._key not in parent_fields:
            parent_fields[self._key] = []
        parent_fields[self._key].append(self._elem.parse(elem))

    def merge(self, origin, override):
        print('*** Unsupported merge type GroupBy')
        return origin


class LinkToPreviousGroupBy(ParsingType):
    def __init__(self, group_by_key: str, key: str, elem: Entity):
        self._grp_key = group_by_key
        self._key = key
        self._elem = elem

    @property
    def group_key(self):
        return self._grp_key

    def parse(self, elem: Element, *, parent_fields=None):
        if parent_fields is None or self._grp_key not in parent_fields:
            return None
        if len(parent_fields[self._grp_key]) > 0:
            parent_fields[self._grp_key][-1][self._key] = self._elem.parse(elem)

    def merge(self, origin, override):
        print('*** Unsupported merge type LinkToPreviousGroupBy')
        return origin
