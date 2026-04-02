# In-Depth Beginner Tutorial: `jutsu_crawler.py` (Scrapy + BeautifulSoup + MediaWiki API)

This tutorial is written for a complete beginner.

Goal: understand **how this crawler works**, **why each function exists**, **what each callback does**, and **how Scrapy + BeautifulSoup cooperate** when scraping Naruto jutsu data from the MediaWiki API.

---

## 1) Big Picture First (What are we building?)

You have a Scrapy spider that:

1. Calls the MediaWiki API to get pages in `Category:Jutsu`.
2. For each page title, calls the API again to get the rendered article HTML.
3. Uses BeautifulSoup to parse that HTML and extract:
   - `jutsu_name`
   - `jutsu_type`
   - `jutsu_description`
4. Returns dictionary items, and Scrapy writes them to `data/musab.jsonl`.

Important: You switched from scraping regular fandom page URLs (blocked by 403) to API endpoints (`api.php`) that respond successfully.

---

## 2) What to Install (and why)

Inside your activated virtual environment:

```bash
pip install scrapy beautifulsoup4
```

### Why these packages?

- `scrapy`
  - Framework for crawling many pages efficiently.
  - Handles request scheduling, callbacks, retries, throttling, exporting items, and more.
- `beautifulsoup4`
  - HTML parser helper.
  - Lets you locate tags and extract clean text from HTML.

### Optional parser engine (faster HTML parsing)

```bash
pip install lxml
```

BeautifulSoup can use Python’s built-in parser (`html.parser`) which is fine for tutorial use. `lxml` is often faster.

---

## 3) Helpful Docs to Read Alongside

If you want the same “tutorial depth” as a video course, these docs are excellent:

### Scrapy docs

- Getting started: https://docs.scrapy.org/en/latest/intro/overview.html
- Spider basics: https://docs.scrapy.org/en/latest/topics/spiders.html
- Request/Response: https://docs.scrapy.org/en/latest/topics/request-response.html
- Selectors: https://docs.scrapy.org/en/latest/topics/selectors.html
- Feed exports (`-o file.jsonl`): https://docs.scrapy.org/en/latest/topics/feed-exports.html
- Settings: https://docs.scrapy.org/en/latest/topics/settings.html

### BeautifulSoup docs

- Official docs: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

### MediaWiki API docs

- Main API help: https://www.mediawiki.org/wiki/API:Main_page
- Category members query: https://www.mediawiki.org/wiki/API:Categorymembers
- Parse endpoint: https://www.mediawiki.org/wiki/API:Parsing_wikitext

---

## 4) The Full Code We Are Explaining

```python
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
```

---

## 5) Line-by-Line Thinking (Beginner style)

### `from urllib.parse import urlencode`

- We need to build URL query strings safely.
- If a page title has spaces or punctuation, `urlencode` converts it properly.
- Example: `Body Flicker Technique` becomes URL-safe text.

### `import scrapy`

- Imports Scrapy framework.
- Gives us `scrapy.Spider`, `scrapy.Request`, `response` helpers, etc.

### `from bs4 import BeautifulSoup`

- Imports BeautifulSoup parser.
- We use it only in `parse_jutsu` to parse article HTML returned by API.

---

## 6) Spider Class and Identity

### `class BlogsSpider(scrapy.Spider):`

- A spider is your crawling robot.
- In Scrapy, spiders are classes that define crawl behavior.

### `name = "narutospider"`

- Unique spider name identifier.
- Scrapy uses this name internally.

### `api_base = "https://naruto.fandom.com/api.php"`

- Single source of truth for base API endpoint.
- Makes code easier to update if endpoint changes.

---

## 7) `custom_settings` (Important in real crawls)

```python
custom_settings = {
    "USER_AGENT": (...),
    "ROBOTSTXT_OBEY": False,
}
```

- `USER_AGENT`
  - Some sites treat generic crawler user agents more strictly.
  - Browser-like user agent helps reduce immediate blocking patterns.
- `ROBOTSTXT_OBEY`
  - Set to `False` here for tutorial flow.
  - In production/ethical crawling, you should review and respect site policies and legal boundaries.

Note: `custom_settings` applies only to this spider, not globally.

---

## 8) Utility Method: `build_api_url`

```python
def build_api_url(self, **params):
    return f"{self.api_base}?{urlencode(params)}"
```

### Why this function exists

- You build many API URLs with different query parameters.
- This method avoids copy-paste mistakes.
- Keeps URL construction centralized and clean.

### `**params` explained like beginner

- `**params` means: accept any number of named arguments.
- It becomes a Python dictionary.

Example call:

```python
self.build_api_url(action="query", format="json")
```

Internally behaves like:

```python
params = {"action": "query", "format": "json"}
```

Then `urlencode(params)` turns dictionary into query string:

```text
action=query&format=json
```

---

## 9) Crawl Entry Point: `start_requests`

```python
def start_requests(self):
    url = self.build_api_url(...)
    yield scrapy.Request(url=url, callback=self.parse_category)
```

### What happens when spider starts?

