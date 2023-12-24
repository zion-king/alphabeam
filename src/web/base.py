"""Beautiful Soup Web scraper."""

import logging
from typing import Any, Callable, Dict, List, Literal, Optional, Tuple, cast
from urllib.parse import urljoin

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document

logger = logging.getLogger(__name__)

"""Simple Web scraper."""
from langchain.requests import RequestsWrapper

logger = logging.getLogger(__name__)

"""Readability Web reader."""
import unicodedata
from pathlib import Path
from llama_index.node_parser.interface import TextSplitter

path = Path(__file__).parent / "Readability.js"

readabilityjs = ""
with open(path, "r") as f:
    readabilityjs = f.read()

inject_readability = f"""
    (function(){{
      {readabilityjs}
      function executor() {{
        return new Readability({{}}, document).parse();
      }}
      return executor();
    }}())
"""


def nfkc_normalize(text: str) -> str:
    return unicodedata.normalize("NFKC", text)


class ReadabilityWebPageReader(BaseReader):
    """Readability Webpage Loader

    Extracting relevant information from a fully rendered web page.
    During the processing, it is always assumed that web pages used as data sources contain textual content.

    1. Load the page and wait for it rendered. (playwright)
    2. Inject Readability.js to extract the main content.

    Args:
        proxy (Optional[str], optional): Proxy server. Defaults to None.
        wait_until (Optional[Literal["commit", "domcontentloaded", "load", "networkidle"]], optional): Wait until the page is loaded. Defaults to "domcontentloaded".
        text_splitter (TextSplitter, optional): Text splitter. Defaults to None.
        normalizer (Optional[Callable[[str], str]], optional): Text normalizer. Defaults to nfkc_normalize.
    """

    def __init__(
        self,
        proxy: Optional[str] = None,
        wait_until: Optional[
            Literal["commit", "domcontentloaded", "load", "networkidle"]
        ] = "domcontentloaded",
        text_splitter: Optional[TextSplitter] = None,
        normalize: Optional[Callable[[str], str]] = nfkc_normalize,
    ) -> None:
        self._launch_options = {
            "headless": True,
        }
        self._wait_until = wait_until
        if proxy:
            self._launch_options["proxy"] = {
                "server": proxy,
            }
        self._text_splitter = text_splitter
        self._normalize = normalize

    def load_data(self, url: str) -> List[Document]:
        """render and load data content from url.

        Args:
            url (str): URL to scrape.

        Returns:
            List[Document]: List of documents.

        """
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(**self._launch_options)

            article = self.scrape_page(
                browser,
                url,
            )
            extra_info = {
                key: article[key]
                for key in [
                    "title",
                    "length",
                    "excerpt",
                    "byline",
                    "dir",
                    "lang",
                    "siteName",
                ]
            }

            if self._normalize is not None:
                article["textContent"] = self._normalize(article["textContent"])
            texts = []
            if self._text_splitter is not None:
                texts = self._text_splitter.split_text(article["textContent"])
            else:
                texts = [article["textContent"]]

            browser.close()

            return [Document(text=x, extra_info=extra_info) for x in texts]

    def scrape_page(
        self,
        browser: Any,
        url: str,
    ) -> Dict[str, str]:
        """Scrape a single article url.

        Args:
            browser (Any): a Playwright Chromium browser.
            url (str): URL of the article to scrape.

        Returns:
            Ref: https://github.com/mozilla/readability
            title: article title;
            content: HTML string of processed article content;
            textContent: text content of the article, with all the HTML tags removed;
            length: length of an article, in characters;
            excerpt: article description, or short excerpt from the content;
            byline: author metadata;
            dir: content direction;
            siteName: name of the site.
            lang: content language

        """
        from playwright.sync_api._generated import Browser

        browser = cast(Browser, browser)
        page = browser.new_page(ignore_https_errors=True)
        page.set_default_timeout(60000)
        page.goto(url, wait_until=self._wait_until)

        r = page.evaluate(inject_readability)

        page.close()
        print("scraped:", url)

        return r

def _substack_reader(soup: Any, **kwargs) -> Tuple[str, Dict[str, Any]]:
    """Extract text from Substack blog post."""
    extra_info = {
        "Title of this Substack post": soup.select_one("h1.post-title").getText(),
        "Subtitle": soup.select_one("h3.subtitle").getText(),
        "Author": soup.select_one("span.byline-names").getText(),
    }
    text = soup.select_one("div.available-content").getText()
    return text, extra_info


def _readthedocs_reader(soup: Any, url: str, **kwargs) -> Tuple[str, Dict[str, Any]]:
    """Extract text from a ReadTheDocs documentation site"""
    import requests
    from bs4 import BeautifulSoup

    links = soup.find_all("a", {"class": "reference internal"})
    rtd_links = []

    for link in links:
        rtd_links.append(link["href"])
    for i in range(len(rtd_links)):
        if not rtd_links[i].startswith("http"):
            rtd_links[i] = urljoin(url, rtd_links[i])

    texts = []
    for doc_link in rtd_links:
        page_link = requests.get(doc_link)
        soup = BeautifulSoup(page_link.text, "html.parser")
        try:
            text = soup.find(attrs={"role": "main"}).get_text()

        except IndexError:
            text = None
        if text:
            texts.append("\n".join([t for t in text.split("\n") if t]))
    return "\n".join(texts), {}


