import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options 
from time import sleep
# import splash
# from scrapy_splash import SplashRequest 


class DivarSpider(scrapy.Spider):
    name = "divar"
    
    start_urls = ["https://divar.ir/s/tehran/buy-residential"]
    
    def parse(self, response):
        driver=webdriver.Chrome()
        driver.get('https://divar.ir/s/tehran/buy-residential')
        driver.implicitly_wait(20)
        
        end_of_scroll=driver.execute_script("return document.body.scrollHeight")
        for i in range(2):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            sleep(2)
            my_scroll=driver.execute_script("return document.body.scrollHeight")
            if my_scroll==end_of_scroll:
                break
            end_of_scroll=my_scroll
            elems = driver.find_elements(By.CSS_SELECTOR,"div.post-card-item-af972.kt-col-6-bee95.kt-col-xxl-4-e9d46 a[href]")
            detail_page_links = [elem.get_attribute('href') for elem in elems]
            
            for link in detail_page_links:
                driver_detail=webdriver.Chrome()
                driver_detail.get(link)
                sleep(2)
                # elems = driver.find_elements(By.XPATH,'/html/body/div[1]/div[2]/div/nav/ol/li[3]/a/span')
                elems = driver.find_elements(By.XPATH,'//html//body//')
                
                break
                # elems = driver.find_elements(By.CSS_SELECTOR','')

                print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                print(elems)
                # element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'div.kt-page-title__title.kt-page-title__title--responsive-sized')))
                #links = [elem.get_attribute("innerHTML") for elem in elems]
                # links=element.text
                #print("---------------------------------------------------")
                #print(links)
                yield {"a": elems}
                        
                # print("---------------------------------------------------------------------------")
                # for element in elems:
                #     print(element.text)
                #     yield element.text
                    
                # yield elems
                # with open('dd.txt', 'a+') as f:
                #     for text in texts:
                #         f.write(text.text+"\n")
                # f.close()
        #     for url in detail_page_links:
        #         yield SplashRequest(url, self.parse_detail, meta={
        #         'splash': {
        #         'endpoint': 'render.html',
        #         'args': {'wait': 0.5}
        #         }
        # })
            # yield from response.follow_all(detail_page_links, self.parse_detail)            
            sleep(2)


    # def parse_detail(self, response):
    #     print("---------------------------------------------------------------------------")
    #     # price = response.css('script::text').getall()[-1]
    #     yield {"price": response.body}
