import flask
import os
import logging
import sys
from bs4 import BeautifulSoup
import requests
import pandas as pd
from covid import CovidData

env = os.environ.get
app = flask.Flask(__name__)


class Config(object):
    COVID_SOURCE_DATA_REST_API = env('COVID_SOURCE_DATA_REST_API', 'https://www.worldometers.info/coronavirus/')
    SECRET_KEY = env("SECRET_KEY", "\xb6\x90\xfe\xd4\xf5\xdd\xf3\x1b\x9b2\x8d\x1b\xa1\x14'\x14>{\xe2\xb0\xb1\xc5\xfa2")


app.config.from_object(Config())

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)


def load_covid_data():
    html_content = requests.get(app.config['COVID_SOURCE_DATA_REST_API']).text
    covid_soup = BeautifulSoup(html_content, 'lxml')
    covid_table = covid_soup.find("table", attrs={"id": "main_table_countries_today"})
    heading = covid_table.thead.find_all("tr")
    headings = []
    for th in heading[0].find_all("th"):
        logger.info(th.text)
        headings.append(th.text.replace("\n", "").strip())
    body = covid_table.tbody.find_all("tr")
    data = []
    for r in range(1, len(body)):
        row = []
        for tr in body[r].find_all("td"):
            row.append(tr.text.replace("\n", "").strip())
        data.append(row)
    df = pd.DataFrame(data, columns=headings)
    df = df[df["#"] != ""].reset_index(drop=True)
    df = df.drop_duplicates(subset=["Country,Other"])
    return df


@app.route('/api/get_country_data/', methods=['POST'])
def get_country_data():
    input_data = [k.lower() for k in flask.request.json['country_list'].split("|")]
    logger.info(input_data)
    covid_data = load_covid_data()
    final_data = [CovidData(r['Country,Other'], r['TotalCases'], r['NewCases'], r['TotalDeaths'], r['NewDeaths'],
                            r['TotalRecovered'], r['ActiveCases'], r['Serious,Critical'], r['TotalTests'],
                            r['Population']) for index, r in covid_data.iterrows()]
    response = [r.__dict__ for r in final_data if r.country_name.lower() in input_data]
    logger.info(response)
    return flask.jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)