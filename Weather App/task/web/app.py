from flask import Flask, render_template, request, redirect, url_for, flash
import sys, random
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
db = SQLAlchemy(app)


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=True)

    def __repr__(self):
        return '<City %r>' % self.name


db.create_all()
db.session.commit()


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':

        city = request.form['city_name']

        if not city.isalpha():
            flash("The city doesn't exist!")
            return redirect('/')

        if City.query.filter_by(name=city).first():
            flash("The city has already been added to the list!")
            return redirect('/')

        new_city = City(name=city)
        db.session.add(new_city)
        db.session.commit()
        return redirect(url_for('index'))
    # the code below is executed if the request method
    # was GET or the credentials were invalid

    cities = City.query.all()
    weather = []
    for city in cities:
        degree = random.randint(20, 30)
        state = random.choice(['rainy', 'wet', 'humid', 'dry', 'arid', 'frigid', 'foggy', 'windy', 'stormy'])
        weather.append({'degree': degree, 'city': city, 'state': state, 'city_id': city.id})

    return render_template('index.html', weather=weather)


@app.route('/delete/<city_id>', methods=['GET', 'POST'])
def delete(city_id):
    city = City.query.filter_by(id=city_id).first()
    db.session.delete(city)
    db.session.commit()
    return redirect('/')

# don't change the following way to run flask:
if __name__ == '__main__':
    app.secret_key = 'super secret key'
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
