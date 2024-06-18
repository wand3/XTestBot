from actions.base import Base
import logging
import random
import asyncio
# Configure logging to display messages to the terminal
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.StreamHandler()])


class Interact(Base):

    def __init__(self, new):
        self.new = new

    # go back
    async def go_back(self):
        goBack = self.new.get_by_test_id('app-bar-back')
        goBackPos = await goBack.bounding_box()
        await self.new.mouse.move(goBackPos["x"] + goBackPos["width"] / 2, goBackPos["y"] + goBackPos["height"] / 2)
        await self.new.mouse.down()
        await self.new.mouse.up()
        logging.info("Back to home new")
        await asyncio.sleep(random.randint(4, 6))

    # has keywords
    async def has_text(self):
        tweetText = await self.new.query_selector_all('div[data-testid="tweetText"]')
        words = ['is', 'the', 'our', 'i']


    # like
    async def like(self):
        await self.new.wait_for_load_state()
        likeTweet = await self.new.query_selector_all('button[data-testid="like"]')
        unlikeTweet = await self.new.query_selector_all('button[data-testid="unlike"]') or None

        if likeTweet:
            # pass

            await likeTweet[0].click()
            logging.info("Liking post successful")
            await asyncio.sleep(random.randint(2, 4))

            self.new.on("dialog", lambda dialog: dialog.accept())

    # retweet
    async def retweet(self):
        retweet = await self.new.query_selector_all('button[data-testid = "retweet"]')
        await retweet[0].click(delay=2000)
        retweetConfirm = self.new.get_by_test_id("retweetConfirm")

        await asyncio.sleep(random.randint(1, 3))
        retweetConfirmPos = await retweetConfirm.bounding_box()
        await self.new.mouse.move(retweetConfirmPos["x"] + retweetConfirmPos["width"] / 2,
                                  retweetConfirmPos["y"] + retweetConfirmPos["height"] / 2)
        await self.new.mouse.down()
        await self.new.mouse.up()
        await asyncio.sleep(random.randint(2, 3))
        logging.info("Retweet post successful")

    # reply
    async def reply(self):
        reply = await self.new.query_selector_all('button[data-testid="reply"]')
        if reply:
            # logging.info(reply)

            await reply[0].click()
            # await self.new.on("dialog", lambda dialog: dialog.accept())

            await self.new.wait_for_load_state()
            await asyncio.sleep(random.randint(2, 4))

            # get reply input box
            replyInput = self.new.get_by_test_id("tweetTextarea_0")
            replyInputPos = await replyInput.bounding_box()
            await self.new.mouse.move(replyInputPos["x"] + replyInputPos["width"] / 2,
                                      replyInputPos["y"] + replyInputPos["height"] / 2)
            await self.new.mouse.down()
            await self.new.mouse.up()
            await self.new.keyboard.type("kkkkkk", delay=200)
            await asyncio.sleep(random.randint(2, 3))

            # send reply
            tweetReply = self.new.get_by_test_id("tweetTextarea_0")
            tweetReplyPos = await tweetReply.bounding_box()
            await self.new.mouse.move(tweetReplyPos["x"] + tweetReplyPos["width"] / 2,
                                      tweetReplyPos["y"] + tweetReplyPos["height"] / 2)
            await self.new.mouse.down()
            await self.new.mouse.up()
            await asyncio.sleep(random.randint(1, 3))
            # click tweet for reply
            # await expect(self.new.get_by_test_id("tweetButton")).to_be_visible()
            await self.new.get_by_test_id("tweetButton").click()
            await self.new.wait_for_load_state()
            logging.info("Post reply successful")
            await asyncio.sleep(random.randint(4, 9))

    # bookmark
    async def bookmark(self):
        tweetBookmark = self.new.get_by_test_id("bookmark")
        tweetBookmarkPos = await tweetBookmark.bounding_box()
        await self.new.mouse.move(tweetBookmarkPos["x"] + tweetBookmarkPos["width"] / 2,
                                  tweetBookmarkPos["y"] + tweetBookmarkPos["height"] / 2)
        await self.new.mouse.down()
        await self.new.mouse.up()
        await self.new.wait_for_load_state()
        await asyncio.sleep(random.randint(1, 3))
        logging.info("Bookmark successful")

    async def execute(self):
        await self.new.wait_for_load_state()
        await self.like()
        await asyncio.sleep(random.randint(1, 2))
        # await self.reply()


