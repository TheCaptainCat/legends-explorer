from xml.etree.ElementTree import parse as parse_xml, Element

from bolinette import blnt
from bolinette.exceptions import InternalError
from bolinette.utils import paths

from legends_explorer.legends import Entity, LegendsConnection, Collection
from legends_explorer.legends.types import Int, Str, Rectangle, Coordinates, List


class LegendsParser:
    def __init__(self, context: blnt.BolinetteContext):
        self.context = context
        self.mongo: LegendsConnection = self.context['df_mongo']
        self._parsers = {
            'regions': Collection('regions', Entity({'id': Int(), 'name': Str(), 'type': Str()}, {})),
            'underground_regions': Collection('underground_regions', Entity(
                {'id': Int(), 'type': Str(), 'depth': Int()}, {}
            )),
            'sites': Collection('sites', Entity({
                'id': Int(), 'type': Str(), 'name': Str(), 'coords': Coordinates(), 'rectangle': Rectangle(),
                'structures': List(Entity(
                    {'local_id': Int(), 'type': Str(), 'name': Str(), 'entity_id': Int(),
                     'subtype': Str(), 'owner_hfid': Int(), 'copied_artifact_id': Int(),
                     'worship_hfid': Int()}, {}
                )),
                'site_properties': List(Entity(
                    {'id': Int(), 'structure_id': Int(), 'type': Str(), 'owner_hfid': Int()}, {}
                ))
            }, {})),
            'artifacts': Collection('artifacts', Entity({
                'id': Int(), 'name': Str(), 'site_id': Int(), 'holder_hfid': Int(),
                'structure_local_id': Int(), 'subregion_id': Int(),
                'abs_tile_x': Str(), 'abs_tile_y': Str(), 'abs_tile_z': Str(),
                'item': Entity({
                    'name_string': Str(), 'page_number': Int(), 'page_written_content_id': Int(),
                    'writing_written_content_id': Int()
                }, {})
            }, {}))
        }

    async def parse(self, path: str, region: str, *, drop: str = None):
        if not paths.exists(path):
            raise InternalError(f'{path} does not exist')
        if drop is not None:
            await self._drop(drop)
        await self._parse_legends(path, region)
        await self._parse_legends_plus(path, region)

    async def _drop(self, args):
        if args == '*':
            self.context.logger.debug('Dropping all collections')
            for name in self._parsers:
                self.mongo.db.drop_collection(name)
            self.context.logger.debug('Done dropping all collections')
        else:
            drop_cols = args.split(',')
            cols = self.mongo.db.collection_names()
            for col in drop_cols:
                if col in cols:
                    self.mongo.db.drop_collection(col)

    async def _parse_legends(self, path: str, region: str):
        file_path = paths.join(path, f'{region}-legends.xml')
        if not paths.exists(file_path):
            raise InternalError(f'{file_path} does not exist')
        self.context.logger.debug(f'Parsing {file_path}')
        tree = parse_xml(file_path)
        root = tree.getroot()
        for elem in root:  # type: Element
            if elem.tag in self._parsers:
                self.context.logger.debug(f'Parsing {elem.tag}')
                await self._parsers[elem.tag].parse(elem)
            else:
                self.context.logger.debug(f'Not parsing {elem.tag}')
        self.context.logger.debug(f'Done parsing {file_path}')
        self.context.logger.debug('Writing to database')
        await self._push_to_mongo()
        self.context.logger.debug('Done writing to database')

    async def _parse_legends_plus(self, path: str, region: str):
        file_path = paths.join(path, f'{region}-legends_plus.xml')
        if not paths.exists(file_path):
            raise InternalError(f'{file_path} does not exist')

    async def _push_to_mongo(self):
        cols = self.mongo.db.collection_names()
        for name, parser in self._parsers.items():
            if name not in cols:
                await parser.insert(self.mongo)
                self.context.logger.debug(f'Inserting {name}')
            else:
                self.context.logger.debug(f'Not inserting {name}')
