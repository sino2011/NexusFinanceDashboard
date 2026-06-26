import os
from datetime import date
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import pymysql
from dateutil.relativedelta import relativedelta

load_dotenv()

# Fixed trailing typo 'a' at the end
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'Yassin2011')
DB_NAME = os.getenv('DB_NAME', 'nexusfinancedashboard')

app = Flask(__name__)

# Core CORS setup (handles preflights automatically)
CORS(
    app,
    resources={r"/*": {"origins": ["https://sino2011.github.io", "http://localhost:5173"]}},
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    supports_credentials=True
)

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "yassin2011")
jwt = JWTManager(app)
db_config = {
    'host': DB_HOST,
    'user': DB_USER,
    'password': DB_PASSWORD,
    'database': DB_NAME,
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db_connection():
    return pymysql.connect(**db_config)

@app.route("/login", methods=["POST"])
def login():
    connection = None
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get("password")
        if not email or not password:
            return jsonify({"error": "Email and password required"}), 400

        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = """SELECT id, pass FROM userinfo WHERE email = %s"""
            cursor.execute(sql, (email,))
            user = cursor.fetchone()

            if user and user['pass'] == password:
                access_token = create_access_token(identity=str(user['id']))
                return jsonify({
                    "message": "Login successful",
                    "token": access_token,
                    "user_id": user['id']
                }), 200

            return jsonify({"error": "Invalid email or password"}), 401
    except Exception as e:
        if connection:
            connection.rollback()
        print(f"Login failed: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        if connection:
            connection.close()

@app.route("/api/calculate", methods=['POST'])
def save_calculations():
    data = request.get_json()
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
                INSERT INTO userinfo (first_name, last_name, date_birth, pass, email)
                VALUES(%s, %s, %s, %s, %s)
            """
            cursor.execute(user_sql, (first_name, last_name, date_birth, passw, email))
            user_id = int(cursor.lastrowid)

            calc_sql = """
                INSERT INTO calculation_table (annual_income, savings_target, timeline, total_savings, emergency_fund, completion_date, user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(calc_sql, (annual_income, savings_target, timeline, total_savings, emergency_fund, calculated_completion, user_id))

        connection.commit()
        access_token = create_access_token(identity=str(user_id))

        return jsonify({
            "message": "Profile and Calculation saved successfully",
            "token": access_token,
            "user_id": user_id
        }), 201

    except Exception as e:
        connection.rollback()
        print(f"Database insertion failed: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

@app.route("/home", methods=['GET'])
@jwt_required()
def fetch_info():
    user_id = get_jwt_identity()
    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid token identity structure"}), 400

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT total_savings, savings_target, timeline, annual_income, completion_date FROM calculation_table WHERE user_id = %s ORDER BY id DESC LIMIT 1", (user_id,))
            calc_result = cursor.fetchone()

            cursor.execute("SELECT monthly_contributed, debt_contributions, emergency_contribtuions FROM extradata WHERE user_id = %s ORDER BY id ASC", (user_id,))
            extra_results = cursor.fetchall() or []

            cursor.execute("SELECT SUM(subscription_price) as total_subs FROM subscription_ledger WHERE user_id = %s", (user_id,))
            sub_result = cursor.fetchone()

            total_subscription = 0.0
            if sub_result and sub_result.get('total_subs') is not None:
                total_subscription = float(sub_result['total_subs'])

            cursor.execute("""
                    SELECT DATE_FORMAT(transaction_date, '%M') as month_name, SUM(transaction_value) as total_spent
                    FROM transaction_ledger
                    WHERE user_id = %s AND transaction_date IS NOT NULL
                    GROUP BY DATE_FORMAT(transaction_date, '%M'), MONTH(transaction_date)
                    ORDER BY MONTH(transaction_date) ASC
            """, (user_id,))
            expense_results = cursor.fetchall() or []

            if not calc_result:
                return jsonify({
                    "profile": {
                        "monthly_savings": 0, "savings_rate": 0, "balance_36mo": 0,
                        "completion_date": str(date.today()), "total_contributed": 0,
                        "time_to_goal": 12, "savings_target": 1000
                    },
                    "base_savings": 0, "savings_history": [], "debt": [], "monthly_averages_chart": [0] * 12
                }), 200

            base_savings = float(calc_result.get('total_savings') or 0)
            savings_target = float(calc_result.get('savings_target') or 0)

            timeline = int(calc_result.get('timeline') or 12)
            if timeline <= 0:
                timeline = 12

            annual_income = float(calc_result.get('annual_income') or 1)
            if annual_income <= 0:
                annual_income = 1

            monthly_savings = savings_target / timeline
            savings_rate = (monthly_savings / (annual_income / 12)) * 100
            balance_36mo = monthly_savings * 36
            completion_date = str(calc_result.get('completion_date')) if calc_result.get('completion_date') else str(date.today() + relativedelta(months=timeline))
            total_contributed = max(0.0, annual_income - savings_target)
            timetogoal = timeline

            history = [int(float(row.get('monthly_contributed') or 0)) for row in extra_results]
            debt_history = [int(float(row.get('debt_contributions') or 0)) for row in extra_results]

            months_labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            monthly_averages_chart = [0.0] * 12

            expenses_by_month = {}
            for row in expense_results:
                if row and row.get('month_name'):
                    m_name = str(row['month_name']).strip()
                    expenses_by_month[m_name] = float(row.get('total_spent') or 0)

            for index, row in enumerate(extra_results):
                if index >= 12:
                    break

                m_cont = float(row.get('monthly_contributed') if row.get('monthly_contributed') is not None else 0)
                d_cont = float(row.get('debt_contributions') if row.get('debt_contributions') is not None else 0)
                e_cont = float(row.get('emergency_contribtuions') if row.get('emergency_contribtuions') is not None else 0)

                gross_pool = m_cont + d_cont + e_cont
                current_month_name = months_labels[index]
                var_expense = float(expenses_by_month.get(current_month_name, 0.0))

                net_surplus = gross_pool - (var_expense + total_subscription)
                monthly_averages_chart[index] = round(net_surplus, 2)

            return jsonify({
                "profile": {
                    "monthly_savings": round(monthly_savings, 2),
                    "savings_rate": round(savings_rate, 1),
                    "balance_36mo": round(balance_36mo, 2),
                    "completion_date": completion_date,
                    "total_contributed": round(total_contributed, 2),
                    "time_to_goal": timetogoal,
                    "savings_target": savings_target
                },
                "base_savings": base_savings,
                "savings_history": history,
                "debt": debt_history,
                "monthly_averages_chart": monthly_averages_chart
            }), 200
    except Exception as e:
        print(f"CRITICAL ERROR compile home payload: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

@app.route("/settings", methods=["POST"])
@jwt_required()
def extra_data():
    user_id = get_jwt_identity()
    data = request.get_json() or {}

    def clean(key, is_numeric=False):
        val = data.get(key)
        if val is None or str(val).strip() == "":
            return 0 if is_numeric else None
        return val

    monthly_cont = clean('monthly_contributed', is_numeric=True)
    debt_cont = clean('debt_contributions', is_numeric=True)
    emergency_cont = clean('emergency_contribution', is_numeric=True)
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
            if monthly_cont > 0 or debt_cont > 0 or emergency_cont > 0:
                metrics_sql = """
                    INSERT INTO extradata (monthly_contributed, debt_contributions, emergency_contribtuions, user_id)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(metrics_sql, (monthly_cont, debt_cont, emergency_cont, user_id))

            if transaction_name:
                tx_sql = """
                    INSERT INTO transaction_ledger (transaction_name, transaction_value, transaction_date, user_id)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(tx_sql, (transaction_name, transaction_value, transaction_date, user_id))

            if subscription_name:
                sub_sql = """
                    INSERT INTO subscription_ledger (subscription_name, subscription_price, subscriptions_status, user_id)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sub_sql, (subscription_name, subscription_price, subscription_status, user_id))

        connection.commit()
        return jsonify({"message": "All data processed successfully"}), 201
    except Exception as e:
        connection.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

@app.route("/Transactions", methods=['GET'])
@jwt_required()
def fetch_trans():
    user_id = get_jwt_identity()
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, transaction_name, transaction_value, transaction_date FROM transaction_ledger WHERE user_id = %s ORDER BY id DESC", (user_id,))
            return jsonify(cursor.fetchall()), 200
    finally:
        connection.close()

@app.route("/Transactions/<int:tx_id>", methods=['DELETE'])
@jwt_required()
def delete_trans(tx_id):
    user_id = get_jwt_identity()
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM transaction_ledger WHERE id = %s AND user_id = %s", (tx_id, user_id))
            connection.commit()
        return jsonify({"message": "Deleted transaction"}), 200
    finally:
        connection.close()

@app.route("/api/subscriptions", methods=['GET'])
@jwt_required()
def fetch_subscription():
    user_id = get_jwt_identity()
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, subscription_name, subscription_price, subscriptions_status FROM subscription_ledger WHERE user_id = %s ORDER BY id DESC", (user_id,))
            return jsonify(cursor.fetchall()), 200
    finally:
        connection.close()

@app.route("/api/subscriptions/<int:sub_id>", methods=['DELETE'])
@jwt_required()
def delete_subscription(sub_id):
    user_id = get_jwt_identity()
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM subscription_ledger WHERE id = %s AND user_id = %s", (sub_id, user_id))
            connection.commit()
        return jsonify({"message": "Deleted subscription"}), 200
    finally:
        connection.close()

@app.route("/Reports", methods=["GET"])
@jwt_required()
def sendInfo():
    user_id = get_jwt_identity()
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT savings_target, total_savings, emergency_fund FROM calculation_table WHERE user_id = %s ORDER BY id DESC LIMIT 1", (user_id,))
            calc_row = cursor.fetchone()

            cursor.execute("SELECT monthly_contributed, emergency_contribtuions FROM extradata WHERE user_id = %s ORDER BY id ASC", (user_id,))
            extra_rows = cursor.fetchall()

            cursor.execute("SELECT SUM(subscription_price) as total_subs FROM subscription_ledger WHERE user_id = %s", (user_id,))
            sub_result = cursor.fetchone()
            total_subs = float(sub_result.get('total_subs') or 0) if sub_result and sub_result.get('total_subs') else 0.0

            cursor.execute("""
                SELECT DATE_FORMAT(transaction_date, '%M') as month_name, SUM(transaction_value) as total_spent
                FROM transaction_ledger
                WHERE user_id = %s
                GROUP BY DATE_FORMAT(transaction_date, '%M'), MONTH(transaction_date)
                ORDER BY MONTH(transaction_date) ASC
            """, (user_id,))
            expense_results = cursor.fetchall()

        months_labels = ["July", "August", "September", "October", "November", "December"]

        expenses_by_month = {}
        if expense_results:
            for row in expense_results:
                if row and row.get('month_name'):
                    expenses_by_month[row['month_name']] = float(row.get('total_spent') or 0)

        fixed_costs_timeline = [2200 for _ in months_labels]
        variable_costs_timeline = [int(float(expenses_by_month.get(m, 0))) for m in months_labels]

        if all(v == 0 for v in variable_costs_timeline):
            variable_costs_timeline = [750, 800, 1450, 1220, 920, 1720]

        if calc_row:
            payload = {
                "savings_target": float(calc_row.get("savings_target") or 0),
                "base_savings": int(float(calc_row.get("total_savings") or 0)),
                "emergency_target": int(float(calc_row.get("emergency_fund") or 0)),
                "savings_history": [int(float(r.get("monthly_contributed") or 0)) for r in extra_rows],
                "emergency_history": [int(float(r.get("emergency_contribtuions") or 0)) for r in extra_rows],
                "deep_dive": {
                    "months": months_labels,
                    "fixed_costs": fixed_costs_timeline,
                    "variable_costs": variable_costs_timeline
                }
            }
        else:
            payload = {
                "savings_target": 0, "base_savings": 0, "emergency_target": 0, "savings_history": [], "emergency_history": [],
                "deep_dive": {
                    "months": months_labels, "fixed_costs": [2200] * 6, "variable_costs": [750, 800, 1450, 1220, 920, 1720]
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