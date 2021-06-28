from flask import Flask, render_template, request, redirect
import requests
import json
import pandas as pd
import numpy as np


app = Flask(__name__)

url = "cost.csv"
sda = []

df = pd.read_csv(url,error_bad_lines=False)
df = df.rename(columns={'rgrp3':'Child', 'rgrp4': 'Blind/Disabled','rgrp6':'Telemonitoring','sfy':'Year','SDA' : 'Region','tot_tvst':'Televisits'})
df = df.fillna(0)
df = df[["Region","Year","Televisits","Blind/Disabled","Child","Telemonitoring","treat","meas","type","post"]]

sda = (df['Region'].unique())

sda = np.roll(sda,2)
sda = sda[sda!=0]
nclients = df[df['meas']=='nclient']
med_df = df[df['type']=='med']

#pre cost
med_df_precost = med_df[med_df['post']==0]
#post cost
med_df_postcost = med_df[med_df['post']==1]

texas_nclient = nclients[nclients['Region']=='Texas']
texas_nclient=texas_nclient.drop(['type','post','meas'],axis=1)
texas_nclient = texas_nclient.sort_values(by=['treat'])
texas_nclient['Child'] = texas_nclient['Child'].map('{:,.0f}'.format)
texas_nclient['Blind/Disabled'] = texas_nclient['Blind/Disabled'].map('{:,.0f}'.format)
texas_nclient['Telemonitoring'] = texas_nclient['Telemonitoring'].map('{:,.0f}'.format)
texas_nclient['Televisits'] = texas_nclient['Televisits'].map('{:,.0f}'.format)
texas_nclient_tele = texas_nclient[texas_nclient['treat']==1]
texas_nclient_nontele = texas_nclient[texas_nclient['treat']==0]
texas_nclient_tele=texas_nclient_tele.drop(['treat'],axis=1)
texas_nclient_nontele=texas_nclient_nontele.drop(['treat'],axis=1)


texas_precost = med_df_precost[med_df_precost['Region']=='Texas']
texas_precost=texas_precost.drop(['type','post','meas'],axis=1)
texas_precost['Blind/Disabled'] = texas_precost['Blind/Disabled'].apply(np.round)
texas_precost['Child'] = texas_precost['Child'].apply(np.round)
texas_precost['Telemonitoring'] = texas_precost['Telemonitoring'].apply(np.round)
texas_precost = texas_precost.sort_values(by=['treat'])
texas_precost['Child'] = texas_precost['Child'].map('${:,.0f}'.format)
texas_precost['Blind/Disabled'] = texas_precost['Blind/Disabled'].map('${:,.0f}'.format)
texas_precost['Telemonitoring'] = texas_precost['Telemonitoring'].map('${:,.0f}'.format)
texas_precost['Televisits'] = texas_precost['Televisits'].map('${:,.0f}'.format)
texas_precost_tele = texas_precost[texas_precost['treat']==1]
texas_precost_nontele = texas_precost[texas_precost['treat']==0]
texas_precost_tele=texas_precost_tele.drop(['treat'],axis=1)
texas_precost_nontele=texas_precost_nontele.drop(['treat'],axis=1)




