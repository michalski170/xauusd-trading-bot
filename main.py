# -*- coding: utf-8 -*-
from metaapi_cloud_sdk import MetaApi
import asyncio
import time

# CONFIG
TOKEN = 'TWOJ_API_KEY_TUTAJ'  # <- wklej tutaj swoj prawdziwy token
ACCOUNT_ID = 'adc78bd6-3f6d-424c-b3af-ce53a3ecbdfa'
SYMBOL = 'XAUUSD'
TIMEFRAME = '10m'
SL_POINTS = 3  # 3 punkty = 0.30 dla XAUUSD (punkt = 0.1)


async def run_bot():
    metaapi = MetaApi(TOKEN)
    
    print('Pobieranie konta...')
    account = await metaapi.metatrader_account_api.get_account(ACCOUNT_ID)
    
    # Czekanie na polaczenie
    print('Czekam na polaczenie...')
    while account.connection_status != 'CONNECTED' or account.synchronization_status != 'DEPLOYED':
        await asyncio.sleep(1)
        account = await metaapi.metatrader_account_api.get_account(ACCOUNT_ID)

    connection = account.get_rpc_connection()
    await connection.connect()

    print('Polaczono. Startuje bot...')

    while True:
        try:
            # Pobieranie danych 10m
            candles = await connection.get_candles(SYMBOL, TIMEFRAME, 1000)
            heikin_ashi = build_heikin_ashi(candles)

            # Nowa pozycja
            if not await connection.get_positions():
                if is_long_signal(heikin_ashi):
                    print('Wejscie LONG')
                    await connection.create_market_buy_order(SYMBOL, 0.01, sl=heikin_ashi[-1]['close'] - SL_POINTS * 0.1)
                elif is_short_signal(heikin_ashi):
                    print('Wejscie SHORT')
                    await connection.create_market_sell_order(SYMBOL, 0.01, sl=heikin_ashi[-1]['close'] + SL_POINTS * 0.1)

            # Wyjscie
            positions = await connection.get_positions()
            if positions:
                side = positions[0]['type']
                if side == 'POSITION_TYPE_BUY' and is_short_signal(heikin_ashi):
                    print('Zamykam LONG')
                    await connection.close_position(positions[0]['id'])
                elif side == 'POSITION_TYPE_SELL' and is_long_signal(heikin_ashi):
                    print('Zamykam SHORT')
                    await connection.close_position(positions[0]['id'])

            await asyncio.sleep(60)

        except Exception as e:
            print(f'Blad: {e}')
            await asyncio.sleep(5)


def build_heikin_ashi(candles):
    ha = []
    for i, c in enumerate(candles):
        close = (c['open'] + c['high'] + c['low'] + c['close']) / 4
        open_ = (ha[i-1]['open'] + ha[i-1]['close']) / 2 if i else (c['open'] + c['close']) / 2
        high = max(c['high'], open_, close)
        low = min(c['low'], open_, close)
        ha.append({'open': open_, 'close': close, 'high': high, 'low': low})
    return ha


def is_long_signal(ha):
    return ha[-1]['close'] > ha[-1]['open'] and ha[-2]['close'] > ha[-2]['open'] and ha[-3]['close'] < ha[-3]['open'] and (ha[-1]['close'] - ha[-1]['open']) >= 2.0

def is_short_signal(ha):
    return ha[-1]['close'] < ha[-1]['open'] and ha[-2]['close'] < ha[-2]['open'] and ha[-3]['close'] > ha[-3]['open'] and (ha[-1]['open'] - ha[-1]['close']) >= 2.0


if __name__ == '__main__':
    asyncio.run(run_bot())
