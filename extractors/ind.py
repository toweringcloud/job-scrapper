from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import re
import requests


def extract_jobs(term, test, page=0):
  base_url = "https://kr.indeed.com/jobs"
  response = requests.get(f"{base_url}?q={term}&start={page*10}")
  results = []

  if response.status_code == 403:
    if test is True:
      samples = ("flutter", "golang", "python", "react", "rust")
      sample = f"ind-{term}.html" if term in samples else "ind-default.html"
      HTMLFile = open(f"{os.getcwd()}/extractors/data/{sample}", "r", encoding="utf-8")
      response.text2 = f"'''{HTMLFile.read()}'''"
    else:
      options = Options()
      options.add_argument("--no-sandbox")
      options.add_argument("--disable-dev-shm-usage")
      browser = webdriver.Chrome(options=options)
      browser.get(base_url)

      if browser.page_source:
        response.status_code = 200
        HTMLFile = open("page_source.html", "w", encoding="utf-8")
        HTMLFile.write(browser.page_source)
        HTMLFile.close()
        HTMLFile = open(f"{os.getcwd()}/page_source.html", "r", encoding="utf-8")
        response.text2 = f"'''{HTMLFile.read()}'''"
        HTMLFile.close()

  if response.status_code == 200 or test is True:
    soup = BeautifulSoup(response.text2 if response.text2 else response.text,
                         "html.parser")
    if test is True: print(f"{term} : use sample data in case of 403")
    print(f"{term} : {soup.find_all('title')[0].string}")

    # indeed scraper old version
    # jobs_list = soup.find_all("ul", class_="jobsearch-ResultsList")
    # jobs = jobs_list.find_all("li", recursive=False)

    # indeed scraper new version
    jobs = soup.find_all("td", class_="resultContent")
    # print(len(jobs))
    # print(jobs[0].prettify())

    for job in jobs:
      jobTitle = job.find("h2").find("span")['title']
      jobDetail = job.find("a", role="button")['href']
      clientNm = job.find("span", class_="companyName")
      location = job.find("div", class_="companyLocation")

      position = jobTitle.strip().replace(',', ' ') if jobTitle else ""
      detail = f"https://kr.indeed.com{jobDetail.strip()}" if jobDetail else ""
      company = clientNm.string if clientNm else ""
      company = re.sub(r'\s', '', company).strip()
      location = location.string.replace('\n', ' ') if location else ""
      location = re.sub(r'\t', '', location).strip()
      # print(position, detail, company, location)

      if position and detail and company and location:
        job_data = {
          'position': position,
          'detail': detail,
          'company': company,
          'location': location
        }
        results.append(job_data)
  else:
    print("Can't get jobs.")

  print(f"{term} : {len(results)} in indeed")
  return results


def count_pages(term):
  base_url = f"https://kr.indeed.com/jobs?q={term}&limit=50"
  response = requests.get(base_url)

  if response.status_code != 200:
    print('Cannot request page')
  else:
    soup = BeautifulSoup(response.text, "html.parser")
    pagination = soup.find("ul", class_="pagination-list")

    if pagination is None:
      return 1
    pages = pagination.find_all("li", recursive=False)
    return len(pages) if len(pages) <= 5 else 5
