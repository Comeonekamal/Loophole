import random
import filenomenclature
import time
from playwright.sync_api import sync_playwright

#Make sure you have run requirements.txt playwright install once before running this script.

def run(url):
   p = sync_playwright().start()
   browser =  p.chromium.launch()
   context =  browser.new_context()
   page =  context.new_page()

   urls = []

   def retrieve_url(response):
      res = response.url
      if "files.1drv.com" in res:
         #urls.add(res)
         type = response.header_values('content-type')
         fname = random.choice(filenomenclature.filters)

         ext = type[0].split('/')
         filename = '/' + fname + '.' + ext[1]
         permalink = res.replace('?', filename)

         urls.append(permalink)


      


   page.on("response", retrieve_url)
   page.goto(url= url, timeout=20000, wait_until="networkidle")
   time.sleep(2)
   page.context.close
   browser.close()

   n_urls = list(set(urls))   
      
   print()
   print(n_urls[0])
         
   
if __name__=='__main__':
   
   url = input("Enter your Onedrive Share-Link: ")

   run(url)