from urllib.parse import urlencode

import scrapy
from bs4 import BeautifulSoup


class BlogsSpider(scrapy.Spider):
    name = "narutospider"
    api_base = "https://naruto.fandom.com/api.php"

    custom_settings = {
        "USER_AGENT": (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0.0.0 Safari/537.36"
        ),
        "ROBOTSTXT_OBEY": False,
    }

    def build_api_url(self, **params):
        return f"{self.api_base}?{urlencode(params)}"

    def start_requests(self):
        url = self.build_api_url(
            action="query",
            list="categorymembers",
            cmtitle="Category:Jutsu",
            cmlimit="500",
            cmtype="page",
            format="json",
        )
        yield scrapy.Request(url=url, callback=self.parse_category)

    def parse_category(self, response):
        payload = response.json()

        for member in payload.get("query", {}).get("categorymembers", []):
            title = member.get("title")
            if not title:
                continue

            detail_url = self.build_api_url(
                action="parse",
                page=title,
                prop="text",
                format="json",
                formatversion="2",
            )
            yield scrapy.Request(detail_url, callback=self.parse_jutsu)

        continuation = payload.get("continue", {}).get("cmcontinue")
        if continuation:
            next_url = self.build_api_url(
                action="query",
                list="categorymembers",
                cmtitle="Category:Jutsu",
                cmlimit="500",
                cmtype="page",
                cmcontinue=continuation,
                format="json",
            )
            yield scrapy.Request(next_url, callback=self.parse_category)

    def parse_jutsu(self, response):
        payload = response.json().get("parse", {})
        jutsu_name = payload.get("title", "").strip()
        article_html = payload.get("text", "")

        if not article_html:
            return

        soup = BeautifulSoup(article_html, "html.parser")

        jutsu_type = ""
        aside = soup.find("aside")

        if aside:
            classification = aside.select_one("[data-source='classification'] .pi-data-value")
            if classification:
                jutsu_type = classification.get_text(" ", strip=True)
            else:
                for cell in aside.select("div.pi-data"):
                    heading = cell.select_one("h3.pi-data-label")
                    value = cell.select_one("div.pi-data-value")
                    if not heading or not value:
                        continue
                    if heading.get_text(strip=True) == "Classification":
                        jutsu_type = value.get_text(" ", strip=True)
                        break
            aside.decompose()

        jutsu_description = soup.get_text("\n", strip=True)
        jutsu_description = jutsu_description.split("Trivia", 1)[0].strip()

        return {
            "jutsu_name": jutsu_name,
            "jutsu_type": jutsu_type,
            "jutsu_description": jutsu_description,
            "source_url": response.url,
        }