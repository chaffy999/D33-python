import json
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import aiohttp
import asyncio
from rich import print
import pandas as pd
import matplotlib.pyplot as plt


URL = 'https://dbschool.alcyone.life/graphql'

async def create_plot(request):
    try:
        async with aiohttp.ClientSession() as session:

            req_param = request.rel_url.query['symbol'].split(',') if request.rel_url.query else ["BTCUSDT"] # ?symbol=BTCUSDT,ZRXUSDT,ZRXBUSD
            req = await request.json() if request.body_exists else {"symbol": req_param}
            transport = AIOHTTPTransport(url=URL)
            client = Client(transport=transport, fetch_schema_from_transport=True)

            listofdf = []
            for symbol in req["symbol"]:
                query = gql("""query {
                                tickers(where: { symbol_contains: "%s" }) {
                                    price
                                    created_at
                                }
                            }""" % symbol
                        ) 

                result = await client.execute_async(query)
                histprices = result['tickers']

                histpricesdf = pd.DataFrame.from_dict(histprices)
                histpricesdf = histpricesdf.rename({'price': symbol}, axis=1)
                listofdf.append(histpricesdf)

            dfs = [df.set_index('created_at') for df in listofdf]
            histpriceconcat = pd.concat(dfs, axis=1)
            
            for i, col in enumerate(histpriceconcat.columns):
                histpriceconcat[col].plot()

            plt.title('Évolution du '+symbol)
            plt.xticks(rotation=70)
            plt.legend(histpriceconcat.columns)
            filename = '.'.join([ '-'.join(req["symbol"]), 'png'])
            file_path = f"./plot/plots/{filename}"
            plt.savefig(file_path, bbox_inches='tight')

        return aiohttp.web.FileResponse(f'./{file_path}')
    except Exception as e:
        print(e)
        raise e