"""
Usage:
    data = crawl('http://www.google.com')

Flow:
    crawl > crawler > retrieve > process_current_page

# retrieval & processing stage 0
process_current_page:
    breaks down and return current page as
    data[url]
    data[links]
    data[html]

# retrieval & processing stage 1
retrieve:
    takes a URL, navigates to it, then calls process_current_page

# retrieval & processing stage 2
crawler:
    generator object. give a starting URL and other args to crawl

# retrieval & processing stage 3
crawl:
    high-level crawler. pass URL and behaviour defining args
    to have all scraped data returned

[ ] easy method to run function on page text while using retriever
[ ] generator obj for process (retriever)
[ ] markdown formatting
[ ] depth variable for retriever
[ ] fix url comparison fix (are_urls_equivalent)
[ ] add easy display links
[ ] add relation diagram based on links found on site
[ ] check if browser obj is still alive
[ ] add ddgs quick data return or starting point
[ ] add color to notification data when run as script
[ ] add initialization checker to all calls: if self.obj == None:
[x] add function to disect and return web page as dictionary
    [x] url
    [x] body
    [x] links


"""

import functools
import logging
import os
import sys
from urllib.parse import parse_qsl, unquote_plus, urlparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

if getattr(sys, "frozen", False):
    app_dir = os.path.dirname(sys.executable)
else:
    app_dir = os.path.dirname(os.path.realpath(__file__))


log = os.path.join(app_dir, "automata_browser.log")
logging.basicConfig(filename=log, level=logging.INFO)


def log_function_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Calling {func.__name__} with args: {args}, kwargs: {kwargs}")
        result = func(*args, **kwargs)
        logging.info(f"{func.__name__} returned {result}")
        return result

    return wrapper


