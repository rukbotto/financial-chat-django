import csv
import datetime
import json
import http.client
import io

from celery import shared_task
from websocket import create_connection


@shared_task
def query_quote(quote, room_id, user_id):
    price = ''

    url = '/q/l/?s={}.us&f=sd2t2ohlcv&h&e=csv'.format(quote.lower())
    connection = http.client.HTTPSConnection('stooq.com')
    connection.request('GET', url)
    response = connection.getresponse()
    csv_data = io.StringIO(response.read().decode('utf-8'))

    csv_reader = csv.DictReader(csv_data)
    for row in csv_reader:
        price = row['Close']

    content = '{} quote is ${} per share'.format(quote, price)

    ws = create_connection('ws://localhost:8000/ws/room/{}/'.format(room_id))
    ws.send(
        json.dumps({ 'content': content, 'room_id': room_id, 'user_id': user_id })
    )
    ws.close()
