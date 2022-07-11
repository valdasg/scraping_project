#import required libs

from requests_html import HTMLSession
from re import search
import json


def cv_online_parser():
    def get_listing(listing):
        """
        Function takes container listings,
        and scrape it to
        data to dictionary. 
        Arguments:
            listing: string
        Returns:
            dictionary
        """  
        employer = listing.find('div.vacancy-item__body > a')[0].text
        position = listing.find('span.vacancy-item__title')[0].text
        location = listing.find('span.vacancy-item__locations')[0].text.split('—')[1]
        # handle exceptions of many html tags not having data or being invalid type
        try:
            salary = list(listing.find('span.vacancy-item__salary-label')[0].text.split(' '))        
        except Exception:
            salary = ''
        salary_payment = 'before tax'

        # follow link to get description of job listing
        for sub_url in listing.find('li.vacancies-list__item > div > a')[0].absolute_links:
            if search('vacancy', sub_url):
                link = sub_url        
            else:
                continue

        try:
            r = s.get(link)
            # r.html.render(sleep = 0.5, timeout = 20)
            # format description to a single string
            description = ('').join((r.html.find('div.vacancy-details')[0].text).splitlines())
            r.session.close()
        except Exception:
            description = ''


        listing = {
            'employer': employer,
            'position': position,
            'location': location,
            'salary': salary,
            'salary_payment': salary_payment,
            'description': description,
            'link': link,
            'source': 'cv_online'
        }

        return listing

    # get highest pagination number for loop
    def get_max_pagination(url = 'https://cvonline.lt/lt/search?limit=20&offset=9000&isHourlySalary=false'):
        """
        Function takes url,
        with a assumned last page value of 9000
        and returns real last page
        Arguments:
            url: string
        Returns:
            last_page: int
        """
        s = HTMLSession()
        r = s.get(url)
        # r.html.render(sleep = 0.5, timeout = 20)
        pages = r.html.find('button.pagination__link')
        page_list = [page.text for page in pages]
        last_page = int(max(page_list))
        r.session.close()
        return last_page

    # create a list of all urls containing job listings
    urls = [f'https://cvonline.lt/lt/search?limit=20&offset={offset}&isHourlySalary=false' for offset in range(0, get_max_pagination() * 20, 20)]
    # urls = [f'https://cvonline.lt/lt/search?limit=20&offset={offset}&isHourlySalary=false' for offset in range(0, 40, 20)]

    # loop through urls using function get_listing()
    vacancies = []
    for page, url in enumerate(urls, start=1):
        s = HTMLSession()
        r = s.get(url)
        # r.html.render(sleep = 0.5, timeout = 20)
        listings = r.html.find('li.vacancies-list__item')
        vacancies.extend(get_listing(listing) for listing in listings)
        # feedback on how parsing status
        print(f'page {page} out of {get_max_pagination()} at cv_online parsed')
        r.session.close()
        
    # return (bytes(json.dumps(vacancies).encode('UTF-8')))
    return json.dumps(vacancies).encode('UTF-8')

