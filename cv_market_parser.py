#import required libs
from requests_html import HTMLSession
import contextlib
import re, json
from re import search

def cv_market_parser():
    url = 'https://www.cvmarket.lt/'

    def get_listing(url):
        """
        Function takes url,
        then loops through main table to scrape listing
        data to dictionary. 
        Arguments:
            url: string
        Returns:
            list of dictionaries
        """
        s = HTMLSession()
        r = s.get(url)

        listings = []
        # data is representen in table, thus looping through table rows and columns
        table = r.html.find('table')[1]
        for row in table.find('tr'):
            
            for c in row.find('td.main-column'):
                listing = {
                    'employer': c.find('span.f_job_company')[0].text,
                    'position': c.find('a.f_job_title')[0].text           
                    }

            for c in row.find('td.location-column'):   
                listing['location'] = row.find('div.f_job_city')[0].text

            for c in row.find('td.main-column'):
                salary_col = c.find('span.f_job_salary > b')
                for i in salary_col:
                    # handle exceptions of many html tags not having data or being invalid type
                    try:
                        salary_str = (i.text).replace(' ', '')
                        listing['salary'] = re.split('-| ', salary_str)
                        
                        # listing['salary'] = (i.text).replace(' ', '').split('-')                    
                    except Exception:
                        listing['salary'] = ''                       
                try:
                    listing['salary_payment'] = c.find('span.salary-type')[0].text
                except Exception:
                    listing['salary_payment'] = ''
            
                # follow link to get description of job listing
                link = list(c.find('a.f_job_title')[0].absolute_links)[0]
            
                r = s.get(link)           

                listing['description'] = ' '.join((('').join(r.html.find('div.job-offer')[0].text)).splitlines())
                listing['link'] = link
                listing['source'] = 'cv_market'
            
            listings.append(listing)      
            
        return listings
            

    def get_max_pagination(url = 'https://www.cvmarket.lt/darbo-skelbimai?start=50000'):
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

        return int((search(r'\d+', ('').join(((r.html.find('ul.pagination')[0].text).splitlines())))).group()[-4:])

    # create a list of all urls containing job listings
    urls = [f'https://www.cvmarket.lt/darbo-skelbimai?start={offset}' for offset in range(0, get_max_pagination()*25, 25)]

    # loop through urls using function get_listing()
    vacancies = []
    for page, url in enumerate(urls, start=1):
        with contextlib.suppress(Exception):
            vacancies.extend(get_listing(url))
            # feedback on how parsing status
            print(f'page {page} out of {get_max_pagination()} at cv_market_parsed')

    # return (bytes(json.dumps(vacancies).encode('UTF-8')))
    return json.dumps(vacancies).encode('UTF-8')
   

