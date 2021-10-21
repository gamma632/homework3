from flask import Flask, render_template
import util

# create an application instance
# all requests it receives from clients to this object for handling
# we are instantiating a Flask object by passing __name__ argument to the Flask constructor.
# The Flask constructor has one required argument which is the name of the application package.
# Most of the time __name__ is the correct value. The name of the application package is used
# by Flask to find static assets, templates and so on.
app = Flask(__name__)

# evil global variables
# can be placed in a config file
# here is a possible tutorial how you can do this
username='raywu1990'
password='test'
host='127.0.0.1'
port='5432'
database='dvdrental'

# route is used to map a URL with a Python function
# complete address: ip:port/
# 127.0.0.1:5000/
@app.route("/api/update_basket_a")

def update_basket_a():
	cursor,connection = util.connect_to_db(username, password, host, port, database)
	status = util.insert_row(cursor)
	util.disconnect_from_db(connection,cursor)
	return render_template('update.html', log_html = status)

@app.route("/api/unique")

def unique():
	cursor,connection = util.connect_to_db(username, password, host, port, database)

	status, data = util.unique(cursor)
	col_names = None
	log = None
	is_error = data is None
	if data is not None:
		col_names = [desc[0] for desc in cursor.description]
		log = data[:]
		# if we need to remove the None's then process data here

	util.disconnect_from_db(connection,cursor)

	return render_template('unique.html', sql_table = log, table_title = col_names, is_error = is_error)

if __name__ == '__main__':
	# set debug mode
	app.debug = True
	# your local machine ip
	ip = '127.0.0.1'
	app.run(host=ip)
