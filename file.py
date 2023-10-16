def save_to_file(keyword, jobs):
  file = open(f"result_{keyword}.csv", "w", encoding="utf-8")
  file.write("Position,Company,Location,Detail\n")

  for job in jobs:
    file.write(f"{job['position']},{job['company']},{job['location']},{job['detail']}\n")
  file.close()
