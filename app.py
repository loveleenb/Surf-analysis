
#Import dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)
app = Flask(__name__)

@app.route("/")
def homepage():
    print("Request for Home page")
    return ("Welcome to Surfs Up")

@app.route("/welcome")
def welcome():
    """List all available api routes."""
    return (
        f"Routes Available:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    precp_results = session.query(Measurement.date, Measurement.prcp).all()
    prep_list = list(np.ravel(precp_results))
    prep_list = []
    for result in precp_results:
        precp_dict = {}
        precp_dict['date'] = result.date
        precp_dict['prcp'] = result.prcp
        prep_list.append(precp_dict)
    return jsonify(prep_list)

@app.route("/api/v1.0/stations")
def stations():
    station_results = session.query(Station.station).all()
    station_list = list(np.ravel(station_results))
    station_list = []
    for station in station_results:
        station_dict = {}
        station_dict['station'] = station.station
        station_list.append(station_dict)
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    tobs_results = session.query(Measurement.tobs).filter(Measurement.date >= "2016-08-23").all()
    tobs_list = []
    tobs_list = list(np.ravel(tobs_results))
    
    return jsonify(tobs_list)    

@app.route("/api/v1.0/tobs")
def tobs():
    tobs_results = session.query(Measurement.tobs).filter(Measurement.date >= "2016-08-23").all()
    tobs_list = []
    tobs_list = list(np.ravel(tobs_results))
    
    return jsonify(tobs_list)  

@app.route("/api/v1.0/<start>")
def temp_start_temp(start_date):

	temp_start = []

	temp_min = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start_date).all()
	temp_max = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()
	temp_avg = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).all()

	temp_start = list(np.ravel(temp_min,temp_max,temp_avg))

	return jsonify(temp_start)

@app.route("/api/v1.0/<start>/<end>")
def temp_start_end_temp(start_date, end_date):

	temp_start_end = []

	temp_min = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start_date, Measurement.date <= end_date).all()
	temp_max = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start_date, Measurement.date <= end_date).all()
	temp_avg = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start_date, Measurement.date <= end_date).all()

	temp_start_end = list(np.ravel(temp_min,temp_max,temp_avg))

	return jsonify(temp_start_end)


if __name__ == "__main__":
    app.run(debug=True)

  
