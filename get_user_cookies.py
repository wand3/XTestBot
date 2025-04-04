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

import storage
from storage import create_record

# Configure logging to display messages to the terminal
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.StreamHandler()])


# get number of items in the new cookies directory
async def get_files_count():
    """
        get the number of cookies in the directory and assign its last number to new acctcookies
        :return int
    """
    # get base folder of the running application
    base_folder = Path(__name__).resolve().parent
    directory = Path(f'/{base_folder}/cookies')
    files = [f for f in directory.iterdir() if f.is_file()]
    return len(files)


async def save_cookies(context, email, password):
    last = await get_files_count()
    cookies = await context.cookies()
    # Save the login cookies
    base_folder = Path(__name__).resolve().parent
    file_path = f'/{base_folder}/cookies/cookies-{last}.json'
    with open(file_path, 'w') as f:
        json.dump(cookies, f)

    new_data = [{'email': f'{email}', 'password': f'{password}', 'cookies_file': f'cookies-{last}.json'}]
    create_record(filename=storage.filename, new_data=new_data)


# handle and dismiss dialogs
async def handle_dialog(dialog):
    print(dialog.message)
    await dialog.dismiss()


async def login_save_cookies(page, context, email_or_username, username, password):
    """
    logs in with cookies stored in file
    :param username:
    :param email_or_username:
    :param context:
    :param page:
    :param password:
    :return:
    """

    # navigate to login page to check if user already logged in
    await page.goto('https://x.com/')
    # await page.wait_for_load_state()
    login_user = await page.get_by_test_id("loginButton").is_visible()

    if login_user:
        await page.get_by_test_id("loginButton").click()
        await page.locator("input[name='text']").click()
        await asyncio.sleep(random.randint(2, 5))
        await page.locator("input[name='text']").fill(email_or_username)

        # Locate the heading with id and get the text content
        # header_text = await page.get_by_id("modal-header").inner_text()
        # logging.error(f"header text {header_text}")

        # Correct, only matches the <article> element
        header_text = await page.query_selector('#modal-header')
        logging.error(f"header text {header_text}")
        if header_text:
            # Select the input field and fill it with the username
            logging.info("header seen success!")
            await page.locator('input[name="text"]').click()
            await page.locator('input[name="text"]').fill(username)

        await page.get_by_role("button", name="Next").click()
        await page.get_by_label("Password", exact=True).click()
        await page.get_by_label("Password", exact=True).fill(password)
        # close blocking for login
        await page.get_by_test_id("xMigrationBottomBar").click()

        await page.get_by_test_id("controlView").get_by_test_id("LoginForm_Login_Button").click()

        # check if requesting a different login method
        # find the step here and execute
        # Wait for login to complete
        await asyncio.sleep(10)
        # save cookies for the user
        await save_cookies(context, email_or_username, password)
        return True
    else:
        logging.error(f"Login FAILED for {email_or_username}")
        return False


async def login():
    async with async_playwright() as p:
        # browser configs
        browser = await p.firefox.launch(headless=False)
        context = await browser.new_context(
            viewport={"width": 375, "height": 812},  # iPhone X viewport size
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
        )

        page = await context.new_page()
        page.set_default_timeout(55000)

        email_or_username = input("Enter username or email: ")

        username = input("Enter username: ")

        password = input("Enter password: ")

        # take count of number of cookies files in folder and user its len index to suffix cookies-(suffix).json
        if email_or_username and password and username:
            value = await login_save_cookies(page, context, email_or_username, username, password)
            if value is False:
                logging.error("Saving cookies failed")
            if value is True:
                logging.info('OPERATION SUCCESSFUL!')
                await asyncio.sleep(random.randint(2, 5))
                from main import shill
                await shill()
        await context.close()
        # provide name and password
        return 'both username and password must be given'

asyncio.run(login())
