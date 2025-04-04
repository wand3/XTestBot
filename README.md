## <a name="X">🤖 X Automated Test / Bot</a>

An Automated test for X social media built using the Command Pattern of Software Design which is well suited for Bot making which mimics human interaction on the X platform it can be equiped further with different Screen Viewports, AI, Proxies, Browser user agents and more actions performed by users

## <a name="tech-stack">⚙️ Technologies</a>
- Python
- Playwright
- BeautifulSoup4
- Bash

## <a name="features">🔋 Features</a>

👉 **Interactions**: Test and make interactions such as Scroll, Like, unlike, retweet, unretweet, and Comment can also be customized further.

👉 **Post**: Test and make text and image tweets or a combination of both

👉 **Search**: Search for tweets by keywords and also seacrch for particular keywords in tweets before interactions

👉 **Account**: Can run Single or Multiple accounts.

👉 **Logging**: Logging error and success messages to identify succeess or failure of actions

👉 **Database**: CSV with Dataframes

👉 **Authentication**: Username or email for login and Uses cookies for repeat login to speed up authentication
                    N.B. 2FA is not implemented in this code

and many more, including code architecture and reusability

## <a name="quick-start">🤸 Quick Start</a>

Follow these steps to set up the project locally on your machine.

**Prerequisites**

Make sure you have the following installed on your machine:

- Git
- Python
- Playwright (Firefox driver)

**Installation Backend**

```bash
git clone https://github.com/wand3/XTest_Bot.git
```
1. create a python virtual environment and activate it
2.
```bash
  pip install -r requirements.txt
```
3. Run the below command to save account login and cookies user_credentials goes to data.csv and cookies goes to /cookies for each account
```bash
python3 get_user_cookies.py
```
4. edit main-1.py to input your search keywords and comments.txt to input various comments you want to make on posts then run
```bash
python3 main-1.py
```
5. To make post you can add images to the post_images folder and edit make_post.py to add post text then
```bash
python3 make_post.py
```

