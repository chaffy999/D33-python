# 
from plot.src.plot import (
  create_plot
)

#
from aiohttp import web

#
app_ticker_plot = web.Application()

#
app_ticker_plot.add_routes([

  web.post('/', create_plot),
  web.get('/', create_plot),
  
])