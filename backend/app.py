from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql
from datetime import date 
from dateutil.relativedelta import relativedelta
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'Yassin2011')
DB_NAME = os.getenv('DB_NAME', 'nexusfinancedashboard')

app = Flask(__name__)
CORS(app, origins=["*"])

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Yassin2011',
    'database': 'nexusfinancedashboard',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db_connection():
    return pymysql.connect(**db_config)

@app.route("/api/calculate", methods=['POST'])
def save_calculations():
    data = request.json

    if not data:
        return jsonify({"error": "Missing request body"}), 400

    annual_income = data.get('annual_income')
    savings_target = data.get('savings_target')
    timeline = int(data.get('timeline') or 0)
    total_savings = data.get('total_savings')
    emergency_fund = data.get('emergency_fund')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    date_birth = data.get('date_birth')
    passw = data.get('passw')
    email = data.get('mail')

    calculated_completion = date.today() + relativedelta(months=timeline)

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            user_sql = """
                INSERT INTO userinfo
                (first_name, last_name, date_birth, pass, email)
                VALUES(%s, %s, %s, %s, %s)
            """
            cursor.execute(user_sql, (first_name, last_name, date_birth, passw, email))
            user_id = cursor.lastrowid
            calc_sql = """
                INSERT INTO calculation_table
                (annual_income, savings_target, timeline, total_savings, emergency_fund, completion_date, user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            
            # This passes user_id into the user_id column, leaving the 'id' column to auto-increment safely!
            cursor.execute(calc_sql, (annual_income, savings_target, timeline, total_savings, emergency_fund, calculated_completion, user_id))
            
        connection.commit()
        return jsonify({"message": "Profile and Calculation saved successfully"}), 201
    
    except Exception as e:
        connection.rollback()
        # Add a print statement here so you can trace errors directly in your terminal log
        print(f"Database insertion failed: {str(e)}") 
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()  # Always explicitly close the connection when done
@app.route("/home", methods=['GET'])
def fetch_info():   
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT total_savings, savings_target, timeline, annual_income, completion_date FROM calculation_table ORDER BY id DESC LIMIT 1")
            calc_result = cursor.fetchone()
            
            cursor.execute("SELECT monthly_contributed, debt_contributions, emergency_contribtuions FROM extradata ORDER BY id ASC")
            extra_results = cursor.fetchall()

            cursor.execute("SELECT SUM(subscription_price) as total_subs FROM subscription_ledger")
            sub_result = cursor.fetchone()
            total_subscription = float(sub_result.get('total_subs') or 0) if sub_result else 0

            cursor.execute("""
                    SELECT DATE_FORMAT(transaction_date, '%M') as month_name, SUM(transaction_value) as total_spent
                    FROM transaction_ledger
                    GROUP BY DATE_FORMAT(transaction_date, '%M'), MONTH(transaction_date)
                    ORDER BY MONTH(transaction_date) ASC
            """)
            expense_results = cursor.fetchall()

            base_savings = float(calc_result.get('total_savings') or 0) if calc_result else 0
            
            # Defensive check if no registration calculation row exists yet
            if not calc_result:
                return jsonify({
                    "profile": {
                        "monthly_savings": 0,
                        "savings_rate": 0,
                        "balance_36mo": 0,
                        "completion_date": str(date.today()),
                        "total_contributed": 0,
                        "time_to_goal": 12, # safe default
                        "savings_target": 1000 # safe default
                    },
                    "base_savings": 0,
                    "savings_history": [],
                    "debt": [],
                    "monthly_averages_chart": [0] * 12
                }), 200
                
            savings_target = float(calc_result.get('savings_target') or 0)
            timeline = int(calc_result.get('timeline') or 12)
            if timeline <= 0: 
                timeline = 12  # Avoid division by zero bugs
            annual_income = float(calc_result.get('annual_income') or 1)
            if annual_income <= 0: 
                annual_income = 1
            
            monthly_savings = savings_target / timeline
            savings_rate = (monthly_savings / (annual_income / 12)) * 100
            balance_36mo = monthly_savings * 36
            
            if calc_result.get('completion_date'):
                completion_date = str(calc_result.get('completion_date'))
            else:
                completion_date = str(date.today() + relativedelta(months=timeline))
                
            total_contributed = annual_income - savings_target
            timetogoal = timeline

            history = [int(row.get('monthly_contributed') or 0) for row in extra_results]
            debt_history = [int(row.get('debt_contributions') or 0) for row in extra_results]

            months_labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            monthly_averages_chart = [0] * 12
            expenses_by_month = {row['month_name']: float(row['total_spent'] or 0) for row in expense_results}

            for index, row in enumerate(extra_results):
                if index >= 12:
                    break

                m_cont = float(row.get('monthly_contributed') or 0)
                d_cont = float(row.get('debt_contributions') or 0)
                e_cont = float(row.get('emergency_contribtuions') or 0)
                gross_pool = m_cont + d_cont + e_cont

                current_month_name = months_labels[index]
                var_expense = expenses_by_month.get(current_month_name, 0)

                net_surplus = gross_pool - (var_expense + total_subscription)
                monthly_averages_chart[index] = round(net_surplus, 2)

            return jsonify({
                "profile": {
                    "monthly_savings": round(monthly_savings, 2),
                    "savings_rate": round(savings_rate, 1),
                    "balance_36mo": round(balance_36mo, 2),
                    "completion_date": completion_date,
                    "total_contributed": total_contributed,
                    "time_to_goal": timetogoal,
                    "savings_target": savings_target
                },
                "base_savings": base_savings,
                "savings_history": history,
                "debt": debt_history,
                "monthly_averages_chart": monthly_averages_chart
            }), 200

    except Exception as e:
        print(f"Failed to fetch home metrics data: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()
    
@app.route("/settings", methods=["POST"])
def extra_data():
    data = request.json or {}

    def clean(key, is_numeric=False):
        val = data.get(key)
        if val is None or str(val).strip() == "":
            return 0 if is_numeric else None
        return val

    # 1. Grab your metric contributions (will be 0 if null/untouched was sent)
    monthly_cont = clean('monthly_contributed', is_numeric=True) 
    debt_cont = clean('debt_contributions', is_numeric=True) 
    emergency_cont = clean('emergency_contribution', is_numeric=True) 
    
    # 2. Grab transactional items
    subscription_name = clean('subscription_name') 
    subscription_price = clean('subscription_price', is_numeric=True) 
    subscription_status = clean('subscription_status') 
    transaction_name = clean('transaction_name') 
    transaction_value = clean('transaction_price', is_numeric=True) 
    transaction_date = clean('transaction_date')

    if not transaction_date or str(transaction_date).strip() == "":
        transaction_date = date.today().strftime('%Y-%m-%d')

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # ONLY log to extradata if at least one metric is strictly greater than 0
            if monthly_cont > 0 or debt_cont > 0 or emergency_cont > 0:
                metrics_sql = """
                    INSERT INTO extradata (monthly_contributed, debt_contributions, emergency_contribtuions) 
                    VALUES (%s, %s, %s)
                """
                cursor.execute(metrics_sql, (monthly_cont, debt_cont, emergency_cont))

            # If a single transaction was added, send it to its own ledger
            if transaction_name:
                tx_sql = """
                    INSERT INTO transaction_ledger (transaction_name, transaction_value, transaction_date) 
                    VALUES (%s, %s, %s)
                """
                cursor.execute(tx_sql, (transaction_name, transaction_value, transaction_date))

            # If a single subscription was added, send it to its own ledger
            if subscription_name:
                sub_sql = """
                    INSERT INTO subscription_ledger (subscription_name, subscription_price, subscriptions_status) 
                    VALUES (%s, %s, %s)
                """
                cursor.execute(sub_sql, (subscription_name, subscription_price, subscription_status))

        connection.commit()
        return jsonify({"message": "All data processed successfully"}), 201
    except Exception as e:
        connection.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

@app.route("/Transactions", methods=['GET'])
def fetch_trans():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, transaction_name, transaction_value, transaction_date FROM transaction_ledger ORDER BY id DESC")
            return jsonify(cursor.fetchall()), 200
    finally: 
        connection.close()

@app.route("/Transactions/<int:tx_id>", methods=['DELETE'])
def delete_trans(tx_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM transaction_ledger WHERE id = %s", (tx_id,))
            connection.commit()
        return jsonify({"message": "Deleted transaction"}), 200
    finally: 
        connection.close()

@app.route("/api/subscriptions", methods=['GET'])
def fetch_subscription():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, subscription_name, subscription_price, subscriptions_status FROM subscription_ledger ORDER BY id DESC")
            return jsonify(cursor.fetchall()), 200
    finally: 
        connection.close()

@app.route("/api/subscriptions/<int:sub_id>", methods=['DELETE'])
def delete_subscription(sub_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM subscription_ledger WHERE id = %s", (sub_id,))
            connection.commit()
        return jsonify({"message": "Deleted subscription"}), 200
    finally: 
        connection.close()

@app.route("/Reports", methods=["GET"])
def sendInfo():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # 1. Get baseline targets and configurations
            cursor.execute("SELECT savings_target, total_savings, emergency_fund FROM calculation_table ORDER BY id DESC LIMIT 1")
            calc_row = cursor.fetchone()
            
            cursor.execute("SELECT monthly_contributed, emergency_contribtuions FROM extradata ORDER BY id ASC")
            extra_rows = cursor.fetchall()

            # 2. Query for subscription costs to accurately reflect fixed costs if needed
            cursor.execute("SELECT SUM(subscription_price) as total_subs FROM subscription_ledger")
            sub_result = cursor.fetchone()
            total_subs = float(sub_result.get('total_subs') or 0) if sub_result else 0

            # 3. Query transaction totals grouped by month for the variable costs line
            cursor.execute("""
                SELECT DATE_FORMAT(transaction_date, '%M') as month_name, SUM(transaction_value) as total_spent
                FROM transaction_ledger
                GROUP BY DATE_FORMAT(transaction_date, '%M'), MONTH(transaction_date)
                ORDER BY MONTH(transaction_date) ASC
            """)
            expense_results = cursor.fetchall()

        # Build dynamic lists for the deep dive chart visualization
        months_labels = ["July", "August", "September", "October", "November", "December"]
        
        # Build dictionary from database tracking results
        expenses_by_month = {row['month_name']: float(row['total_spent'] or 0) for row in expense_results}
        
        # Map values or fall back to your dashboard default template rules smoothly
        fixed_costs_timeline = [2200 for _ in months_labels]  # Base fixed target line
        variable_costs_timeline = [int(expenses_by_month.get(m, 0)) for m in months_labels]
        
        # If no custom data is generated yet, supply your frontend template fallback values
        if all(v == 0 for v in variable_costs_timeline):
            variable_costs_timeline = [750, 800, 1450, 1220, 920, 1720]

        if calc_row:
            payload = {
                "savings_target": calc_row.get("savings_target", 0),
                "base_savings": int(calc_row.get("total_savings", 0)),
                "emergency_target": int(calc_row.get("emergency_fund", 0)),
                "savings_history": [int(r.get("monthly_contributed", 0)) for r in extra_rows],
                "emergency_history": [int(r.get("emergency_contribtuions", 0)) for r in extra_rows],
                # Add this key back in so Vue can read it!
                "deep_dive": {
                    "months": months_labels,
                    "fixed_costs": fixed_costs_timeline,
                    "variable_costs": variable_costs_timeline
                }
            }
        else:
            payload = {
                "savings_target": 0, 
                "base_savings": 0, 
                "emergency_target": 0, 
                "savings_history": [], 
                "emergency_history": [],
                "deep_dive": {
                    "months": months_labels,
                    "fixed_costs": [2200] * 6,
                    "variable_costs": [750, 800, 1450, 1220, 920, 1720]
                }
            }

        return jsonify(payload), 200
    except Exception as e:
        print(f"Failed to compile report payload: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000)