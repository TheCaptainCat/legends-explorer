from xml.etree.ElementTree import Element

from legends_explorer.legends import LegendsConnection
from legends_explorer.legends.types import Entity


class Collection:
    def __init__(self, name: str, root: Entity):
        self._name = name
        self._entities = {}
        self._root = root

    async def parse(self, elem: Element):
        for child in elem:  # type: Element
            entity = self._root(child)
            self._entities[entity['id']] = entity

    async def insert(self, mongo: LegendsConnection):
        regions = [r for r in self._entities.values()]
        mongo.db[self._name].insert(regions)
