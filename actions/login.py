#!/usr/bin/env python3
from actions.base import Base
from playwright.async_api import Page
import logging
import asyncio
import json
import random
import os
from pathlib import Path
# from get_user_cookies import login


# Configure logging to display messages to the terminal
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.StreamHandler()])


parent_dir = os.path.dirname(os.path.dirname(__file__))  # Get the parent directory of the current directory
cookies_filepath = os.path.join(parent_dir, "cookies.json")


class loginAcct(Base):
    """
        if cookies exist load up user cookies
        login an account with required inputs from pages
    """

    def __init__(self, page, context, user, filename, url: str):
        self.page = page
        self.url = url
        self.user = user
        self.context = context
        self.filename = filename
        logging.info("initialized successfully")

    # load cookies if it exists
    async def load_cookies(self):
        base_folder = Path(__name__).resolve().parent
        file_path = f'{base_folder}/cookies/{self.filename}'
        # load cookies of the user from the file
        with open(file_path, "r") as f:
            # cookies_data = f.read()
            # cookies = [{"name": c.split("=")[0], "value": c.split("=")[1], "domain": "x.com", "path": "/"}
            #            for c in cookies_data.split(",")]
            cookies = json.load(f)
            await self.context.add_cookies(cookies)
            logging.info(f"Cookies loaded for {self.user} successfully")

    # login if it auto logs out
    @staticmethod
    async def sign_in(page, context):
        login_button = await page.get_by_test_id("loginButton").is_visible()

        if login_button:
            await page.get_by_test_id("loginButton").click()
            logging.info("Login button spotted succesfully")
        else:
            logging.error("Login button not found")
            return "Not Visible"
        await page.locator("input[name='text']").click()
        await asyncio.sleep(random.randint(2, 5))
        await page.locator("input[name='text']").fill("@gmail.com")

        await page.get_by_role("button", name="Next").click()
        await page.get_by_label("Password", exact=True).click()
        await page.get_by_label("Password", exact=True).fill("")
        await page.get_by_test_id("controlView").get_by_test_id("LoginForm_Login_Button").click()

        # Wait for login to complete
        await asyncio.sleep(10)

        # Save the login cookies
        async def save_cookies(file_path=cookies_filepath):
            cookies = await context.cookies()
            with open(file_path, 'w') as f:
                json.dump(cookies, f)

        await save_cookies(context)

    async def execute(self):
        await self.load_cookies()
        logging.info(f"cookies loaded for {self.user} to session")
        await asyncio.sleep(random.randint(2, 5))
        await self.page.goto(self.url)
        await self.page.wait_for_load_state()
        login_button = await self.page.get_by_test_id("loginButton").is_visible()
        if login_button:
            logging.error("Session continued failed for user")
            # await login()
            # await self.sign_in(self.page, self.context)
        logging.info(f"Session continued successful for {self.user}")
        await self.page.wait_for_load_state()