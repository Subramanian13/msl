from flask import Flask, render_template, request, redirect, url_for
import os
import psycopg2
from datetime import datetime, timedelta

app = Flask(__name__)

DATABASE_URL = "postgres://data_gbi0_user:DRHIPL0XVjIi1tc3dzVhEjLJ1hbA0web@dpg-co3pef4f7o1s738kb0h0-a.oregon-postgres.render.com/data_gbi0"

def connect_to_db():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_record_form')
def add_record_form():
    return render_template('add_record.html')

@app.route('/add_record', methods=['POST'])
def add_record():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()

        name = request.form['Name']
        address = request.form['address']
        aadhar_number = request.form['aadhar_number']
        phone_number = request.form['phone_number']
        joint_holder = request.form['joint_holder']
        size = request.form['size']
        locker_no = request.form['locker_no']
        deposit_amount_paid = int(request.form['deposit_amount_paid'])
        rent_amount_paid = int(request.form['rent_amount_paid'])
        rent_time_period_from = datetime.strptime(request.form['rent_time_period_from'], '%Y-%m-%d').date()
        # rent_time_period_to=request.form['rent_time_period_to']
        rent_paid_date = request.form['rent_paid_date'] or None
        deposit_amount_yet_to_pay = 30000 - deposit_amount_paid

        if size == 'XL':
            rent_amount_yet_to_be_paid = 5000 - rent_amount_paid
        elif size == 'L':
            rent_amount_yet_to_be_paid = 4000 - rent_amount_paid
        elif size == 'M':
            rent_amount_yet_to_be_paid = 3000 - rent_amount_paid
        else:
            rent_amount_yet_to_be_paid = None  # Handle invalid size

        rent_time_period_to = rent_time_period_from + timedelta(days=365)

        cursor.execute("INSERT INTO locker_data (Name, address, aadhar_number, phone_number, joint_holder, size, locker_no, deposit_amount_paid, deposit_amount_yet_to_pay, rent_amount_paid, rent_amount_yet_to_be_paid,rent_time_period_from,rent_time_period_to,rent_paid_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s,%s)",
                       (name, address, aadhar_number, phone_number, joint_holder, size, locker_no, deposit_amount_paid, deposit_amount_yet_to_pay, rent_amount_paid, rent_amount_yet_to_be_paid,rent_time_period_from,rent_time_period_to,rent_paid_date))
        
        connection.commit()
        
        return redirect(url_for('display_records'))  # Assuming you have a route named 'display_records' for displaying records
    except (Exception, psycopg2.Error) as error:
        print("Error adding record to PostgreSQL:", error)
        return "Error adding record to PostgreSQL"
    finally:
        if connection:
            cursor.close()
            connection.close()

@app.route('/display_records')
def display_records():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM locker_data order by Name")
        data = cursor.fetchall()
        
        return render_template('display_records.html', data=data)
    except (Exception, psycopg2.Error) as error:
        print("Error fetching data from PostgreSQL:", error)
        return "Error fetching data from PostgreSQL"
    finally:
        if connection:
            cursor.close()
            connection.close()

@app.route('/view_record/<int:id>')
def view_record(id):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM locker_data WHERE id = %s", (id,))
        record = cursor.fetchone()

        if record:
            return render_template('view.html', record=record)
        else:
            return "Record not found"
    except (Exception, psycopg2.Error) as error:
        print("Error fetching data from PostgreSQL:", error)
        return "Error fetching data from PostgreSQL"
    finally:
        if connection:
            cursor.close()
            connection.close()

