
from flask import Flask, request
from metaapi.cloud_metaapi import MetaApi
import asyncio

app = Flask(__name__)

TOKEN = "YOUR_METAAPI_TOKEN"
ACCOUNT_ID = "adc78bd6-3f6d-424c-b3af-ce53a3ecbdfa"

metaapi = MetaApi(TOKEN)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    signal = data.get("signal")

    async def trade():
        account = await metaapi.metatrader_account_api.get_account(ACCOUNT_ID)
        await account.deploy()
        await account.wait_connected()

        connection = account.get_streaming_connection()
        await connection.connect()
        await connection.wait_synchronized()

        if signal == "buy":
            await connection.create_market_buy_order("XAUUSD", 0.01)
        elif signal == "sell":
            await connection.create_market_sell_order("XAUUSD", 0.01)

    asyncio.run(trade())
    return "ok", 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
