#!/usr/bin/env python3
from actions.base import spaxmController
from actions.scroll import Scroll
from actions.scrollcomments import Scroll_comment
from actions.login import loginAcct
from actions.interactions import Interact
from actions.shill import Shill
import asyncio
import json
import logging
import random
import pandas as pd
from pathlib import Path
from playwright.async_api import Playwright, async_playwright, expect

#Generate a random delay between 3600 and 5400 seconds (1 hour to 1.5 hours)
#     delay = random.randint(3600, 5400)
# asyncio.sleep(random.randint(1600, 2200))


async def shill():
    async with async_playwright() as p:
        # Generate a random delay between 3600 and 5400 seconds (1 hour to 1.5 hours)
        # await asyncio.sleep(random.randint(1600, 2200))

        # browser configs
        browser = await p.firefox.launch(headless=False)
        context = await browser.new_context(
            viewport={"width": 375, "height": 812},  # iPhone X viewport size
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
        )
        # Load the CSV file into a DataFrame
        df = pd.read_csv('data.csv')

        # Iterate over each row using iterrows()
        for index, user in df.iterrows():
            page = await context.new_page()
            page.set_default_timeout(155000)

            controller = spaxmController()
            controller.add_command(loginAcct(page, context, user["email"], user["cookies_file"], "https://x.com/"))
            await controller.execute_commands()


            # try login
            logging.info(f'{user["email"]}, {user["cookies_file"]}')
            # await page.goto('https://x.com/home')
            # page = await context.new_page()
            page.set_default_timeout(155000)

            controller.clear_commands()

            # # each_post_len = len(each_post)
            new = await context.new_page()
            await new.goto('https://x.com')

            # replace with multiple keywords you want to search
            all_search = ['flipper zero', 'Flipper Zero', 'FlipperZero']
            search = random.choice(all_search)
            # shill section
            controller.add_command(Shill(new, search))
            await controller.execute_commands()
            await new.close()
            await page.close()

    await context.close()


if __name__ == "__main__":
    asyncio.run(shill())
