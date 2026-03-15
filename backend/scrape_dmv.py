import requests
from bs4 import BeautifulSoup
from pathlib import Path

PAGES = {
    "dmv_renewal": "https://www.flhsmv.gov/driver-licenses-id-cards/renew-or-replace-your-florida-driver-license-or-id-card/",
    "dmv_what_to_bring": "https://www.flhsmv.gov/driver-licenses-id-cards/what-to-bring/",
    "medicare_signup": "https://www.medicare.gov/basics/get-started-with-medicare/sign-up/how-do-i-sign-up-for-medicare",
    "ssa_replace_card": "https://www.ssa.gov/number-card/replace-card",
}

data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

for name, url in PAGES.items():
    try:
        print(f"Scraping {name}...")

        response = requests.get(url, timeout=20)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        main_section = (
            soup.find("section", id="text")
            or soup.find("main")
            or soup.find("article")
            or soup.body
        )

        texts = []
        for tag in main_section.find_all(["h1", "h2", "h3", "p", "li"]):
            text = tag.get_text(" ", strip=True)
            if text:
                texts.append(text)

        output = "\n".join(texts)
        output_file = data_dir / f"{name}.txt"
        output_file.write_text(output, encoding="utf-8")

        print(f"Saved to {output_file}")

    except Exception as e:
        print(f"Failed on {name}: {e}")