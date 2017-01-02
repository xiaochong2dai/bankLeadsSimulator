from flask import Flask
from flask import request
import argparse
from flask_restful import Resource, Api
from flask_restful import reqparse
from flaskext.mysql import MySQL
import random,string
from random import randint, randrange, uniform
from datetime import datetime
# import MySQLdb

parser = reqparse.RequestParser()
parser.add_argument('low', type = str)
parser.add_argument('high', type = str)

app = Flask(__name__)

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '1'
app.config['MYSQL_DATABASE_DB'] = 'bankLeads'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
conn = mysql.connect()
cur = conn.cursor()

# @app.route('/api/v1.0/lenderData',methods=['GET'])
# def get_taxiData():
	
#     # you must create a Cursor object. It will let
# 	#  you execute all the queries you need
# 	args = parser.parse_args()
# 	# conn = mysql.connect()
# 	# cur = conn.cursor()
	
# 	start = request.args.get('low','0-100')
# 	end = request.args.get('high','0-100')

# 	# Use all the SQL you like

# 	cur.execute("SELECT * FROM lender where age >'"+low+"' and  age < '"+high+"'")
# 	# print all the first cell of all the rows
# 	# for row in cur.fetchall():
# 	#     return row[0] + ' ,' + row[1]+ ' ,' + row[2] + ' ,' 
	

# 	conn.close()
# 	data = cur.fetchall()
# 	return data

@app.route('/api/v1.0/streaming/lenderData',methods=['GET'])
def get_streamingData():
	# you must create a Cursor object. It will let
	#  you execute all the queries you need
	conn = mysql.connect()
	cur = conn.cursor()
	# now = datetime.now()
	# date = now.strftime('%Y/%m/%d %H:%M:%S')
	
   	age = random.randrange(18, 67)
   	loanAmount = 1000*random.randrange(1,999)
   	income = 1000*random.randrange(10, 999)
   	"""
   	credit score range:
   	Category     Range
   	Excellent	 750 & Above
   	Good 		 700-749
   	Fair		 650-699
   	Poor		 550-649
   	Bad 		 550 & Below
   	"""
   	creditScore = random.randrange(500,850)
   	employmentYears = random.randrange(0,50)
   	"""
   	0: Unemployed     
   	1: Employed
   	set employment 80% probability and Unemployment 20%
   	"""
   	weightedEmploymentStatusCode = [0,0,1,1,1,1,1,1,1,1]
   	employmentStatus = random.choice(weightedEmploymentStatusCode)
   	
	try:
	   insert_query = """INSERT INTO lender (age,loanAmount,income,creditScore,employmentYears,employmentStatus) VALUES ('%d','%d','%d','%d','%d','%d')
	   				  """%(age,loanAmount,income,creditScore,employmentYears,employmentStatus)
	   cur.execute(insert_query)   
	   conn.commit()
	except:
	   conn.rollback()
	
	cur.execute("""SELECT * FROM lender ORDER BY RAND() LIMIT 1""")
	for row in cur.fetchall():
	    return str(row[0]) + ', ' + \
	    	   str(row[1]) + ', ' + \
	    	   str(row[2]) + ', ' + \
	    	   str(row[3]) + ', ' + \
	    	   str(row[4]) + ', ' + \
	    	   str(row[5]) + ', ' + \
	    	   str(row[6])
	cur.close()
	# data = cur.fetchall()
	#return data


if __name__ == '__main__':
	try:
		create_query = """CREATE TABLE IF NOT EXISTS lender (
							lid INT NOT NULL AUTO_INCREMENT,
							age TINYINT,
							loanAmount INT NOT NULL,
							income INT NOT NULL,
							creditScore SMALLINT,
							employmentYears TINYINT,
							employmentStatus TINYINT,
							PRIMARY KEY (lid)
						)"""
		conn = mysql.connect()
		cur = conn.cursor()
		cur.execute(create_query)
	except:
		conn.rollback()
	app.run(debug=True)