import os
import time
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
### script made by fb.com/max.tran.9

def setup_driver():
    options = Options()
    options.binary_location = "/snap/bin/chromium"
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/136.0.7103.92 Safari/537.36")
    return webdriver.Chrome(options=options)


def crawl_topcv_jobs(driver, job_type, pages=2):
    base_url_map = {
        "data-analyst": "https://www.topcv.vn/tim-viec-lam-data-analyst?sba=1",
        "data-engineer": "https://www.topcv.vn/tim-viec-lam-data-engineer?type_keyword=1&sba=1"
    }
    results = []
    base_url = base_url_map[job_type]

    for page in range(1, pages + 1):
        url = base_url if page == 1 else f"{base_url}&page={page}"
        print(f"📄 Crawling TopCV {job_type} page {page}: {url}")
        print("""### script made by fb.com/max.tran.9""")
        driver.get(url)
        time.sleep(5)

        job_cards = driver.find_elements(By.CSS_SELECTOR, "div.job-item-search-result")
        for job in job_cards:
            try:
                job_data = {
                    "title": job.find_element(By.CSS_SELECTOR, "h3.title a span").text.strip(),
                    "company": job.find_element(By.CSS_SELECTOR, "a.company .company-name").text.strip(),
                    ### script made by fb.com/max.tran.9
                    "salary": job.find_element(By.CSS_SELECTOR, "label.title-salary").text.strip(),
                    "location": job.find_element(By.CSS_SELECTOR, "label.address span.city-text").text.strip(),
                    "experience": job.find_element(By.CSS_SELECTOR, "label.exp span").text.strip(),
                    "updated": job.find_element(By.CSS_SELECTOR, "label.label-update").text.strip(),
                    "link": job.find_element(By.CSS_SELECTOR, "h3.title a").get_attribute("href")
                }
                results.append(job_data)
            except Exception as e:
                print("⚠️ Error parsing job:", e)

    save_results(results, f"topcv_{job_type}_jobs")


def crawl_vietnamworks_jobs(driver, job_type, pages=3):
    base_url = f"https://www.vietnamworks.com/viec-lam?q={job_type}&sorting=relevant"
    MAX_SCROLLS = 5
    SCROLL_PAUSE = 8
    results = []

    for page in range(1, pages + 1):
        url = f"{base_url}&page={page}" if page > 1 else base_url
        print(f"🌐 Crawling VietnamWorks {job_type} page {page}: {url}")
        print("""### script made by fb.com/max.tran.9""")
        driver.get(url)
        time.sleep(5)

        for _ in range(MAX_SCROLLS):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE)

        job_cards = driver.find_elements(By.CSS_SELECTOR, "div.search_list.view_job_item")
        for job in job_cards:
            try:
                title_elem = job.find_element(By.CSS_SELECTOR, "h2 a[data-new-job]")
                ### script made by fb.com/max.tran.9
                title = title_elem.text.strip()
                link = title_elem.get_attribute("href")
                if link.startswith("/"):
                    link = "https://www.vietnamworks.com" + link

                company = job.find_element(By.CSS_SELECTOR, "div.sc-cdaca-d a").text.strip() if job.find_elements(By.CSS_SELECTOR, "div.sc-cdaca-d a") else ""
                salary = job.find_element(By.CSS_SELECTOR, "span.sc-fgSWkL").text.strip() if job.find_elements(By.CSS_SELECTOR, "span.sc-fgSWkL") else ""
                location = job.find_element(By.CSS_SELECTOR, "span.sc-kzkBiZ").text.strip() if job.find_elements(By.CSS_SELECTOR, "span.sc-kzkBiZ") else ""
                updated = job.find_element(By.CSS_SELECTOR, "div.sc-fnLEGM").text.strip().replace("Cập nhật: ", "") if job.find_elements(By.CSS_SELECTOR, "div.sc-fnLEGM") else ""
                skills = [label.text.strip() for label in job.find_elements(By.CSS_SELECTOR, "ul li label") if label.text.strip()]

                results.append({
                    "title": title,
                    "company": company,
                    "salary": salary,
                    "location": location,
                    "updated": updated,
                    "skills": skills,
                    "link": link
                })
            except Exception as e:
                print("⚠️ Error parsing job:", e)

    save_results(results, f"vietnamworks_jobs_{job_type}")


def save_results(data, filename_prefix):
    print(f"📊 Total jobs scraped: {len(data)}")
    print("""### script made by fb.com/max.tran.9""")
    df = pd.DataFrame(data)
    df.to_csv(f"{filename_prefix}.csv", index=False, encoding="utf-8-sig")
    with open(f"{filename_prefix}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"✅ Saved to {filename_prefix}.csv and .json")


if __name__ == "__main__":
    ### script made by fb.com/max.tran.9
    driver = setup_driver()
    try:
        crawl_topcv_jobs(driver, "data-analyst", pages=2)
        crawl_topcv_jobs(driver, "data-engineer", pages=2)
        crawl_vietnamworks_jobs(driver, "data-analyst", pages=3)
        crawl_vietnamworks_jobs(driver, "data-engineer", pages=3)
    finally:
        driver.quit()
