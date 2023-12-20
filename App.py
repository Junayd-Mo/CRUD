from flask import Flask, render_template, request, redirect, url_for,flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = 'Secret Key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)


class Data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(12))

    # def __init__(self, name, email, phone):
    #     self.name = name
    #     self.email = email
    #     self.phone = phone
    def __repr__(self):
        return '<Name %r>' % self.name

app.app_context().push()
db.create_all()

@app.route('/')
def Index():
    all_data = Data.query.all()
    return render_template("index.html",employees=all_data)

@app.route('/insert', methods = ['POST','GET'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        my_data = Data(name=name, email=email, phone=phone)
        db.session.add(my_data)
        db.session.commit()
        flash('Account created!', category='success')

        return redirect((url_for('Index')))
    return 'get method was used so insertion failed'

@app.route('/update',methods = ['GET', 'Post'])
def update():
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))

        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['Phone']

        db.session.commit()
        flash("Empolyee Updated Successfully")
        return redirect(url_for('Index'))


@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash('Employee Has Been Deleted!')
    return redirect(url_for('Index'))


if __name__ =='__main__':
    app.run(debug=True)