- Scrapy asks your spider: “What first request should I send?”
- `start_requests` returns that initial request.

### Parameters used

- `action="query"`: tells MediaWiki API we are doing a query operation.
- `list="categorymembers"`: ask for pages inside a category.
- `cmtitle="Category:Jutsu"`: category name.
- `cmlimit="500"`: ask up to 500 members in one API response.
- `cmtype="page"`: include only normal pages (not files/subcategories).
- `format="json"`: return JSON.

### `yield scrapy.Request(...)` concept

- `yield` does not execute request immediately by itself.
- It hands request object to Scrapy engine.
- Scrapy schedules and sends it asynchronously.
- When response comes back, callback function is called.

### Callback here

- `callback=self.parse_category`
- Means the response for this request goes to `parse_category(response)`.

---

## 10) Callback 1: `parse_category`

```python
def parse_category(self, response):
    payload = response.json()
```

### `response.json()`

- Converts JSON response body directly into Python dictionary.
- Easier than `json.loads(response.text)` manually.

### Looping category members

```python
for member in payload.get("query", {}).get("categorymembers", []):
```

This is defensive coding:

- `payload.get("query", {})`: if `query` missing, use empty dict.
- `.get("categorymembers", [])`: if list missing, use empty list.
- Prevents crashes (`KeyError`) when API shape differs.

### Extract title safely

```python
title = member.get("title")
if not title:
    continue
```

- If title missing/empty, skip this member.
- Good real-world habit: never assume perfect data.

### Generate detail request per title

```python
detail_url = self.build_api_url(
    action="parse",
    page=title,
    prop="text",
    format="json",
    formatversion="2",
)
yield scrapy.Request(detail_url, callback=self.parse_jutsu)
```

- `action=parse`: ask API to render page content.
- `prop=text`: return page HTML text.
- `formatversion=2`: cleaner JSON shape than legacy version.
- Callback now is `parse_jutsu` for each page.

So this function does fan-out:

- 1 category response
- becomes many page detail requests

### Handling pagination (`continue`)

MediaWiki category API may not return all members in one response.
If more exist, it returns a continuation token:

```python
continuation = payload.get("continue", {}).get("cmcontinue")
```

If token exists, build next API request with `cmcontinue=...` and send it to `parse_category` again.

This creates a loop over paginated API responses until no continuation remains.

---

## 11) Callback 2: `parse_jutsu`

This is where extraction happens and where your final exported item is produced.

### Parse API response

```python
payload = response.json().get("parse", {})
jutsu_name = payload.get("title", "").strip()
article_html = payload.get("text", "")
```

- `payload` is now parse result block.
- `title` gives page name.
- `text` gives rendered HTML content.

### Guard clause

```python
if not article_html:
    return
```

- If API returned no HTML (bad page, missing permission, etc.), stop cleanly.
- Avoid parsing empty content.

### BeautifulSoup parser creation

```python
soup = BeautifulSoup(article_html, "html.parser")
```

Now `soup` is the parse tree of the page HTML.

### Extracting `jutsu_type`

```python
jutsu_type = ""
aside = soup.find("aside")
```

- Fandom infobox data typically lives in `<aside>` section.
- `jutsu_type` default is empty string, so no crash if not found.

#### Fast path selector

```python
classification = aside.select_one("[data-source='classification'] .pi-data-value")
```

- CSS selector says: find element whose `data-source='classification'`, then inside it find `.pi-data-value`.
- If this exact structure exists, use it.

#### Fallback path

If fast selector fails, loop all infobox rows:

```python
for cell in aside.select("div.pi-data"):
    heading = cell.select_one("h3.pi-data-label")
    value = cell.select_one("div.pi-data-value")
```

- Find row label and row value.
- If label text equals `Classification`, use associated value.

Why fallback is useful:

- Wiki page templates may vary.
- Some pages differ in attributes or nesting.
- Fallback improves robustness.

#### `aside.decompose()`

```python
aside.decompose()
```

- Removes infobox from soup tree.
- Why remove? So description text extraction does not include infobox metadata.

### Extracting description text

```python
jutsu_description = soup.get_text("\n", strip=True)
jutsu_description = jutsu_description.split("Trivia", 1)[0].strip()
```

- `get_text("\n", strip=True)` converts visible HTML text to plain text with newlines.
- Splitting on `Trivia` removes trailing trivia section.
- `split("Trivia", 1)` splits once only (first occurrence).

Potential side effect to know as beginner:

- If the word `Trivia` appears naturally in description text, it may cut early.
- You can later improve by removing section using heading structure instead of plain word split.

### Returning the scraped item

```python
return {
    "jutsu_name": jutsu_name,
    "jutsu_type": jutsu_type,
    "jutsu_description": jutsu_description,
    "source_url": response.url,
}
```

In Scrapy callback methods, returning a dict is equivalent to yielding an item.
Scrapy feed exporter collects these and writes JSON lines.

---

## 12) Callback Chain Visualized

Think of callbacks as “where response goes next.”

