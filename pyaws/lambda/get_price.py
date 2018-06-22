"""
Retrieve Amazon Web Services Pricing
"""
import json
import requests

from functools import lru_cache
from itertools import chain

INDEXURL = "https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/index.json"
url_prefix = "https://pricing.us-east-1.amazonaws.com"


def global_index(service, url=INDEXURL):
    """
    Retrieves master index file containing current price file urls for all AWS Services
    """
    r = requests.get(INDEXURL)
    f1 = json.loads(r.content)
    return url_prefix + f1['offers'][service]['currentRegionIndexUrl']


def region_index(region):
    """
    Returns url of price file for specific region
    """
    r2 = requests.get(global_index(service='AWSLambda'))
    return url_prefix + json.loads(r2.content)['regions'][region]['currentVersionUrl']


@lru_cache()
def price_data(region, sku=None):
    """
    Summary:
        all price data for an AWS service
    Return:
        data (json)
    """
    r = requests.get(region_index(region)).json()

    products = [x for x in r['products'].values() if x['attributes']['servicecode'] == 'AWSLambda']
    skus = {x['sku'] for x in products}

    terms = list(chain(
        *[
            y.values() for y in [x for x in r['terms'].values()]
        ]
    ))

    parsed = []

    for term in terms:
        if list(term.values())[0]['sku'] not in skus:
            continue
        parsed.append(term)

    return products, skus, parsed


def main():
    from pprint import PrettyPrinter
    pp = PrettyPrinter()
    pp.pprint(price_data('eu-west-1'))


if __name__ == '__main__':
    main()
