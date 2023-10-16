from flask import Flask, render_template, request, redirect, send_file

from extractors.ind import extract_jobs as indeed
from extractors.rok import extract_jobs as remoteok
from extractors.wwr import extract_jobs as weworkremotely
from file import save_to_file

app = Flask("Job Scrapper")
db = {}


@app.route("/")
def home():
  return render_template("home.html")


@app.route("/reset")
def reset():
  db = {}
  return render_template("home.html", action="reset")


@app.route("/search")
def search():
  keyword = request.args.get("keyword")

  if keyword is None:
    return redirect("/")

  if keyword in db:
    jobs = db[keyword]
  else:
    jobs_a = indeed(keyword, False)
    jobs_b = remoteok(keyword)
    jobs_c = weworkremotely(keyword)
    jobs = jobs_a + jobs_b + jobs_c
    db[keyword] = jobs

  print(f"{keyword} : {len(jobs)} jobs found!")
  return render_template("search.html", keyword=keyword, jobs=jobs)


@app.route("/export")
def export():
  keyword = request.args.get("keyword")

  if keyword is None:
    return redirect("/")

  if keyword not in db:
    return redirect(f"/search/keyword={keyword}")

  save_to_file(keyword, db[keyword])
  return send_file(f"result_{keyword}.csv", as_attachment=True)


app.run("0.0.0.0")
