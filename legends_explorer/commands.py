from bolinette import blnt
from bolinette.decorators import command

from legends_explorer.legends import LegendsParser


@command('parse_legends', 'Parse Dwarf Fortress legends from XML dumps')
@command.argument('argument', 'folder', summary='Legends folder name')
@command.argument('option', 'parse', flag='p', summary='Parses collections, comma-separated or *')
@command.argument('option', 'drop', flag='d', summary='Drops collections before processing, comma-separated or *')
@command.argument('flag', 'insert', flag='i', summary='Inserts data into database')
async def parse_legends(context: blnt.BolinetteContext, folder: str, parse: str, drop: str, insert: bool):
    parser = LegendsParser(context)
    path = context.root_path('df_dumps', folder)
    await parser.parse(path, folder, parse=parse, drop=drop, insert=insert)