texas_postcost = med_df_postcost[med_df_postcost['Region']=='Texas']
texas_postcost=texas_postcost.drop(['type','post','meas'],axis=1)
texas_postcost['Blind/Disabled'] = texas_postcost['Blind/Disabled'].apply(np.round)
texas_postcost['Child'] = texas_postcost['Child'].apply(np.round)
texas_postcost['Telemonitoring'] = texas_postcost['Telemonitoring'].apply(np.round)
texas_postcost = texas_postcost.sort_values(by=['treat'])
texas_postcost['Child'] = texas_postcost['Child'].map('${:,.0f}'.format)
texas_postcost['Blind/Disabled'] = texas_postcost['Blind/Disabled'].map('${:,.0f}'.format)
texas_postcost['Telemonitoring'] = texas_postcost['Telemonitoring'].map('${:,.0f}'.format) 
texas_postcost['Televisits'] = texas_postcost['Televisits'].map('${:,.0f}'.format)
texas_postcost_tele = texas_postcost[texas_postcost['treat']==1]
texas_postcost_nontele = texas_postcost[texas_postcost['treat']==0]
texas_postcost_tele=texas_postcost_tele.drop(['treat'],axis=1)
texas_postcost_nontele=texas_postcost_nontele.drop(['treat'],axis=1)

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
        num_client = nclients[nclients['Region']==sda_name]
        num_client = num_client.sort_values(by=['treat'])
        num_client=num_client.drop(['type','post','meas'],axis=1)
        num_client['Child'] = num_client['Child'].map('{:,.0f}'.format)
        num_client['Blind/Disabled'] = num_client['Blind/Disabled'].map('{:,.0f}'.format)
        num_client['Telemonitoring'] = num_client['Telemonitoring'].map('{:,.0f}'.format)
        num_client['Televisits'] = num_client['Televisits'].map('{:,.0f}'.format)
        numclient_tele = num_client[num_client['treat']==1]
        numclient_nontele = num_client[num_client['treat']==0]
        numclient_tele=numclient_tele.drop(['treat'],axis=1)
        numclient_nontele=numclient_nontele.drop(['treat'],axis=1)

        df_precost = med_df_precost[med_df_precost['Region']==sda_name]
        df_precost = df_precost.sort_values(by=['treat'])
        df_precost=df_precost.drop(['type','post','meas'],axis=1)
        df_precost['Blind/Disabled'] = df_precost['Blind/Disabled'].apply(np.round)
        df_precost['Child'] = df_precost['Child'].apply(np.round)
        df_precost['Telemonitoring'] = df_precost['Telemonitoring'].apply(np.round)
        df_precost['Child'] = df_precost['Child'].map('${:,.0f}'.format)
        df_precost['Blind/Disabled'] = df_precost['Blind/Disabled'].map('${:,.0f}'.format)
        df_precost['Telemonitoring'] = df_precost['Telemonitoring'].map('${:,.0f}'.format)
        df_precost['Televisits'] = df_precost['Televisits'].map('${:,.0f}'.format)
        precost_tele = df_precost[df_precost['treat']==1]
        precost_nontele = df_precost[df_precost['treat']==0]
        precost_tele=precost_tele.drop(['treat'],axis=1)
        precost_nontele=precost_nontele.drop(['treat'],axis=1)

        df_postcost = med_df_postcost[med_df_postcost['Region']==sda_name]
        df_postcost = df_postcost.sort_values(by=['treat'])
        df_postcost=df_postcost.drop(['type','post','meas'],axis=1)
        df_postcost['Blind/Disabled'] = df_postcost['Blind/Disabled'].apply(np.round)
        df_postcost['Child'] = df_postcost['Child'].apply(np.round)  
        df_postcost['Telemonitoring'] = df_postcost['Telemonitoring'].apply(np.round)   
        df_postcost['Child'] = df_postcost['Child'].map('${:,.0f}'.format)
        df_postcost['Blind/Disabled'] = df_postcost['Blind/Disabled'].map('${:,.0f}'.format)
        df_postcost['Telemonitoring'] = df_postcost['Telemonitoring'].map('${:,.0f}'.format)     
        df_postcost['Televisits'] = df_postcost['Televisits'].map('${:,.0f}'.format)
        postcost_tele = df_postcost[df_postcost['treat']==1]
        postcost_nontele = df_postcost[df_postcost['treat']==0]
        postcost_tele=postcost_tele.drop(['treat'],axis=1)
        postcost_nontele=postcost_nontele.drop(['treat'],axis=1)

        if sda_name != None:
            return render_template("medcost.html", sda_name=sda_name, sda=sda, numclient_tele=[numclient_tele.to_html(index = False)],numclient_nontele=[numclient_nontele.to_html(index = False)],
                                    precost_tele=[precost_tele.to_html(index = False)], precost_nontele=[precost_nontele.to_html(index = False)],postcost_tele=[postcost_tele.to_html(index = False)], postcost_nontele=[postcost_nontele.to_html(index = False)])
    
    return render_template('medcost1.html',sda=sda, texas_nclient_tele=[texas_nclient_tele.to_html(index=False)], texas_nclient_nontele=[texas_nclient_nontele.to_html(index=False)], texas_precost_tele=[texas_precost_tele.to_html(index=False)], 
                            texas_precost_nontele=[texas_precost_nontele.to_html(index=False)], texas_postcost_tele=[texas_postcost_tele.to_html(index = False)],  texas_postcost_nontele=[texas_postcost_nontele.to_html(index = False)])
    
    

@app.route('/documents', methods = ["GET","POST"])
def documents(): 
    return render_template('documents.html')

if __name__ == "__main__":
    app.run(debug=True) 