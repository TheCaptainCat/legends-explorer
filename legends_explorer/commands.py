from bolinette import blnt
from bolinette.decorators import command

from legends_explorer.legends import LegendsParser


@command('parse_legends', 'Parse Dwarf Fortress legends from XML dumps')
@command.argument('argument', 'folder', summary='Legends folder name')
@command.argument('option', 'drop', flag='d', summary='Drops collections before processing, comma-separated or *')
async def parse_legends(context: blnt.BolinetteContext, folder: str, drop: str):
    parser = LegendsParser(context)
    path = context.root_path('df_dumps', folder)
    await parser.parse(path, folder, drop=drop)
