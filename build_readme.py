import feedparser
import re
import os
import datetime

def replace_chunk(content, marker, chunk):
    r = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    chunk = "<!-- {} starts -->\n{}\n<!-- {} ends -->".format(marker, chunk, marker)
    return r.sub(chunk, content)

def fetch_blog_entries():
    entries = feedparser.parse("https://wesleydesilvestro.com/rss.xml")["entries"]
    return [
        {
            "title": entry["title"],
            "url": entry["link"],
            "published": datetime.datetime.strptime(entry["published"], '%a, %d %b %Y  %H:%M:%S %Z').strftime("%Y-%m-%d")
        }
        for entry in entries
    ]


if __name__ == "__main__":
    readme = open("README.md", "r")

    readme_contents = readme.read()

    entries = fetch_blog_entries()[:5]
    entries_md = "\n".join(
        ["* [{title}]({url}) - {published}".format(**entry) for entry in entries]
    )
    rewritten = replace_chunk(readme_contents, "blog", entries_md)

    print(entries_md)

    with open("README.md", "w") as file:
        file.write(rewritten)