# -*- coding: utf-8 -*-
from metaapi_cloud_sdk import MetaApi
import asyncio
import time

# CONFIG
TOKEN = 'eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiJiNGIyZjFkYzMwMDFiMWY1NWEzOGJlZDI0MDIwYjU2NCIsImFjY2Vzc1J1bGVzIjpbeyJpZCI6InRyYWRpbmctYWNjb3VudC1tYW5hZ2VtZW50LWFwaSIsIm1ldGhvZHMiOlsidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiXSwicmVzb3VyY2VzIjpbImFjY291bnQ6JFVTRVJfSUQkOmFkYzc4YmQ2LTNmNmQtNDI0Yy1iM2FmLWNlNTNhM2VjYmRmYSJdfSx7ImlkIjoibWV0YWFwaS1yZXN0LWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiYWNjb3VudDokVVNFUl9JRCQ6YWRjNzhiZDYtM2Y2ZC00MjRjLWIzYWYtY2U1M2EzZWNiZGZhIl19LHsiaWQiOiJtZXRhYXBpLXJwYy1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOndzOnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyJhY2NvdW50OiRVU0VSX0lEJDphZGM3OGJkNi0zZjZkLTQyNGMtYjNhZi1jZTUzYTNlY2JkZmEiXX0seyJpZCI6Im1ldGFhcGktcmVhbC10aW1lLXN0cmVhbWluZy1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOndzOnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyJhY2NvdW50OiRVU0VSX0lEJDphZGM3OGJkNi0zZjZkLTQyNGMtYjNhZi1jZTUzYTNlY2JkZmEiXX0seyJpZCI6Im1ldGFzdGF0cy1hcGkiLCJtZXRob2RzIjpbIm1ldGFzdGF0cy1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciJdLCJyZXNvdXJjZXMiOlsiYWNjb3VudDokVVNFUl9JRCQ6YWRjNzhiZDYtM2Y2ZC00MjRjLWIzYWYtY2U1M2EzZWNiZGZhIl19LHsiaWQiOiJyaXNrLW1hbmFnZW1lbnQtYXBpIiwibWV0aG9kcyI6WyJyaXNrLW1hbmFnZW1lbnQtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiXSwicmVzb3VyY2VzIjpbImFjY291bnQ6JFVTRVJfSUQkOmFkYzc4YmQ2LTNmNmQtNDI0Yy1iM2FmLWNlNTNhM2VjYmRmYSJdfV0sImlnbm9yZVJhdGVMaW1pdHMiOmZhbHNlLCJ0b2tlbklkIjoiMjAyMTAyMTMiLCJpbXBlcnNvbmF0ZWQiOmZhbHNlLCJyZWFsVXNlcklkIjoiYjRiMmYxZGMzMDAxYjFmNTVhMzhiZWQyNDAyMGI1NjQiLCJpYXQiOjE3NDg0MjgzMzMsImV4cCI6MTc1NjIwNDMzM30.g6Ex02jTEg7gt6U265Cwfu-wBna3c6SAHWm9zKVC2ncoJVCeiF_jfQJ0XCAG4d7GihBsjgWzNLXTU358neorUf_9zT4V-iDkh_sTyqTjCkmT2KuN5cl2iUjUmaQcPj0puMHZ92zuz5R0RBVShrIgN5B_q2o2Ly-WPtZQA5TBvObjtC2I8N7XMhY0R7U3DFe8-5oO-8z5kUxHC-QHBM9ta4JISsh1aySbRWO7AInHDtobvuPkbuGbkMlyRjJjztNv1h44PmoJx7YFyNvbb_qUUnauc5kKo695O_LtEbamdus6apKYVOM0mP1DWcgHNhZNpp3l3nKFo05VpxcpdtffnI82ZQX55jJSnplednrhoYb6mJ5fzU50Nhq-zcq5JILnGCHLhml8-A2Wi_NlCnTlQdWdHnu-ofbOBh3LeKj3BqqZfVj3HNhRi29UG2HjF_ysDsyI_C5Bv2u7EU9RP-okx9-HvH68nE98yXNHtn2Q9iRUbdybTzwqSmDYcirKXipOzClzru6Ur6Qjix5sFCf04z-cnkWt_Nsew0q-9zWPy7iDSWnQyeB-bE-4nU3NTCpGTXnG4Y-2M2Sp0lmJM0Zmt7t7xL-av3KmjU1iLuFQOGYd1QZT3yQvUxsPtMcm4IKxIffaTdqo9Na2F9FCOPK00GDho_Kq_HbsnYkWGKmT038'  # <- wklej tutaj swoj prawdziwy token
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
