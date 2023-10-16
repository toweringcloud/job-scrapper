from bs4 import BeautifulSoup
import re
import requests


def extract_jobs(term):
  base_url = f"https://weworkremotely.com/remote-jobs/search?term={term}"
  response = requests.get(f"{base_url}")
  results = []

  if response.status_code != 200:
    print("Can't request website")
  else:
    soup = BeautifulSoup(response.text, "html.parser")
    print(f"{term} : {soup.find_all('title')[0].string}")

    # weworkremotely scraper old version
    # jobs = soup.find_all('section', class_="jobs")

    # weworkremotely scraper new version
    jobs = soup.find_all('li', class_="feature")
    # print(len(jobs))
    # print(jobs[0].prettify())

    for job in jobs:
      jobTitle = job.find("span", class_="title")
      jobDetail = job.find('a', recursive=False)['href']
      clientNm = job.find_all("span", class_="company")
      location = job.find("span", class_="region company")

      position = jobTitle.string.strip().replace(',', ' ') if jobTitle else ""
      detail = f"http://weworkremotely.com{jobDetail.strip()}" if jobDetail else ""
      company = clientNm[0].string.strip() if clientNm else ""
      company = re.sub(r'\s', '', company).strip()
      location = location.string.strip() if location else ""
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

  print(f"{term} : {len(results)} in weworkremotely")
  return results
