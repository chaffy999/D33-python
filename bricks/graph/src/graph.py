import json
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import aiohttp
import asyncio
from rich import print

url = 'https://dbschool.alcyone.life/graphql'

async def create_tick(request):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://51.15.17.205:9000/tick/chaffydev') as resp:
                info = await resp.json()
                ticks = info['data']
            
            transport = AIOHTTPTransport(url="https://dbschool.alcyone.life/graphql")
            client = Client(transport=transport, fetch_schema_from_transport=True)

            for tick in ticks:
                query = gql("""mutation {
                                createTicker(input: { data: { symbol: "%s", price: %d } }) {
                                    ticker {
                                    symbol
                                    price
                                    }
                                }
                            }""" % (tick["symbol"], float(tick["price"]))
                        )
                        
                result = await client.execute_async(query)
                print(result)

        return aiohttp.web.json_response(dict(json=info))
    except Exception as e:
        print(e)
        raise e