class web_manager:
    """description: connection manager for information retrieval from the internet"""

    def are_urls_equivalent(url1, url2, protocol_agnostic=True):
        """
        Compares two URLs for equivalency, considering potential variations
        in query parameter order, path encoding, and fragment identifiers.
        """
        if not url1[-1] == "/":
            url1 += "/"
        if not url2[-1] == "/":
            url2 += "/"

        if protocol_agnostic:
            url1 = url1.replace("https://", "http://")
            url2 = url2.replace("https://", "http://")

        parsed1 = urlparse(url1)
        parsed2 = urlparse(url2)

        path1 = unquote_plus(parsed1.path)
        path2 = unquote_plus(parsed2.path)

        query1 = frozenset(parse_qsl(parsed1.query))
        query2 = frozenset(parse_qsl(parsed2.query))

        return (
            parsed1.scheme == parsed2.scheme
            and parsed1.netloc == parsed2.netloc
            and path1 == path2
            and query1 == query2
        )

    class Browser:
        """"""

        @log_function_calls
        def __init__(self, browserObject=None):
            self.obj = browserObject

        @log_function_calls
        def createBrowserInstance(self, *args, **kwargs):
            """"""
            # print("creating selenium browser instance...")
            import atexit

            opts = Options()
            if "headless" in kwargs.keys():
                if kwargs["headless"]:
                    opts.add_argument("-headless")
            browser = webdriver.Firefox(options=opts)
            browser.implicitly_wait(10)
            self.obj = browser
            atexit.register(self.quit)

        @log_function_calls
        def validateBrowserInstance(browser):
            try:
                if type(browser.obj) == webdriver.firefox.webdriver.WebDriver:
                    print("browser creation validated")
                else:
                    raise
            except:
                print("browser creation failed")

        # retrieval & processing stage 0
        @log_function_calls
        def process_current_page(self, link_mode="safe"):
            if self.obj == None:
                print("scraper browser not initialized")

            url = self.obj.current_url
            # print("crawling {}...".format(url))
            WebDriverWait(self.obj, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            ret = 1
            try:
                body = self.obj.find_element(By.TAG_NAME, "body").text
                link_elems = self.obj.find_elements(By.TAG_NAME, "a")

                links = []
                for indx in range(len(link_elems)):
                    link = link_elems[indx].get_attribute("href")
                    if not link in links:
                        links.append(link)

                ret = {"url": url, "html": body, "links": links}
            except:
                print('autobrowser could not retrieve data from {}...'.format(url))

            return ret

        # retrieval & processing stage 1
        @log_function_calls
        def retrieve(self, url=None, headless=True):
            """"""
            if self.obj == None:
                print("scraper browser not initialized")

            if not url == None:
                if not web_manager.are_urls_equivalent(self.obj.current_url, url):
                    # print("navigating to {}...".format(url))
                    self.obj.get(url)

            return self.process_current_page()

        # retrieval & processing stage 2
        @log_function_calls
        def crawler(self, links=None, headless=True, depth=1, max_visited=50):
            """
            crawler > retrieve > process_current_page
            """
            visited = []
            while (len(links) > 0) and (len(visited) <= max_visited):
                link = links.pop()
                if not link in links:
                    data = self.retrieve(link, headless=headless)
                    links += data["links"]
                    visited.append(link)
                    yield (data)

        # retrieval & processing stage 3
        @log_function_calls
        def crawl(self, url):
            data = {}
            for i in self.crawler([url]):
                print(f"{i['url']}\t\t\t\t\t\t\t\r", end="")
                data[i["url"]] = i

            for i in data[list(data)[0]]["html"].split("\n"):
                print(i)

            return data

        @log_function_calls
        def page_inquiry(self, inquiry, chat_func, store=False):
            """
            1. browser = llm.tools.browse()
            2. navigate to webpage you want to inquire about
            3. browser.page_inquiry('what can you tell me about this webpage?', llm.chat)
            """
            WebDriverWait(self.obj, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            element = self.obj.find_element(By.TAG_NAME, "body")
            chat_func(f"{inquiry}\n\n{element.text}")

        def quit(self):
            self.obj.quit()
            self.obj = None


if __name__ == "__main__":
    try:
        import readline
    except ImportError:
        print("Module readline not available.")
    else:
        import rlcompleter

        readline.parse_and_bind("tab: complete")

    if len(sys.argv[1:]) == 0:
        interactive = True
        browser = web_manager.Browser()
        browser.createBrowserInstance(headless=False)
        print("\n[browser] is the automata browser object")
        print("[browser.obj] is the selenium browser object")
        print("\nexamples:")
        print("    browser.retrieve('http://www.facebook.com')")
        print("          is the same as...")
        print("    browser.obj.get('http://www.facebook.com')")
        print("    browser.obj.find_element(By.TAG_NAME, 'body').text")
        print()
    else:
        import argparse

        parser = argparse.ArgumentParser(description="Selenium scaffolding (for web scraping)")
        parser.add_argument(
            "-t",
            "--test",
            action="store_true",
            help="test browser creation and functionality",
        )
        parser.add_argument(
            "-u", "--url", type=str, nargs="?", help="url to extract data from"
        )
        parser.add_argument(
            "-z", "--headless", action="store_true", help="use headless browser"
        )
        parser.add_argument(
            "-i", "--interactive", action="store_true", help="use headless browser"
        )
        parser.add_argument(
            "-s",
            "--script",
            type=str,
            nargs="?",
            help="call auto_browser script from previously created usage",
        )
        args = parser.parse_args()

        if args.test:
            browser = web_manager.Browser()
            browser.createBrowserInstance(headless=False)
            web_manager.Browser.validateBrowserInstance(browser)
            sys.exit()

        if not args.url:
            parser.error("The following arguments are required: -u/--url")
            sys.exit()
        else:
            # better structure for this http/https
            # option to enable this feature or not
            if not args.url.startswith('http'):
                args.url = f'http://{args.url}'

        browser = web_manager.Browser()
        browser.createBrowserInstance(headless=args.headless)
        data = browser.retrieve(args.url)
        sys.stdout.write(data["html"])
        sys.exit()
