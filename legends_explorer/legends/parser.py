import typing
from xml.etree.ElementTree import parse as parse_xml, Element

from bolinette import blnt
from bolinette.exceptions import InternalError
from bolinette.utils import paths

from legends_explorer.legends import LegendsConnection, definitions


class LegendsParser:
    def __init__(self, context: blnt.BolinetteContext):
        self.context = context
        self.mongo: LegendsConnection = self.context['df_mongo']
        self._parsers = definitions

    async def parse(self, path: str, region: str, *, parse: str = None, drop: str = None, insert: bool = False):
        if parse != '*':
            parse = parse.split(',')
        else:
            parse = None
        if not paths.exists(path):
            raise InternalError(f'{path} does not exist')
        if drop is not None:
            await self._drop(drop)
        await self._parse_legends(path, region, parse_only=parse)
        await self._parse_legends_plus(path, region, parse_only=parse)
        if insert:
            self.context.logger.debug('Writing to database')
            await self._push_to_mongo(push_only=parse)
            self.context.logger.debug('Done writing to database')

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

    async def _parse_legends_file(self, file_path: str, parse_only: typing.List[str] = None):
        if not paths.exists(file_path):
            raise InternalError(f'{file_path} does not exist')
        self.context.logger.debug(f'Parsing {file_path}')
        tree = parse_xml(file_path)
        root = tree.getroot()
        for elem in root:  # type: Element
            if elem.tag in self._parsers and (parse_only is None or elem.tag in parse_only):
                self.context.logger.debug(f'Parsing {elem.tag}')
                await self._parsers[elem.tag].parse(elem)
            else:
                self.context.logger.debug(f'Not parsing {elem.tag}')
        self.context.logger.debug(f'Done parsing {file_path}')

    async def _parse_legends(self, path: str, region: str, parse_only: typing.List[str] = None):
        file_path = paths.join(path, f'{region}-legends.xml')
        await self._parse_legends_file(file_path, parse_only)

    async def _parse_legends_plus(self, path: str, region: str, parse_only: typing.List[str] = None):
        file_path = paths.join(path, f'{region}-legends_plus.xml')
        await self._parse_legends_file(file_path, parse_only)

    async def _push_to_mongo(self, push_only: typing.List[str] = None):
        cols = self.mongo.db.collection_names()
        for name, parser in self._parsers.items():
            if name not in cols and (push_only is None or name in push_only):
                self.context.logger.debug(f'Inserting {name}: {len(parser)} entities')
                await parser.insert(self.mongo)
            else:
                self.context.logger.debug(f'Not inserting {name}')
