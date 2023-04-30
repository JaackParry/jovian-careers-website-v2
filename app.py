from flask import Flask, render_template, jsonify
from database import load_jobs_from_db

app = Flask(__name__)

#creating an array to use as dynamic content on the web page - we have since replaced this with our database information
'''JOBS = [
  {
    'id': 1,
    'title': 'Data Analyst',
    'location': 'Bengaluru, India',
    'salary': 'Rs. 10,000,000'
  },
  {
    'id': 2,
    'title': 'Data Scientist',
    'location': 'Dehli, India',
    'salary': 'Rs. 15,000,000'
  },
  {
    'id' : 3,
    'title': 'Frontend Engineer',
    'location': 'London, UK'
  },
  {
    'id': 4,
    'title': 'Backend Engineer',
    'location': 'San Francisco, USA',
    'salary': '$150,000'
  }
]'''

@app.route("/")
def hello_jovian():
  jobs = load_jobs_from_db()
  return render_template('home.html', 
                         jobs=jobs, #this is saying that wherever jobs appears in home.html to use our jobs variable
                         company_name="Jack's")

@app.route("/api/jobs")
def list_jobs():
  jobs = load_jobs_from_db()
  return jsonify(jobs)

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)