from bs4 import BeautifulSoup
import re
import requests


def extract_jobs(term):
  base_url = f"https://remoteok.com/remote-{term}-jobs"
  response = requests.get(base_url, headers={"User-Agent": "Kimchi"})
  results = []

  if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    print(f"{term} : {soup.find_all('title')[0].string}")

    jobs = soup.find_all("tr", class_="job")
    # print(len(jobs))
    # print(jobs[0].prettify())

    for job in jobs:
      jobTitle = job.find("h2", itemprop="title")
      jobDetail = job.find("a", class_="preventLink")['href']
      clientNm = job.find("h3", itemprop="name")
      location = job.find("div", class_="location")

      position = jobTitle.string.strip().replace(',', ' ') if jobTitle else ""
      detail = f"https://remoteok.com{jobDetail.strip()}" if jobDetail else ""
      company = clientNm.string.strip() if clientNm else ""
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
  else:
    print("Can't get jobs.")

  print(f"{term} : {len(results)} in remoteok")
  return results
