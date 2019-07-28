from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import pandas as pd
import numpy as np
import io


import intrinio_sdk
from intrinio_sdk.rest import ApiException

my_api_key = YOUR API KEY HERE
intrinio_sdk.ApiClient().configuration.api_key['api_key'] = my_api_key


def crypto(request):

    crypto_api = intrinio_sdk.CryptoApi()

    timeframe = 'd1'  # str | The time interval for the prices. (default to d1)
    # str | Return prices for the given Crypto Currency Pair. (optional)
    pair = 'btcusd'
    # str | Return prices for a Crypto Currency on the given Crypto Exchange. (optional)
    exchange = 'binance'
    # str | Return prices for the given Crypto Currency. (optional)
    currency = 'BTC'
    # str | Return price date/times in this timezone, also interpret start/end date/time parameters in this timezone. (optional) (default to UTC)
    timezone = 'UTC'
    # date | Return Crypto Prices on or after this date. (optional)
    start_date = datetime.today() - timedelta(days=200)
    # str | Return Crypto Prices at or after this time (24-hour). (optional)
    start_time = ''
    # date | Return Crypto Prices on or before this date. (optional)
    end_date = datetime.today() - timedelta(days=1)
    # str | Return Crypto Prices at or before this time (24-hour). (optional)
    end_time = ''
    # int | An integer greater than or equal to 1 for specifying the number of results on each page. (optional) (default to 100)
    page_size = 100
    # str | Gets the next page of data from a previous API call (optional)
    next_page = ''

    try:
        api_response = crypto_api.get_crypto_prices(
            timeframe,
            pair=pair,
            exchange=exchange,
            currency=currency,
            timezone=timezone,
            start_date=start_date,
            start_time=start_time,
            end_date=end_date,
            end_time=end_time,
            page_size=page_size,
            next_page=next_page)

        crypto_dict = api_response.prices_dict

        datos = pd.DataFrame(crypto_dict)
        f = plt.figure()
        ax = f.add_subplot(111)
        # TENGO QUE CAMBIAR LA FORMA EN LA QUE MUESTRA LAS FECHAS EL GRÁFICO
        ax.plot(datos['time'], datos['close'])
        ax.xaxis.set_major_locator(plt.MaxNLocator(8))
        ax.legend(['Value of a Bitcoin in USD'])
        plt.ylabel('Value', fontsize=10)
        plt.xlabel('Date', fontsize=10)
        ax.tick_params(labelsize=7, width=3)
        # plt.tight_layout()

        # Como enviaremos la imagen en bytes la guardaremos en un buffer
        buf = io.BytesIO()
        canvas = FigureCanvasAgg(f)
        canvas.print_png(buf)

        # Creamos la respuesta enviando los bytes en tipo imagen png
        response = HttpResponse(buf.getvalue(), content_type='image/png')

        # Limpiamos la figura para liberar memoria
        f.clear()

        # Añadimos la cabecera de longitud de fichero para más estabilidad
        response['Content-Length'] = str(len(response.content))

        # Devolvemos la response
        return response

        # return render(request, 'stock_tracker/table.html', {'datos': datos.to_html})

    except ApiException as err:
        return HttpResponse('Ha ocurrido un error {}'.format(err))


def dow_jones_30(request):

    datos = pd.read_html('https://money.cnn.com/data/dow30/')
    datos = datos[1]

    return render(request, 'stock_tracker/table.html', {'datos': datos.to_html(index=False)})


def company(request, company):

    company_api = intrinio_sdk.CompanyApi()

    # str | A Company identifier (Ticker, CIK, LEI, Intrinio ID)
    # identifier = 'AAPL'
    identifier = company[3:]
    try:
        api_response = company_api.get_company(identifier)

        # return render_to_response(datos.to_html())
        return render(request, 'stock_tracker/company.html', {'company': api_response})

    except ApiException as err:
        return HttpResponse('Ha ocurrido un error {}'.format(err))


def stock_exchange_company(request, company):

    company_api = intrinio_sdk.CompanyApi()

    # str | A Company identifier (Ticker, CIK, LEI, Intrinio ID)
    # identifier = 'AAPL'
    identifier = company[3:]

    # str | An Intrinio data tag ID or code (<a href='https://data.intrinio.com/data-tags'>reference</a>)
    tag = 'close_price'
    # close_price
    # str | Return historical data in the given frequency (optional) (default to daily)
    frequency = 'daily'
    # str | Return historical data for given fiscal period type (optional)
    type = ''
    # date | Return historical data on or after this date (optional)
    start_date = datetime.today() - timedelta(days=200)
    # date | Return historical data on or before this date (optional)
    end_date = datetime.today() - timedelta(days=1)
    # str | Sort by date `asc` or `desc` (optional) (default to desc)
    sort_order = 'desc'
    # int | The number of results to return (optional) (default to 100)
    page_size = 100
    # str | Gets the next page of data from a previous API call (optional)
    next_page = ''

    try:
        api_response = company_api.get_company_historical_data(
            identifier, tag, frequency=frequency, type=type, start_date=start_date, end_date=end_date, sort_order=sort_order, page_size=page_size, next_page=next_page)
        stock_prices = api_response.historical_data_dict
        company_info = api_response.company
        datos = pd.DataFrame(stock_prices)

        f = plt.figure()
        ax = f.add_subplot(111)
        # TENGO QUE CAMBIAR LA FORMA EN LA QUE MUESTRA LAS FECHAS EL GRÁFICO
        ax.plot(datos['date'], datos['value'])
        ax.xaxis.set_major_locator(plt.MaxNLocator(8))
        ax.legend(['Stock value for {}'.format(company_info.name)])
        plt.ylabel('Value', fontsize=10)
        plt.xlabel('Date', fontsize=10)
        ax.tick_params(labelsize=7, width=3)
        # plt.tight_layout()

        # Como enviaremos la imagen en bytes la guardaremos en un buffer
        buf = io.BytesIO()
        canvas = FigureCanvasAgg(f)
        canvas.print_png(buf)

        # Creamos la respuesta enviando los bytes en tipo imagen png
        response = HttpResponse(buf.getvalue(), content_type='image/png')

        # Limpiamos la figura para liberar memoria
        f.clear()

        # Añadimos la cabecera de longitud de fichero para más estabilidad
        response['Content-Length'] = str(len(response.content))

        # Devolvemos la response
        return response

    except ApiException as err:
        return HttpResponse('Ha ocurrido un error {}'.format(err))
