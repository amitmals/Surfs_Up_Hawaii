import sqlalchemy
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import datetime as dt
from sqlalchemy.orm import scoped_session, sessionmaker

from flask import Flask, json, jsonify

#################################################
# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = scoped_session(sessionmaker(bind=engine))

# Find the last date
last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
one_year_ago = dt.datetime.strptime(last_date, '%Y-%m-%d') - dt.timedelta(days=365)

#################################################
# Flask Setup
app = Flask(__name__)

# Flask Routes

@app.route("/")
def welcome():
    return (
        f"<br/>--List of all the routes that are available--<br/>"
        f"<br/>Returns the dates and rainfall(precipitation):<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>Returns a list of stations<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>Returns a list of Temperature for the previous year:<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>Returns the minimum, average and maximum temperature for a date<br/>"
        f"/api/v1.0/start_date<br/>"
        f"<br/>Returns the minimum, average and maximum temperature for a start and end date<br/>"
        f"/api/v1.0/start_date/end_date<br/>"
        f"<br/>-Dates are in YYYY-MM-DD format"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    precipitation_data = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date).all()
    precipitation_dict = dict(precipitation_data)
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    station_data = session.query(Station.station, Station.name).order_by(Station.station).all()
    station_dict = dict(station_data)
    return jsonify(station_dict)    

@app.route("/api/v1.0/tobs")
def temps_last_yr():
    temps_last_yr_data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date>=one_year_ago)
    temps_last_yr_dict = dict(temps_last_yr_data)
    return jsonify(temps_last_yr_dict)

@app.route("/api/v1.0/<start>")
def temps_from_date1(start):
    day_temp1 = session.query(func.min(Measurement.tobs) ,func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date>=start).all()
    dict1 = {"Min_Temp": day_temp1[0][0], "Avg_Temp": day_temp1[0][1], "Max_Temp": day_temp1[0][2]}
    return jsonify(dict1)

@app.route("/api/v1.0/<start>/<end>")
def temps_from_date2(start,end):
    day_temp2 = session.query(func.min(Measurement.tobs) ,func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date>=start).filter( Measurement.date<=end).all()
    dict2 = {"Min_Temp": day_temp2[0][0], "Avg_Temp": day_temp2[0][1], "Max_Temp": day_temp2[0][2]}
    return jsonify(dict2)

if __name__ == "__main__":
    app.run(debug=True)