def _readmedocs_reader(
    soup: Any, url: str, include_url_in_text: bool = True
) -> Tuple[str, Dict[str, Any]]:
    """Extract text from a ReadMe documentation site"""
    import requests
    from bs4 import BeautifulSoup

    links = soup.find_all("a")
    docs_links = [link["href"] for link in links if "/docs/" in link["href"]]
    docs_links = list(set(docs_links))
    for i in range(len(docs_links)):
        if not docs_links[i].startswith("http"):
            docs_links[i] = urljoin(url, docs_links[i])

    texts = []
    for doc_link in docs_links:
        page_link = requests.get(doc_link)
        soup = BeautifulSoup(page_link.text, "html.parser")
        try:
            text = ""
            for element in soup.find_all("article", {"id": "content"}):
                for child in element.descendants:
                    if child.name == "a" and child.has_attr("href"):
                        if include_url_in_text:
                            url = child.get("href")
                            if url is not None and "edit" in url:
                                text += child.text
                            else:
                                text += (
                                    f"{child.text} (Reference url: {doc_link}{url}) "
                                )
                    elif child.string and child.string.strip():
                        text += child.string.strip() + " "

        except IndexError:
            text = None
            logger.error(f"Could not extract text from {doc_link}")
            continue
        texts.append("\n".join([t for t in text.split("\n") if t]))
    return "\n".join(texts), {}


def _gitbook_reader(
    soup: Any, url: str, include_url_in_text: bool = True
) -> Tuple[str, Dict[str, Any]]:
    """Extract text from a ReadMe documentation site"""
    import requests
    from bs4 import BeautifulSoup

    links = soup.find_all("a")
    docs_links = [link["href"] for link in links if "/docs/" in link["href"]]
    docs_links = list(set(docs_links))
    for i in range(len(docs_links)):
        if not docs_links[i].startswith("http"):
            docs_links[i] = urljoin(url, docs_links[i])

    texts = []
    for doc_link in docs_links:
        page_link = requests.get(doc_link)
        soup = BeautifulSoup(page_link.text, "html.parser")
        try:
            text = ""
            text = soup.find("main")
            clean_text = clean_text = ", ".join([tag.get_text() for tag in text])
        except IndexError:
            text = None
            logger.error(f"Could not extract text from {doc_link}")
            continue
        texts.append(clean_text)
    return "\n".join(texts), {}


DEFAULT_WEBSITE_EXTRACTOR: Dict[
    str, Callable[[Any, str], Tuple[str, Dict[str, Any]]]
] = {
    "substack.com": _substack_reader,
    "readthedocs.io": _readthedocs_reader,
    "readme.com": _readmedocs_reader,
    "gitbook.io": _gitbook_reader,
}


class BeautifulSoupWebReader(BaseReader):
    """BeautifulSoup web page reader.

    Reads pages from the web.
    Requires the `bs4` and `urllib` packages.

    Args:
        website_extractor (Optional[Dict[str, Callable]]): A mapping of website
            hostname (e.g. google.com) to a function that specifies how to
            extract text from the BeautifulSoup obj. See DEFAULT_WEBSITE_EXTRACTOR.
    """

    def __init__(
        self,
        website_extractor: Optional[Dict[str, Callable]] = None,
    ) -> None:
        """Initialize with parameters."""
        self.website_extractor = website_extractor or DEFAULT_WEBSITE_EXTRACTOR

    def load_data(
        self,
        urls: List[str],
        custom_hostname: Optional[str] = None,
        include_url_in_text: Optional[bool] = True,
    ) -> List[Document]:
        """Load data from the urls.

        Args:
            urls (List[str]): List of URLs to scrape.
            custom_hostname (Optional[str]): Force a certain hostname in the case
                a website is displayed under custom URLs (e.g. Substack blogs)
            include_url_in_text (Optional[bool]): Include the reference url in the text of the document

        Returns:
            List[Document]: List of documents.

        """
        from urllib.parse import urlparse

        import requests
        from bs4 import BeautifulSoup

        documents = []
        for url in urls:
            try:
                page = requests.get(url)
            except Exception:
                raise ValueError(f"One of the inputs is not a valid url: {url}")

            hostname = custom_hostname or urlparse(url).hostname or ""

            soup = BeautifulSoup(page.content, "html.parser")

            data = ""
            extra_info = {"URL": url}
            if hostname in self.website_extractor:
                data, metadata = self.website_extractor[hostname](
                    soup=soup, url=url, include_url_in_text=include_url_in_text
                )
                extra_info.update(metadata)

            else:
                data = soup.getText()

            documents.append(Document(text=data, extra_info=extra_info))

        return documents



class SimpleWebPageReader(BaseReader):
    """Simple web page reader.

    Reads pages from the web.

    Args:
        html_to_text (bool): Whether to convert HTML to text.
            Requires `html2text` package.

    """

    def __init__(self, html_to_text: bool = False) -> None:
        """Initialize with parameters."""
        self._html_to_text = html_to_text

    def load_data(self, urls: List[str]) -> List[Document]:
        """Load data from the input directory.

        Args:
            urls (List[str]): List of URLs to scrape.

        Returns:
            List[Document]: List of documents.

        """
        if not isinstance(urls, list):
            raise ValueError("urls must be a list of strings.")
        requests = RequestsWrapper()
        documents = []
        for url in urls:
            response = requests.get(url)
            if self._html_to_text:
                import html2text

                response = html2text.html2text(response)

            documents.append(Document(text=response))

        return documents