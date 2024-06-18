from actions.base import Base
import logging
from bs4 import BeautifulSoup
import random
import asyncio

# Configure logging to display messages to the terminal
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.StreamHandler()])


class Scroll_comment(Base):
    """
        scroll through posts on a page
    """
    def __init__(self, page):
        self.page = page

    # beautiful soup to get each post link from a scroll
    async def post_hrefs(self, all_divs: list):
        all_hrefs = []
        for div in all_divs:
            anchor_tag = div.find('a')
            logging.info("Extracting comment link from anchor tag")
            if anchor_tag:
                href = anchor_tag.get('href')
                if href:
                    all_hrefs.append(href)
        return all_hrefs

    async def get_urls(self, all_links=None):
        post_urls = []
        if all_links is not None:
            links_len = len(all_links)
            for i in range(links_len):
                link = 'https://x.com' + all_links[i]
                logging.info(f"Comment Link {i} {link}")
                post_urls.append(link)
            return post_urls

    async def scroll_to_end(self):
        last_height = await self.page.evaluate("document.body.scrollHeight")
        while True:
            await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
            await asyncio.sleep(random.randint(1, 2)) # Adjust wait time if needed

            # new_height = await self.page.evaluate("document.body.scrollHeight")
            # if last_height == new_height:
            #     break  # Stop scrolling if heights are the same (reached the end)
            # last_height = new_height

    async def execute(self):
        await self.scroll_to_end()


        # Get the page content
        html_code = await self.page.content()

        # get all tweets or articles on each page scroll
        soup = BeautifulSoup(html_code, 'html.parser')

        # Find all divs with the specified class
        all_divs = soup.find_all('div', class_='css-175oi2r r-18u37iz r-1q142lx')
        logging.info(f"Comments {len(all_divs)}")

        # Extract href attributes from anchor tags within each div
        all_links = await self.post_hrefs(all_divs)
        # Print all extracted hrefs
        print(len(all_links))
        # visit each extracted link one after the other open and interact in new context
        each_post = await self.get_urls(all_links)
        each_post_len = len(each_post)
        return each_post



