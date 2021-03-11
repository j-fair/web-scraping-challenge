import pandas as pd 
from bs4 import BeautifulSoup
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False) 

def scrape():

    browser = init_browser()
    mars_dict = {}

    nasa_html = browser.html
    nasa_soup = BeautifulSoup(nasa_html, "html.parser")
    slide_element = nasa_soup.select_one("ul.item_list li.slide")

    news_title = slide_element.find("div", class_="content_title").get_text()
    news_p = slide_element.find('div',class_='article_teaser_body').get_text()

    jpl_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(jpl_url)

    browser.click_link_by_partial_text('FULL IMAGE')

    try:
        jpl_html = browser.html
        jpl_soup = BeautifulSoup(jpl_html, "html.parser")

        pic_search = jpl_soup.find_all('img', {'class' :'headerimage'})

        for link in pic_search:
            img_path = (link.get('src'))
        
        base_jpl_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'
        featured_img_url = base_jpl_url + img_path
        
    except AttributeError:
            return None

    mars_facts_url = 'https://space-facts.com/mars/'
    browser.visit(mars_facts_url)

    #facts_html = browser.html
    #facts_soup = BeautifulSoup(facts_html, "html.parser")

    try:
        mars_table = pd.read_html("https://space-facts.com/mars/")[0]
    except BaseException:
        return None
    mars_table.columns=["Planet Profile", "Cool Fact"]
    mars_table.set_index("Planet Profile", inplace=True)

    final_mars_table = mars_table.to_html(classes="table table-striped")

    #mars_hemispheres = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    hemi_html = browser.html
    hemi_soup = BeautifulSoup(hemi_html, "html.parser")

    hemisphere_image_urls = []
    hemi_search = hemi_soup.find_all('div', class_="item")

    for hemi in range(len(hemi_search)):
    
        # splinter browser to obtain hemisphere link for image data
        browser.find_by_css("a.product-item h3")[item].click()
    
        hemi_html = browser.html
        hemi_soup = BeautifulSoup(hemi_html, "html.parser")
        base_url = 'https://astrogeology.usgs.gov'
    
        hemi_url = hemi_soup.find('img', class_="wide-image")['src']
        img_url = base_url + hemi_url
    
        img_title = browser.find_by_css('.title').text

        # Adding desired data to variable
        hemisphere_image_urls.append({"title": img_title, "img_url": img_url})
    
        # Browser back to main page
        browser.back()

    mars_dict={
        "news_title":news_title,
        "news_p":news_p,
        "featured_image_url":featured_img_url,
        "fact_table":final_mars_table,
        "hemisphere_images":hemisphere_image_urls
    }


    browser.quit()
    return mars_dict