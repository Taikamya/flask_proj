from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Database(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    complete = db.Column(db.Boolean)


@app.get("/")
def home():
    entry_list = db.session.query(Database).all()
    return render_template("base.html", entry_list=entry_list)

@app.post("/add")
def add():
    title = request.form.get("title")
    new_entry = Database(title=title, complete=False)
    db.session.add(new_entry)
    db.session.commit()
    return redirect(url_for("home"))

@app.get("/update/<int:entry_id>")
def update(entry_id):
    entry = db.session.query(Database).filter(Database.id == entry_id).first()
    entry.complete = not entry.complete
    db.session.commit()
    return redirect(url_for("home"))

@app.get("/delete/<int:entry_id>")
def delete(entry_id):
    entry = db.session.query(Database).filter(Database.id == entry_id).first()
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == '__main__':
    db.create_all()
    app.run()