1. `start_requests` sends category request.
2. Category response -> `parse_category`.
3. `parse_category` sends many page requests.
4. Each page response -> `parse_jutsu`.
5. `parse_jutsu` returns item dict.
6. Exporter writes items to file.

This is event-driven and asynchronous. Requests are not processed one-by-one in strict script order.
Scrapy schedules many requests and processes responses as they return.

---

## 13) Why `yield` matters in Scrapy

`yield` is central to Scrapy design:

- You `yield Request` objects to continue crawling.
- You `yield` or `return` item dictionaries to output data.

If you forget to yield requests:

- Spider starts but does not go deeper.

If callback is wrong:

- Response reaches wrong parser and extraction fails.

---

## 14) Running Commands (Practical)

Run spider and export to JSONL:

```bash
python -m scrapy runspider crawler/jutsu_crawler.py -o data/musab.jsonl
```

If your venv Python is explicit:

```bash
/home/keshtech/Documents/Keshtech/ML-DS-AI/NLP_TV_Series_Analysis/.venv/bin/python -m scrapy runspider crawler/jutsu_crawler.py -o data/musab.jsonl
```

Count rows quickly:

```bash
wc -l data/musab.jsonl
```

Peek first lines:

```bash
head -n 3 data/musab.jsonl
```

---

## 15) Common Beginner Confusions (and answers)

### Q1) Why not scrape normal page HTML directly?

Because your environment got `403` on regular fandom URLs. API endpoint remained accessible.

### Q2) Why use both Scrapy and BeautifulSoup?

- Scrapy: crawling engine and networking framework.
- BeautifulSoup: detailed HTML parsing utility.

You can parse HTML with Scrapy selectors alone, but many beginners find BeautifulSoup easier for flexible text extraction.

### Q3) Why not put everything in one function?

Because crawl flow has stages:

- discover page titles
- visit each page
- extract fields

Splitting functions mirrors this lifecycle and makes debugging easier.

### Q4) Is `return { ... }` okay in callback?

Yes. For a single item, returning dict works.
`yield { ... }` also works and is common style.

### Q5) Why use `.get(..., default)` everywhere?

External data can break assumptions.
Using `.get` prevents hard crashes and keeps crawl resilient.

---

## 16) Debugging Like a Tutorial Instructor

If no items appear, check in this order:

1. **Network status**
   - Are responses `200`?
   - If `403`, endpoint may be blocked.

2. **Callback flow**
   - Did `start_requests` yield request?
   - Did `parse_category` yield detail requests?

3. **Data shape**
   - Print/log `payload.keys()`.
   - Confirm API fields (`query`, `categorymembers`, `parse`, `text`).

4. **Selectors**
   - Infobox HTML may differ across pages.
   - Validate selectors against sample HTML.

5. **Export command**
   - Confirm using `-o data/musab.jsonl`.

For debug logs:

```bash
python -m scrapy runspider crawler/jutsu_crawler.py -L DEBUG -o data/musab.jsonl
```

---

## 17) How this differs from your original blocked spider

Original approach:

- Request fandom HTML listing page.
- Extract anchor links from DOM.
- Follow each link.
- Parse article HTML directly from regular page response.

Current approach:

- Request API list of category members (JSON).
- Use page titles to request rendered HTML via API parse endpoint.
- Parse the returned HTML text.

Main benefit: avoids blocked browse pages while preserving tutorial concepts (requests, callbacks, parsing, extraction, exporting).

---

## 18) Concept Mapping: Scrapy Components in Your File

- **Spider class**: `BlogsSpider`
- **Spider identity**: `name`
- **Spider-level settings**: `custom_settings`
- **Entry requests**: `start_requests`
- **First callback**: `parse_category`
- **Second callback**: `parse_jutsu`
- **Request creation**: `scrapy.Request(...)`
- **Item output**: returned dictionary

This is a classic two-stage crawl architecture:

- Stage A = discover URLs/titles
- Stage B = scrape detail data

---

## 19) If you want to practice more (beginner exercises)

1. Add a new field: `jutsu_rank` from infobox.
2. Add another field: `jutsu_users` list from infobox.
3. Save `jutsu_description` with normalized whitespace.
4. Skip non-canonical pages using title filters.
5. Log progress every 100 scraped items.

These will teach selectors, cleanup, and spider robustness.

---

## 20) Mental Model to Keep Forever

When you build any crawler, always think in this sequence:

1. **Where do I start?** (`start_requests`)
2. **How do I discover targets?** (`parse_category`)
3. **How do I parse target pages?** (`parse_jutsu`)
4. **What exact structure do I output?** (item dict)
5. **What breaks in real-world data?** (defensive coding)

If you keep this model, you can adapt to almost any website/API.

---

## 21) Final Beginner Takeaway

Your code already demonstrates core web-data engineering concepts:

- handling blocked endpoints by changing strategy
- API-first crawling
- asynchronous request chaining
- callback-driven parsing
- robust extraction with fallback selectors
- structured export to JSONL

This is exactly the kind of architecture used in real projects, not only tutorials.
