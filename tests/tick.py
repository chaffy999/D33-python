import aiohttp
import asyncio
import yaml
import graphene
from datetime import datetime
import os
from rich import print
from aiohttp import web

async def main():

    async with aiohttp.ClientSession() as session:
        async with session.get('http://51.15.17.205:9000/tick/chaffydev', json=dict(text='text')) as response:
            html = await response.text()
            json = await response.json()
            #file
            filename = datetime.now()
            filename = filename.strftime("%Y%m%d")
            json["timestamp"] = f'{filename}'
            data = yaml.dump(json)
            file_path = f"../tick/data/{filename}.yaml"
            mode = 'a' if os.path.exists(file_path) else 'w'
            with open(file_path, mode) as f:
                    f.write(data)
            return web.json_response(json)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())