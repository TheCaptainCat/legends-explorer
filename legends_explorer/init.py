from bolinette import blnt
from bolinette.decorators import init_func

from legends_explorer.legends import LegendsConnection


@init_func
def init_legends_mongo(context: blnt.BolinetteContext):
    context['df_mongo'] = LegendsConnection(context.env['legends_mongo_url'], context.env['legends_mongo_database'])
