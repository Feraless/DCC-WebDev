from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)
db = yaml.safe_load(open("db.yaml"))
app.config["MYSQL_HOST"] = db["mysql_host"]
app.config["MYSQL_USER"] = db["mysql_user"]
app.config["MYSQL_PASSWORD"] = db["mysql_password"]
app.config["MYSQL_DB"] = db["mysql_db"]
mysql = MySQL(app)


@app.route("/", methods=["GET", "POST"])
def about():
    if request.method == "POST":
        bondno = request.form['bond_number']
        cur = mysql.connection.cursor()
        query = """
            (SELECT * FROM company_name WHERE `Bond\nNumber` = %s)
            UNION
            (SELECT * FROM political_party WHERE `Bond\nNumber` = %s)
        """
        cur.execute(query, (bondno, bondno))
        result = cur.fetchall()
        cur.close()
        print("Fetched data:", result)
        return render_template("home.html", result=result)
    return render_template("about.html")


@app.route("/home")
def info():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
