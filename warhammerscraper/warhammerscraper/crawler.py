from scrapy import spiderloader
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os
import pandas as pd

# Overwrite file
file_path = 'output/warhammer.csv'
if os.path.exists(file_path):
    os.remove(file_path)

# Start up spiders to crawl
process = CrawlerProcess()
spider_loader = spiderloader.SpiderLoader.from_settings(get_project_settings())
for spider_name in spider_loader.list():
    if spider_name == "BaseSpider":
        continue
    process.crawl(spider_loader.load(spider_name))
process.start()

# Remove duplicates
df = pd.read_csv('output/warhammer.csv', encoding = 'ANSI')
cleaned_df = df.drop_duplicates(keep='first')
cleaned_df.to_csv('output/warhammer.csv', index=False, encoding='ANSI')

# Remove duplicated column name
df = pd.read_csv('output/warhammer.csv', encoding = 'ANSI')
df2 = pd.read_csv('output/warhammer.csv', encoding = 'ANSI', header=None)
duplicated_index = df2[df2.duplicated()].index
cleaned_df = df.drop(duplicated_index-1)
cleaned_df.to_csv('output/warhammer.csv', index=False, encoding='ANSI')