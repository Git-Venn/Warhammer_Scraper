Disclaimer: This project is for learning purposes and personal use only. In no way is this to be distributed or used in a commercial setting.

The Warhammer_Scraper crawls the warhammer.com website and scrapes information of all products, then outputs information such as 'name', 'type', 'setting', 'price', 'isInStock' into a .csv file.

This is a python project that utilizes
- Scrapy framework
- Pandas library
- Exchange rate API from https://www.exchangerate-api.com

Steps to run:
1. A .env file containing "X-Algolia-Application-Id" and "X-Algolia-Api-Key" is required. Go to [https://www.warhammer.com/en-US/shop/warhammer-40000/space-marines/black-templars], right-click >> inspect element >> Network >> Fetch/XHR then refresh the page, you should see "queries?x-algolia....", click on it then go to Headers, scroll down and you should have ur values.
2. Create a .env file at the root directory of the project, and put these two values inside.
3. To run the scraper all you have to do is run the "crawler.exe" file located in the [dist] directory, a .csv file will then appear in the output folder. 
