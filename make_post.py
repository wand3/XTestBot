#!/usr/bin/env python3

import os
import typing
import asyncio
import json
import logging
import random
from playwright.async_api import Playwright, async_playwright, expect
import time
import re
# Using pathlib - chainable and intuitive
from pathlib import Path
import pandas as pd

import storage
from storage import create_record

# Configure logging to display messages to the terminal
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.StreamHandler()])


# handle and dismiss dialogs
async def handle_dialog(dialog):
    print(dialog.message)
    await dialog.dismiss()


async def make_post(new):
    await asyncio.sleep(random.randint(1, 3))
    await new.goto('https://x.com/compose/post')
    await new.wait_for_load_state()
    logging.info("Post tweet page successful")

    await new.get_by_test_id('tweetTextarea_0_label').click()
    # comment = get_random_comment(file_path='comments.txt')
    logging.info('Text area tweet selected successful')
    comment = 'So, let\'s kickstart today with a smile and conquer our goal'
    await new.keyboard.type(comment, delay=100)
    await new.get_by_test_id('tweetTextarea_0_label').press_sequentially(comment)
    await asyncio.sleep(random.randint(2, 3))
    logging.info("Type Post tweet successful")

    # send image or other accepted formats
    # filename = user["cookies_file"]
    base_folder = Path(__name__).resolve().parent
    file_path = f'{base_folder}/post_images/tw-1.jpeg'
    logging.info(f"image path successful {file_path}")

    # photo = await new.get_by_label("Add photos or video").filter(has=new.get_by_test_id("fileInput"))
    # await new.get_by_label("Add photos or video").click()
    photo = await new.query_selector('input[type="file"]')
    logging.info(f"input {photo}")

    await photo.set_input_files(file_path)
    await asyncio.sleep(random.randint(2, 3))

    await asyncio.sleep(random.randint(3, 8))
    logging.info(f"input image successful")

    await new.get_by_test_id("tweetButton").click()
    await new.wait_for_load_state()
    logging.info("Post tweet successful")
    await asyncio.sleep(random.randint(4, 9))


# goto profile page
async def user_profile(new):
    await new.get_by_test_id("DashButton_ProfileIcon_Link").click()
    await new.wait_for_load_state()
    logging.info("user profile image click successful")

    await asyncio.sleep(random.randint(4, 9))

    await new.locator('span', has_text='Profile').click()
    await new.wait_for_load_state()
    logging.info("user profile load successful")

    await asyncio.sleep(random.randint(4, 9))


async def grow():
    async with async_playwright() as p:
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
            await asyncio.sleep(random.randint(1, 3))
            await page.goto('https://x.com/compose/post')
            await page.wait_for_load_state()


asyncio.run(grow())
