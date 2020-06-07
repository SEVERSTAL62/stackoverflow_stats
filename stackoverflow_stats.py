from flask import Flask
import json

import requests
app = Flask(__name__)

@app.route('/health')
def health():
    return 'Application is running...'

@app.route('/search/<tag>')
def get_cur_time(tag):
    result = {}

    result[tag] = rec(tag)

    return json.dumps(result)


def request_service(tag, page):
    payload = {'page': page, 'pagesize': 100, 'tagged': tag, 'site': 'stackoverflow', 'order': 'desc', 'sort': 'creation'}
    url = 'https://api.stackexchange.com/search'
    response = requests.get(url, params=payload)
    return response.json()


def rec(tag, total=0, answered=0, page=1, has_more=True):
    if has_more:
       rj = request_service(tag, page)

       total += len(rj['items'])
       answered += len(list(filter(lambda x: x['is_answered'], rj['items'])))

       rec(tag, total, answered, page + 1, rj['has_more'])
    else:
        stat_dict = {}
        stat_dict['total'] = total
        stat_dict['answered'] = answered
        return stat_dict