
from flask import Flask
from flask import render_template
from flask import request
from db_connection import PostgresDB
from flask_cors import CORS
from flask import redirect


app = Flask(__name__)
CORS(app)
postgres = PostgresDB()
conn = postgres.get_connection()  #

@app.route('/')
def customer():
    return render_template('studentLogin.html')

# Route to handle form submission
@app.route('/create', methods=['POST'])
def create_data():
    print("within create service point")
    result = request.form  
    global conn
    conn = checkConnection(conn)
    
    cursor=conn.cursor()
    # query = 'Insert into persona_predictor.student values ('+result['sid']+","+result['fname']+","+result['lname']+","+result['dob']+","+result['adue']+')'
    query = "INSERT INTO persona_predictor.student VALUES (%s, %s, %s, %s, %s)"
        
    cursor.execute(query, (
            result['sid'],
            result['fname'],
            result['lname'],
            result['dob'],
            result['adue']
        ))
    
    commitAndclose(conn)
    # return render_template("result_data.html", result=result)
    return "successfully inserted the record"

@app.route('/edit_student/<int:student_id>', methods=['POST','GET'])
def edit_student(student_id):
    global conn
    conn = checkConnection(conn)
    cursor=conn.cursor()

    query="select * from persona_predictor.student   where student_id=%s"
    cursor.execute(query, (student_id,))

    rows  = cursor.fetchall()
    print("the row to edit is ",rows[0])
    return render_template('updateStudent.html', data=rows[0])

@app.route('/update', methods=['POST'])
def update_data():
    result= request.form
    print("the values to update is ", result)
    global conn
    conn = checkConnection(conn)
    cursor=conn.cursor()

    query = "UPDATE persona_predictor.student  set first_name=%s, last_name=%s, dob=%s, amount_due=%s where student_id=%s"
    cursor.execute(query,( 
        
            result['fname'],
            result['lname'],
            result['dob'],
            result['adue'],
            result['sid']
        ))
    commitAndclose(conn)
    return "successfully updated the record"

@app.route('/delete/<int:student_id>',  methods=['GET', 'POST'])
def delete_data(student_id):
    result= request.form
    print("the values to update is ", result)
    global conn
    conn = checkConnection(conn)
    cursor=conn.cursor()

    query = "delete from persona_predictor.student where student_id=%s"
    cursor.execute(query,( 
            student_id,
        ))
    commitAndclose(conn)
    return "successfully deleted record Id- "+str(student_id)

@app.route('/lookforstudent/<int:student_id>', methods=['GET'])
def searchStudent(student_id):
    
    global conn
    conn = checkConnection(conn)
    cursor=conn.cursor()

    query="select  * from persona_predictor.student where student_id=%s"

    cursor.execute(query,(student_id,))

    rows = cursor.fetchall()
    x= [row for row in rows]
    print("the student record is ", x)
    return render_template("studentRecord.html", rows=x)
       
@app.route('/lookforallstudent', methods=['GET'])
def searchAllStudent():
    
    global conn
    conn = checkConnection(conn)
    cursor=conn.cursor()

    query="select  * from persona_predictor.student"

    cursor.execute(query)

    rows = cursor.fetchall()
    x= [row for row in rows]
    print("the student record is ", x)
    return render_template("studentRecord.html", rows=x)




def checkConnection(conn):
    if conn.closed != 0: 
        conn = postgres.get_connection()    
    return conn

def commitAndclose(conn):
    conn.commit()
    conn.close()

if __name__ == '__main__':
    app.run(debug=True)
