from flask import Flask, render_template, request, redirect
import requests
import json
import pandas as pd



app = Flask(__name__)

url = "cost.csv"
sda = []

df = pd.read_csv(url,error_bad_lines=False)
df = df.dropna()
sda = (df['SDA'].unique())

nclients = df[df['meas']=='nclient']
med_df = df[df['type']=='med']
#pre cost
med_df_precost = med_df[med_df['post']==0]
#post cost
med_df_postcost = med_df[med_df['post']==1]


@app.route('/', methods=["GET","POST"])
@app.route('/home', methods=["GET","POST"])
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

@app.route('/medcost', methods=["GET", "POST"])
def medcost():
    if request.method == "POST":
        sda_name = request.form.get("sda", None)
        num_client = nclients[nclients['SDA']==sda_name]
        num_client = num_client.sort_values(by=['sfy'])
        df_precost = med_df_precost[med_df_precost['SDA']==sda_name]
        df_precost = df_precost.sort_values(by=['sfy'])

        df_postcost = med_df_postcost[med_df_postcost['SDA']==sda_name]
        df_precost = df_precost.sort_values(by=['sfy'])
        
        if sda_name != None:
            return render_template("medcost.html", sda_name=sda_name, sda=sda, num_client=[num_client.to_html(classes='data')], df_precost=[df_precost.to_html(classes='data')], df_postcost=[df_postcost.to_html(classes='data')],  header = "true")
    return render_template('medcost.html',sda=sda)
    #return render_template('medcost.html', med_df_precost = [med_df_precost.to_html(classes='data')], header="true", med_df_postcost = [med_df_postcost.to_html(classes='data')])
    
if __name__ == "__main__":
    app.run(debug=True) 