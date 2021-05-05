from graph.src.graph import (
  create_tick
)

#
from aiohttp import web

#
app_ticker = web.Application()

#
app_ticker.add_routes([

  web.post('/', create_tick),
  
])