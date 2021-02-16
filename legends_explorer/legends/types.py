import re
from abc import ABC, abstractmethod
from typing import Dict, Any, Union
from xml.etree.ElementTree import Element

str_regex = re.compile('[\t\n ]')


class ParsingType(ABC):
    @abstractmethod
    def merge(self, origin, override):
        pass


class BasicType(ParsingType, ABC):
    @abstractmethod
    def parse(self, elem: Element) -> Union[str, int, float, list]:
        pass


class ComplexType(ParsingType, ABC):
    @abstractmethod
    def parse(self, elem: Element, *, parent_fields: Dict[str, Any]) -> None:
        pass


class Bool(BasicType):
    def parse(self, elem: Element):
        if elem.tag == 'false':
            return False
        return True

    def merge(self, origin, override):
        return True


class Int(BasicType):
    def parse(self, elem: Element):
        return int(elem.text)

    def merge(self, origin, override):
        return override


class Float(BasicType):
    def parse(self, elem: Element):
        return float(elem.text)

    def merge(self, origin, override):
        return override


class Str(BasicType):
    def parse(self, elem: Element):
        return elem.text

    def merge(self, origin, override):
        new_str = str_regex.sub('', override)
        if len(new_str) > 0:
            return override
        return origin


class SplitStr(BasicType):
    def __init__(self, char: str):
        self._char = char

    def parse(self, elem: Element):
        return elem.text.split(self._char)

    def merge(self, origin, override):
        print('*** Unsupported merge type GroupTree')
        return origin


class Population(BasicType):
    def parse(self, elem: Element):
        race, population = elem.text.split(':')
        return {'race': race, 'population': int(population)}

    def merge(self, origin, override):
        return override


class Coordinates(BasicType):
    def parse(self, elem: Element):
        if '|' in elem.text:
            raise ValueError()
        x, y = elem.text.split(',')
        return {'x': int(x), 'y': int(y)}

    def merge(self, origin, override):
        return override


class Path(BasicType):
    def __init__(self, *, points: int = 2):
        self._points = points
        if points > 3:
            self._origin_point = ord('a')
        else:
            self._origin_point = ord('x')

    def parse(self, elem: Element):
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


class Rectangle(BasicType):
    def parse(self, elem: Element):
        point0, point1 = elem.text.split(':')
        point00, point01 = point0.split(',')
        point10, point11 = point1.split(',')
        return {'x0y0': int(point00), 'x0y1': int(point01), 'x1y0': int(point10), 'x1y1': int(point11)}

    def merge(self, origin, override):
        return override


class Entity(ParsingType):
    def __init__(self, merge_id: str, fields: Dict[str, Union[BasicType, ComplexType]],
                 *, transforms: Dict[str, str] = None):
        self._merge_id = merge_id
        self._fields = dict([(field, fields[field]) for field in fields if not isinstance(fields[field], GroupTree)])
        self._group_trees = [value for value in fields.values() if isinstance(value, GroupTree)]
        self._transforms = transforms

    @property
    def merge_id(self):
        return self._merge_id

    def parse(self, elem: Element):
        fields = {}
        for child in elem:  # type: Element
            tag = child.tag
            if self._transforms is not None and tag in self._transforms:
                tag = self._transforms[tag]
            if tag in self._fields:
                if tag in fields:
                    print('*** Duplicated key', elem.tag, tag)
                p_type = self._fields[tag]
                if isinstance(p_type, BasicType):
                    fields[tag] = p_type.parse(child)
                elif isinstance(p_type, ComplexType):
                    p_type.parse(child, parent_fields=fields)
            else:
                for group in self._group_trees:
                    if group.test(tag):
                        group.parse(child, parent_fields=fields)
                        break
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


class List(BasicType):
    def __init__(self, elem: Entity):
        self._elem = elem

    def parse(self, elem: Element):
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


class GroupBy(ComplexType):
    def __init__(self, key: str, elem: Union[BasicType, Entity]):
        self._key = key
        self._elem = elem

    @property
    def group_key(self):
        return self._key

    def parse(self, elem: Element, *, parent_fields):
        if parent_fields is None:
            return None
        if self._key not in parent_fields:
            parent_fields[self._key] = []
        parent_fields[self._key].append(self._elem.parse(elem))

    def merge(self, origin, override):
        new_grp = []
        if isinstance(self._elem, Entity):
            print('*** Unsupported merge type GroupBy')
            return origin
        else:
            for elem in origin:
                if elem not in override:
                    new_grp.append(elem)
            for elem in override:
                new_grp.append(elem)
        return new_grp


class LinkToPreviousGroupBy(ComplexType):
    def __init__(self, group_by_key: str, key: str, elem: Union[BasicType, Entity]):
        self._grp_key = group_by_key
        self._key = key
        self._elem = elem

    @property
    def group_key(self):
        return self._grp_key

    def parse(self, elem: Element, *, parent_fields):
        if parent_fields is None or self._grp_key not in parent_fields:
            return None
        if len(parent_fields[self._grp_key]) > 0:
            parent_fields[self._grp_key][-1][self._key] = self._elem.parse(elem)

    def merge(self, origin, override):
        print('*** Unsupported merge type LinkToPreviousGroupBy')
        return origin


class Wrap(BasicType):
    def __init__(self, wrapping_key, elem: BasicType):
        self._key = wrapping_key
        self._elem = elem

    def parse(self, elem: Element):
        return {self._key: self._elem.parse(elem)}

    def merge(self, origin, override):
        print('*** Unsupported merge type Wrap')
        return origin


class GroupTree(ComplexType):
    def __init__(self, start: str, depth: int, elem: BasicType):
        self._start = start
        self._depth = depth
        self._elem = elem

    def test(self, tag: str):
        return tag.startswith(self._start)

    def parse(self, elem: Element, *, parent_fields):
        path = [self._start[:-1]] + elem.tag[len(self._start):].split('_', maxsplit=self._depth - 1)
        collection = parent_fields
        for key in path[:-1]:
            if key not in collection:
                collection[key] = {}
            collection = collection[key]
        collection[path[-1]] = self._elem.parse(elem)

    def merge(self, origin, override):
        print('*** Unsupported merge type GroupTree')
        return origin
