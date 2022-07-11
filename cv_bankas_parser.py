#import required libs
from requests_html import HTMLSession
import re, json

def cv_bankas_parser():
    
    url = 'https://www.cvbankas.lt/'

    def get_listing(listing_container):
        """pip install requests-html
        Function takes container of listings,
        then loops through container to scrape listing
        data to dictionary. 
        Arguments:
            listing_container: string
        Returns:
            list of dictionaries
        """
        listings = []
        for listing in listing_container:            
            employer = listing.find('span.heading_secondary > span')[0].text
            position = listing.find('div.list_cell > h3.list_h3')[0].text
            # handle exceptions of many html tags not having data or being invalid type
            try:
                location = listing.find('span.list_city')[0].text
            except Exception:
                location = ''

            try:
                salary_str = listing.find('span.salary_amount')[0].text
                salary = list(re.split('-| ', salary_str))               
            except Exception:
                salary = ''
            
            try:
                salary_payment = listing.find('span.salary_calculation')[0].text
                
            except Exception:
                salary_payment = ''        
                    
            link= list(listing.find('article > a.list_a_has_logo')[0].absolute_links)[0]
            
            # follow link to get description of job listing
            try:
                r = s.get(link)
                r.html.render(sleep = 1)
                # format description to a single string
                description = ('').join((r.html.find('#jobad_content_main')[0].text).splitlines())
                r.session.close()
            except Exception:
                description = ''

            # collect dictionary
            listing = {
                'employer': employer,
                'position': position,
                'location': location,
                'salary': salary,
                'salary_payment': salary_payment,
                'description': description,
                'link': link,
                'source': 'cv_bankas'
            }

            # append dictionaries while looping through container items
            listings.append(listing)
        return listings


    # create a session
    s = HTMLSession()s
    r = s.get(url)    

    # get highest pagination number for loop
    link_list= (r.html.find('ul.pages_ul_inner'))
    pages = [page.text for page in link_list]
    max_pagination = int(((pages[0].replace('\n', ',')).replace('...,', '').split(','))[-1])-1
    r.session.close()
    # create a list of all urls containing job listings
    urls = []
    for n in range(1, max_pagination):
        url = f'https://www.cvbankas.lt/?page={n}' 
        urls.append(url)

    # loop through urls using function get_listing()
    vacancies = []
    for page, url in enumerate(urls, start=0):
        s = HTMLSession()
        r = s.get(url)
        listing_container = r.html.find('article')
        r.session.close()
        vacancies.append(get_listing(listing_container))
        # feedback on how parsing status
        print(f'page {page} out of {max_pagination} at cv_bankas parsed')
    
    # return (bytes(json.dumps(vacancies).encode('UTF-8')))
    
    return json.dumps(vacancies).encode('UTF-8')


   
