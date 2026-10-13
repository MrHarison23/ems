from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

@app.route('/add', methods=['POST'])
def add_employee():
	employee_name = request.form.get('employee_name')
	employee_email = request.form.get('employee_email')
	employee_position = request.form.get('employee_position')


	conn = psycopg2.connect(
		host = "db",
		database = "flaskdb",
		user = "flaskuser",
		password = "flaskpass"
	)

	cur = conn.cursor()

	cur.execute(
		"INSERT INTO users (name, email, position) VALUES (%s, %s, %s)", 
		(employee_name, employee_email, employee_position)
	)
	
	conn.commit()

	cur.close()
	conn.close()

	return redirect(url_for('home')) 
	
@app.route('/')
def home():
	conn = psycopg2.connect(
		host = "db",
		database = "flaskdb",
		user = "flaskuser",
		password = "flaskpass"
	)

	promo = "Employee Management System"
	
	cur = conn.cursor()
	
	cur.execute("SELECT id, name, email, position FROM users")
	
	users = cur.fetchall()
	
	print("DEBUG:", users) 

	cur.close()
	conn.close()
	return render_template('index.html', users=users)
    
if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000, debug=True)