@app.route('/update_record/<int:id>', methods=['GET', 'POST'])
def update_record(id):
    if request.method == 'POST':
        try:
            connection = connect_to_db()
            cursor = connection.cursor()

            name = request.form['Name']
            address = request.form['address']
            aadhar_number = request.form['aadhar_number']
            phone_number = request.form['phone_number']
            joint_holder = request.form['joint_holder']
            size = request.form['size']
            locker_no = request.form['locker_no']
            deposit_amount_paid = int(request.form['deposit_amount_paid'])
            rent_amount_paid = int(request.form['rent_amount_paid'])
            rent_time_period_from = datetime.strptime(request.form['rent_time_period_from'], '%Y-%m-%d').date()
            # rent_time_period_to=request.form['rent_time_period_to']
            rent_paid_date = request.form['rent_paid_date'] or None
            deposit_amount_yet_to_pay = 30000 - deposit_amount_paid

            if size == 'XL':
                rent_amount_yet_to_be_paid = 5000 - rent_amount_paid
            elif size == 'L':
                rent_amount_yet_to_be_paid = 4000 - rent_amount_paid
            elif size == 'M':
                rent_amount_yet_to_be_paid = 3000 - rent_amount_paid
            else:
                rent_amount_yet_to_be_paid = None  # Handle invalid size

            rent_time_period_to = datetime.strptime('31/03/2024','%Y-%m-%d').date()

            cursor.execute("UPDATE locker_data SET Name = %s, address = %s, aadhar_number = %s, phone_number = %s, joint_holder = %s, size = %s, locker_no = %s, deposit_amount_paid = %s, deposit_amount_yet_to_pay = %s, rent_amount_paid = %s, rent_amount_yet_to_be_paid = %s ,rent_time_period_from=%s,rent_time_period_to=%s,rent_paid_date=%s WHERE id = %s",
                           (name, address, aadhar_number, phone_number, joint_holder, size, locker_no, deposit_amount_paid, deposit_amount_yet_to_pay, rent_amount_paid, rent_amount_yet_to_be_paid,rent_time_period_from,rent_time_period_to,rent_paid_date,id))

            connection.commit()

            return redirect(url_for('display_records'))  
        except (Exception, psycopg2.Error) as error:
            print("Error updating record in PostgreSQL:", error)
            return "Error updating record in PostgreSQL"
        finally:
            if connection:
                cursor.close()
                connection.close()
    else:
        try:
            connection = connect_to_db()
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM locker_data WHERE id = %s", (id,))
            data = cursor.fetchone()

            if data:
                return render_template('update_record.html', data=data)
            else:
                return "Record not found"
        except (Exception, psycopg2.Error) as error:
            print("Error fetching data from PostgreSQL:", error)
            return "Error fetching data from PostgreSQL"
        finally:
            if connection:
                cursor.close()
                connection.close()


@app.route('/delete_record/<int:id>', methods=['POST'])
def delete_record(id):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        
        cursor.execute("DELETE FROM locker_data WHERE id = %s", (id,))
        
        connection.commit()
        
        return redirect(url_for('display_records'))
    except (Exception, psycopg2.Error) as error:
        print("Error deleting record from PostgreSQL:", error)
        return "Error deleting record from PostgreSQL"
    finally:
        if connection:
            cursor.close()
            connection.close()

def update_rent_dates():
    connection = None  # Initialize connection variable
    try:
        connection = connect_to_db()
        cursor = connection.cursor()

        cursor.execute("SELECT id, rent_time_period_to FROM locker_data")
        records = cursor.fetchall()

        current_date = datetime.now().date()

        for record in records:
            record_id, rent_to_date = record
            if current_date > rent_to_date:
                # Update rent time period to next 12 months
                rent_from_date = rent_to_date + timedelta(days=1)
                rent_to_date = rent_to_date.replace(year=rent_to_date.year + 1)

                cursor.execute("UPDATE locker_data SET rent_time_period_from = %s, rent_time_period_to = %s WHERE id = %s",
                               (rent_from_date, rent_to_date, record_id))

        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error updating rent dates:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()

# Run update_rent_dates function at the start of each request
@app.before_request
def update_rent_dates_before_request():
    update_rent_dates()

if __name__ == '__main__':
    app.run(debug=True)
