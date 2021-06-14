from flask import Flask, render_template, request, redirect
import requests
import json


app = Flask(__name__)

@app.route('/', methods=["GET","POST"])
def index():
    #intervention_cost = ['Medical','Non Medical']
    if request.method == 'POST':
        intervention = request.form['intervention']
        intervention_period = request.form['intervention_period']
        intervention_cost = request.form['intervention_cost']
        net_cost = float(request.form['net_cost'])
        outcome_change = float(request.form['outcome_change'])

        return render_template('result.html', intervention = intervention, intervention_period=intervention_period,intervention_cost=intervention_cost, net_cost=net_cost, outcome_change=outcome_change)
    return render_template('index.html')


    
if __name__ == "__main__":
    app.run() 