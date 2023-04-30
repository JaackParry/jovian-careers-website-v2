#packages required to connect to the db
from sqlalchemy import create_engine, text
import os

#using our secrets manager to add the DB connection string, it's very bad practice to be storing plain text information in our code

db_connection_string = os.environ['DB_CONNECTION_STRING']

#first we have to create an engine to connect to the db - then we will be able to extract data from the db
engine = create_engine(
  db_connection_string,
  connect_args={
    #you need to use ssl to connect to mysql as it won't allow insecure connections, you'll get an error otherwise
    "ssl": {
      "ssl_ca": "/etc/ssl/ca.pem"
    }
  })

#this allows us to use the connection we defined above to execute against the db. once the sequence has run then the connection will drop
with engine.connect() as conn:
  #running a query to just pull all data from the jobs table
  result = conn.execute(text("select * from jobs"))


#here we are pulling our list of jobs from the db and into a dictionary. this is all based upon the work that is now commented out in database.py. it is good practice to keep all our database-related functionality in a database file rather than mixing it across the app.py file
def load_jobs_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from jobs"))
    jobs = []
    for row in result.all():
      jobs.append(row._asdict())
    return jobs


#this is a slight different function that will only return one particular job depending on it's id. if an ID is specified that doesn't exist in the DB then we will just return 0
def load_job_from_db(id):
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM jobs WHERE id = :val"),
                          {'val': id})
    rows = result.all()
    if len(rows) == 0:
      return None
    else:
      row = rows[0]
      column_names = list(result.keys())
      return {column_names[i]: row[i] for i in range(len(column_names))}


#now we're creating a dictionary withe the rows from the db. the rows were not iterable so we needed to use the _asdict function to convert
  '''result_dicts = []
  for row in result.all():
    result_dicts.append(row._asdict())

  print(result_dicts)'''

  #code below is testing out pulling different results
  '''print("type(result)", type(result))
  result_all = result.all()
  print("type(result.all)", type(result_all))
  first_result = result_all[0]
  print("type(first_result):",type(first_result))
  first_result_dict = dict([result_all])
  print(type(first_result_dict))
  print(first_result_dict)
'''
