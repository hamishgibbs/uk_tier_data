import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import datetime
import logging
import platform

def scrape(url):
    '''Function to scrape url for Areas by tier table'''

    r = requests.get(url)

    soup = BeautifulSoup(r.text, 'html.parser')

    # get table by selector
    table = soup.select('#mw-content-text > div.mw-parser-output > table:nth-child(22)')

    # pull table caption
    caption = table[0].find('caption')

    # check that this is the correct table
    assert 'Areas by tier' in caption.text

    '''
    Rows follow a repeating pattern of:

    * Tier, Header, Values
    * Tier, Header, Values
        * Header, Values
        * Header, Values
    * Tier, Header, Values

    etc.
    '''

    group_rows = []

    for row in table[0].find_all('tr'):

        row_data = parse_row(row)
        row_header_data = parse_row_header(row)

        # update data dictionary with header if it is present
        try:
            row_data.update(row_header_data)
        except:
            pass

        group_rows.append(row_data)

    group_rows = [x for x in group_rows if x is not None]

    group_rows = fill_header(group_rows)

    return(group_rows)

def parse_row(row):
    '''Function to parse data elements (td) from table row'''

    try:
        data = row.find_all('td')

        data = {
                'date':data[0].text,
                # preserve html tags
                'area':str(data[1]),
        }

        return (data)

    except:

        pass

def parse_row_header(row):
    '''Function to parse header elements (th) from table row'''

    data = row.find('th')

    try:

        return({'tier':data.text})

    except:

        return(None)


def fill_header(rows):
    '''Function to add a header key for non-header rows'''

    res = []

    for row in rows:

        if 'tier' in row.keys():

            tier = {'tier': row['tier']}

        row.update(tier)

        res.append(row)

    return(res)

def parse_scrape_row(row):
    '''Function to convert row dict to DataFrame'''

    # parse Tier
    tier = row['tier']
    tier = tier.replace('\n', '')

    # parse Date
    date = row['date']
    date = date.replace('\n', '')

    # parse Area
    area = parse_area(row['area'])

    area['tier'] = tier
    area['date'] = date

    return(area)

def parse_area(area):
    '''Function to parse a string of area names, identifying counties and la names by italics'''

    area = str(area).replace('<td>', '')
    area = str(area).replace('</td>', '')

    # select italic text as major area name
    area = area.split('<i>')

    area = [x for x in area if x != '']

    areas = []

    for area_group in area:

        area_group = area_group.split('</i>')

        mega = area_group[0]
        mini = area_group[1:]

        mini = [x.replace('\n', '') for x in mini]
        mini = [x.replace(': ', '') for x in mini]
        mini = [x.replace('. ', '') for x in mini]

        assert len(mini) <= 1

        if mini == []:

            mini = ['NA']

        areas.append({mega: mini[0].split(', ')})

    areas = [pd.concat({k: pd.Series(v) for k, v in x.items()}) for x in areas]
    areas = [x.reset_index() for x in areas]
    areas = pd.concat(areas)
    areas.columns = ['county', 'i', 'la_name']
    areas = areas[['county', 'la_name']]

    return(areas)

if __name__ == '__main__':

    run_time = datetime.datetime.now()

    logging.basicConfig(filename='output/scrape_%s.log' % run_time.strftime("%d_%m_%y_%H%M"), level=logging.DEBUG)

    ''' Scrape data from Wikipedia table '''

    logging.info('Starting Wikipedia scrape: %s Platform: %s' % (run_time.strftime("%d-%m-%y %H:%M"), platform.platform()))

    url = 'https://en.wikipedia.org/wiki/COVID-19_tier_regulations_in_England'

    data = scrape(url)

    data = [parse_scrape_row(x) for x in data if x is not None]

    pd.concat(data).to_csv('output/uk_tier_data_wikipedia_%s.csv' % run_time.strftime("%d_%m_%y_%H%M"), index = False)
    pd.concat(data).to_csv('output/uk_tier_data_wikipedia_latest.csv', index = False)

    logging.info('Successfuly downloaded Wikipedia data.')

    logging.info('Starting Parliament scrape: %s Platform: %s' % (run_time.strftime("%d-%m-%y %H:%M"), platform.platform()))

    ''' Download data from parliament website '''

    url = 'https://visual.parliament.uk/research/visualisations/coronavirus-restrictions-map/commonslibrary-coronavirus-restrictions-data.csv'

    data = pd.read_csv(url)

    pd.concat(data).to_csv('output/uk_tier_data_parliament_%s.csv' % run_time.strftime("%d_%m_%y_%H%M"), index = False)
    pd.concat(data).to_csv('output/uk_tier_data_parliament_latest.csv', index = False)

    logging.info('Successfuly downloaded Parliament data.')
