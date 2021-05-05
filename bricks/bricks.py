
# -------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------

from rich.traceback import install
install()

import aiohttp
import aiohttp_cors

from aiohttp import web

def create_and_config_api():

  # ----------------------------------------
  # Create Application with Middlewares
  app = web.Application(
    middlewares=[
      # authMiddleware #authentification
    ],
    client_max_size=1024**3
  )

  # Configure CORS on all routes.
  cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
      # allow_credentials=True,
      expose_headers="*",
      allow_headers="*",
    )
  })
  for route in list(app.router.routes()):
    print(route)
    cors.add(route)
  # ----------------------------------------
  return app

app = create_and_config_api()

# ----------------------------------------
# add sub_apps
from echo import app_echo
app.add_subapp('/echo', app_echo)

from tick import app_tick
app.add_subapp('/tick', app_tick)

from graph import app_ticker
app.add_subapp('/graph', app_ticker)

from plot import app_ticker_plot
app.add_subapp('/plot', app_ticker_plot)


if __name__ == '__main__':
  web.run_app(app, port=8000)

