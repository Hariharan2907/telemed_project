from flask import Flask, render_template, request, redirect
import requests
import json
import pandas as pd
import numpy as np


app = Flask(__name__)

url = "cost.csv"
sda = []

df = pd.read_csv(url,error_bad_lines=False)
df = df.dropna()
df = df.rename(columns={'rgrp3':'Child', 'rgrp4': 'Blind/Disabled','rgrp6':'Telemonitoring','sfy':'Year'})
sda = (df['SDA'].unique())



print(sda)


nclients = df[df['meas']=='nclient']
med_df = df[df['type']=='med']
#pre cost
med_df_precost = med_df[med_df['post']==0]
#post cost
med_df_postcost = med_df[med_df['post']==1]

texas_nclient = nclients[nclients['SDA']=='Texas']
texas_nclient=texas_nclient.drop(['type','post','meas','tot_tvst'],axis=1)
texas_nclient['Blind/Disabled'] = texas_nclient['Blind/Disabled'].astype('int64')
texas_nclient['Child'] = texas_nclient['Child'].astype('int64')
texas_nclient['Telemonitoring'] = texas_nclient['Telemonitoring'].astype('int64')

texas_precost = med_df_precost[med_df_precost['SDA']=='Texas']
texas_precost=texas_precost.drop(['type','post','meas','tot_tvst'],axis=1)
texas_precost['Blind/Disabled'] = texas_precost['Blind/Disabled'].apply(np.ceil)
texas_precost['Blind/Disabled'] = texas_precost['Blind/Disabled'].astype('int64')
texas_precost['Child'] = texas_precost['Child'].apply(np.ceil)
texas_precost['Child'] = texas_precost['Child'].astype('int64')
texas_precost['Telemonitoring'] = texas_precost['Telemonitoring'].apply(np.ceil)
texas_precost['Telemonitoring'] = texas_precost['Telemonitoring'].astype('int64')

texas_postcost = med_df_postcost[med_df_postcost['SDA']=='Texas']
texas_postcost=texas_postcost.drop(['type','post','meas','tot_tvst'],axis=1)
texas_postcost['Blind/Disabled'] = texas_postcost['Blind/Disabled'].apply(np.ceil)
texas_postcost['Blind/Disabled'] = texas_postcost['Blind/Disabled'].astype('int64')
texas_postcost['Child'] = texas_postcost['Child'].apply(np.ceil)
texas_postcost['Child'] = texas_postcost['Child'].astype('int64')
texas_postcost['Telemonitoring'] = texas_postcost['Telemonitoring'].apply(np.ceil)
texas_postcost['Telemonitoring'] = texas_postcost['Telemonitoring'].astype('int64')



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
        num_client = num_client.sort_values(by=['treat'])
        num_client=num_client.drop(['type','post','meas','tot_tvst'],axis=1)
        num_client['Blind/Disabled'] = num_client['Blind/Disabled'].astype('int64')
        num_client['Child'] = num_client['Child'].astype('int64')
        num_client['Telemonitoring'] = num_client['Telemonitoring'].astype('int64')

        df_precost = med_df_precost[med_df_precost['SDA']==sda_name]
        df_precost = df_precost.sort_values(by=['treat'])
        df_precost=df_precost.drop(['type','post','meas','tot_tvst'],axis=1)
        df_precost['Blind/Disabled'] = df_precost['Blind/Disabled'].apply(np.ceil)
        df_precost['Blind/Disabled'] = df_precost['Blind/Disabled'].astype('int64')
        df_precost['Child'] = df_precost['Child'].apply(np.ceil)
        df_precost['Child'] = df_precost['Child'].astype('int64')
        df_precost['Telemonitoring'] = df_precost['Telemonitoring'].apply(np.ceil)
        df_precost['Telemonitoring'] = df_precost['Telemonitoring'].astype('int64')

        df_postcost = med_df_postcost[med_df_postcost['SDA']==sda_name]
        df_postcost = df_postcost.sort_values(by=['treat'])
        df_postcost=df_postcost.drop(['type','post','meas','tot_tvst'],axis=1)
        df_postcost['Blind/Disabled'] = df_postcost['Blind/Disabled'].apply(np.ceil)
        df_postcost['Blind/Disabled'] = df_postcost['Blind/Disabled'].astype('int64')
        df_postcost['Child'] = df_postcost['Child'].apply(np.ceil)
        df_postcost['Child'] = df_postcost['Child'].astype('int64')
        df_postcost['Telemonitoring'] = df_postcost['Telemonitoring'].apply(np.ceil)
        df_postcost['Telemonitoring'] = df_postcost['Telemonitoring'].astype('int64')

        if sda_name != None:
            return render_template("medcost.html", sda_name=sda_name, sda=sda, num_client=[num_client.to_html(classes='data')], df_precost=[df_precost.to_html(classes='data')], df_postcost=[df_postcost.to_html(classes='data')],  header = "true")
    return render_template('medcost1.html',sda=sda, texas_nclient=[texas_nclient.to_html(classes='data')], texas_precost=[texas_precost.to_html(classes='data')], texas_postcost=[texas_postcost.to_html(classes='data')])
    #return render_template('medcost.html', med_df_precost = [med_df_precost.to_html(classes='data')], header="true", med_df_postcost = [med_df_postcost.to_html(classes='data')])
    
if __name__ == "__main__":
    app.run(debug=True) 