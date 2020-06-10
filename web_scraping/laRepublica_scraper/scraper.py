#!/usr/bin/env python3
"""laRepublica web site scraping"""

import requests
import lxml.html as html
import os
import datetime


HOME_URL = 'https://www.larepublica.co'

XPATH_LINK_TO_ARTICLE = '//h2[@class="headline"]/a/@href'
XPATH_TITLE = '//h1[@class="headline"]/a/text()'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_BODY = '//div[@class="articleWrapper  "]/p/text()'


def parsed_notices(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"', '')
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)

            except IndexError:
                return

            filename = './' + today + '/' + title + '.txt'
            print(filename)
            with open(filename, 'w', encoding='utf-8') as f:
                f.write('\n')
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')

        else:
            raise ValueError('Error: {}'.format(response.status_code))

    except ValueError as err:
        print(err)


def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            # getting all the links of the web site
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            # print(links_to_notices)

            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)

            for link in links_to_notices:
                parsed_notices(link, today)

        else:
            raise ValueError('Error: {}'.format(response.status_code))

    except ValueError as err:
        print(err)


def run():
    parse_home()


if __name__ == "__main__":
    """ Web Scraping: History of the notices
        Getting the notices of the web site www.larepublica.co
        and save each of them with the name, description and the body
        in a directory day by day
    """
    run()
