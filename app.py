from flask import *
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login_page.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False 

db = SQLAlchemy(app)

class Login(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    email = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)

@app.route("/", methods = ["POST","GET"])
def insert():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        record = Login(email = email, password = password)
        db.session.add(record)
        db.session.commit()
        db.session.close()
        return redirect("/view")
    else:
        return render_template("form.html")

@app.route("/view")
def view():
    all_rec = Login.query.all()
    return render_template("view.html", records = all_rec)

@app.route("/delete/<int:id>", methods = ["POST","GET"])
def delete(id):
    rec = Login.query.get(id)
    db.session.delete(rec)
    db.session.commit()
    db.session.close()
    return redirect("/view")

@app.route("/update/<int:id>", methods = ["POST","GET"])
def update(id):
    rec = Login.query.get(id)
    if request.method == "POST":
        rec.email = request.form["email"]
        rec.password = request.form["password"]
        db.session.commit()
        db.session.close()
        return redirect("/view")
    else:
        return render_template("update.html", rec = rec)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug = True)