import sys
import asyncio
from playwright.async_api import async_playwright  # type: ignore  # noqa: F401
from bs4 import BeautifulSoup
import csv

# Ensure compatibility with Windows event loop
if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

def print_separator():
    print('-' * 40)

def clean_text(text):
    if not isinstance(text, str):
        return text
    # Replace non-breaking spaces, zero-width spaces, and curly apostrophes
    return text.replace('\xa0', ' ').replace('\u200b', '').replace('\u2019', "'").replace('\u2013', '-').replace('\u2014', '-').strip()

async def get_top_product_urls(section_url, num_products=25):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Show browser for debugging
        page = await browser.new_page()
        await page.goto(section_url, timeout=60000)
        await asyncio.sleep(3)

        # Scroll to load more products (simulate user scrolling)
        for _ in range(8):  # Increase range for more scrolling if needed
            await page.mouse.wheel(0, 2000)
            await asyncio.sleep(2)

        html = await page.content()
        soup = BeautifulSoup(html, 'html.parser')

        product_links = []
        for a in soup.select('a[href^="/product/"]'):
            href = a.get('href')
            if isinstance(href, str):
                full_url = 'https://www.sephora.com' + href
                if full_url not in product_links:
                    product_links.append(full_url)
            if len(product_links) >= num_products:
                break

        await browser.close()
        return product_links

async def scrape_sephora_ingredients_async(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Show browser for debugging
        page = await browser.new_page()
        await page.goto(url, timeout=60000)
        # Try to get product name
        try:
            await page.wait_for_selector("h1", timeout=10000)
            product_name = await page.inner_text("h1")
            product_name = product_name.strip()
        except Exception:
            # Fallback: try to get from <title>
            try:
                product_name = await page.title()
            except Exception:
                product_name = "Unknown Product"
        # Try to get ingredients
        try:
            await page.wait_for_selector("//button[contains(., 'Ingredients')]", timeout=10000)
            await page.click("//button[contains(., 'Ingredients')]")
            await page.wait_for_selector("#ingredients", timeout=10000)
            await asyncio.sleep(2)
            ingredients_html = await page.inner_html("#ingredients")
            soup = BeautifulSoup(ingredients_html, 'html.parser')
            ingredients_text = soup.get_text(separator="\n").strip()
            print("Extracted Ingredients for:", url)
            print(ingredients_text)
            return product_name, ingredients_text if ingredients_text else "No ingredients found"
        except Exception as e:
            print(f"❌ Error occurred for {url}: {e}")
            return product_name, "No ingredients found"
        finally:
            await browser.close()

async def main():
    section_url = "https://www.sephora.com/shop/skincare"
    print(f"Fetching top 25 product URLs from: {section_url}")
    product_urls = await get_top_product_urls(section_url, num_products=25)
    results = []
    for idx, url in enumerate(product_urls, 1):
        print(f"\n[{idx}/25] Scraping: {url}")
        product_name, ingredients = await scrape_sephora_ingredients_async(url)
        product_name = clean_text(product_name)
        ingredients = clean_text(ingredients)
        results.append({'url': url, 'product_name': product_name, 'ingredients': ingredients})
        print_separator()
    # Write results to CSV
    csv_filename = 'sephora_ingredients.csv'
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['url', 'product_name', 'ingredients'])
        writer.writeheader()
        for row in results:
            writer.writerow(row)
    print(f"\nScraping complete. Results saved to {csv_filename}")

if __name__ == "__main__":
    asyncio.run(main()) 
    
    