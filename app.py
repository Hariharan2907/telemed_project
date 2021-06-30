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

df['Other'] = df['Televisits']-df['Blind/Disabled']-df['Child']
df = df[["Region","Year","Blind/Disabled","Child","Other","Televisits","Telemonitoring","treat","meas","type","post"]]


sda = (df['Region'].unique())

sda = np.roll(sda,2)
sda = sda[sda!=0]
nclients = df[df['meas']=='nclient']

#----------------------------------------------------Medical Cost------------------------------------------#
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
texas_nclient['Other'] = texas_nclient['Other'].map('{:,.0f}'.format)
texas_nclient = texas_nclient.rename(columns={'Telemonitoring':'Total ','Televisits':'Total'})
texas_nclient_tele = texas_nclient[texas_nclient['treat']==1]
texas_nclient_nontele = texas_nclient[texas_nclient['treat']==0]
texas_nclient_tele=texas_nclient_tele.drop(['treat','Region'],axis=1)
texas_nclient_nontele=texas_nclient_nontele.drop(['treat','Region'],axis=1)
#texas_nclient_tele.columns=pd.MultiIndex.from_product([['Televisits'],texas_nclient_tele['Blind/Disabled'],texas_nclient_tele['Child'],texas_nclient_tele['Other']])


texas_precost = med_df_precost[med_df_precost['Region']=='Texas']
texas_precost=texas_precost.drop(['type','post','meas'],axis=1)
texas_precost['Blind/Disabled'] = texas_precost['Blind/Disabled'].apply(np.round)
texas_precost['Child'] = texas_precost['Child'].apply(np.round)
texas_precost['Telemonitoring'] = texas_precost['Telemonitoring'].apply(np.round)
texas_precost['Other'] = texas_precost['Other'].apply(np.round)
texas_precost = texas_precost.sort_values(by=['treat'])
texas_precost['Child'] = texas_precost['Child'].map('${:,.0f}'.format)
texas_precost['Blind/Disabled'] = texas_precost['Blind/Disabled'].map('${:,.0f}'.format)
texas_precost['Telemonitoring'] = texas_precost['Telemonitoring'].map('${:,.0f}'.format)
texas_precost['Televisits'] = texas_precost['Televisits'].map('${:,.0f}'.format)
texas_precost['Other'] = texas_precost['Other'].map('${:,.0f}'.format)
texas_precost = texas_precost.rename(columns={'Telemonitoring':'Total ','Televisits':'Total'})
texas_precost_tele = texas_precost[texas_precost['treat']==1]
texas_precost_nontele = texas_precost[texas_precost['treat']==0]
texas_precost_tele=texas_precost_tele.drop(['treat','Region'],axis=1)
texas_precost_nontele=texas_precost_nontele.drop(['treat','Region'],axis=1)


texas_postcost = med_df_postcost[med_df_postcost['Region']=='Texas']
texas_postcost=texas_postcost.drop(['type','post','meas'],axis=1)
texas_postcost['Blind/Disabled'] = texas_postcost['Blind/Disabled'].apply(np.round)
texas_postcost['Child'] = texas_postcost['Child'].apply(np.round)
texas_postcost['Telemonitoring'] = texas_postcost['Telemonitoring'].apply(np.round)
texas_postcost['Other'] = texas_postcost['Other'].apply(np.round)
texas_postcost = texas_postcost.sort_values(by=['treat'])
texas_postcost['Child'] = texas_postcost['Child'].map('${:,.0f}'.format)
texas_postcost['Blind/Disabled'] = texas_postcost['Blind/Disabled'].map('${:,.0f}'.format)
texas_postcost['Telemonitoring'] = texas_postcost['Telemonitoring'].map('${:,.0f}'.format) 
texas_postcost['Televisits'] = texas_postcost['Televisits'].map('${:,.0f}'.format)
texas_postcost['Other'] = texas_postcost['Other'].map('${:,.0f}'.format)
texas_postcost = texas_postcost.rename(columns={'Telemonitoring':'Total ','Televisits':'Total'})
texas_postcost_tele = texas_postcost[texas_postcost['treat']==1]
texas_postcost_nontele = texas_postcost[texas_postcost['treat']==0]
texas_postcost_tele=texas_postcost_tele.drop(['treat','Region'],axis=1)
texas_postcost_nontele=texas_postcost_nontele.drop(['treat','Region'],axis=1)

#----------------------------------------------------Inpatient Cost------------------------------------------#
inpat_df = df[df['type']=='inp']

#pre cost
inpat_df_precost = inpat_df[inpat_df['post']==0]
inpat_df_precost = inpat_df_precost[inpat_df_precost['meas']=='cost']
#post cost
inpat_df_postcost = inpat_df[inpat_df['post']==1]
inpat_df_postcost = inpat_df_postcost[inpat_df_postcost['meas']=='cost']

inpat_encount = inpat_df[inpat_df['meas']=='cnt']

texas_postcost_inpat = inpat_df_postcost[inpat_df_postcost['Region']=='Texas']
texas_postcost_inpat = texas_postcost_inpat.drop(['type','post','meas'],axis=1)
texas_postcost_inpat['Blind/Disabled'] = texas_postcost_inpat['Blind/Disabled'].apply(np.round)
texas_postcost_inpat['Child'] = texas_postcost_inpat['Child'].apply(np.round)
texas_postcost_inpat['Telemonitoring'] = texas_postcost_inpat['Telemonitoring'].apply(np.round)
texas_postcost_inpat['Other'] = texas_postcost_inpat['Other'].apply(np.round)
texas_postcost_inpat = texas_postcost_inpat.sort_values(by=['treat'])
texas_postcost_inpat['Child'] = texas_postcost_inpat['Child'].map('${:,.0f}'.format)
texas_postcost_inpat['Blind/Disabled'] = texas_postcost_inpat['Blind/Disabled'].map('${:,.0f}'.format)
texas_postcost_inpat['Telemonitoring'] = texas_postcost_inpat['Telemonitoring'].map('${:,.0f}'.format) 
texas_postcost_inpat['Televisits'] = texas_postcost_inpat['Televisits'].map('${:,.0f}'.format)
texas_postcost_inpat['Other'] = texas_postcost_inpat['Other'].map('${:,.0f}'.format)
texas_postcost_inpat = texas_postcost_inpat.rename(columns={'Telemonitoring':'Total ','Televisits':'Total'})
texas_postcost_tele_inpat = texas_postcost_inpat[texas_postcost_inpat['treat']==1]
texas_postcost_nontele_inpat = texas_postcost_inpat[texas_postcost_inpat['treat']==0]
texas_postcost_tele_inpat=texas_postcost_tele_inpat.drop(['treat','Region'],axis=1)
texas_postcost_nontele_inpat=texas_postcost_nontele_inpat.drop(['treat','Region'],axis=1)

texas_inpat_encount_df = inpat_encount[inpat_encount['Region']=='Texas']
texas_inpat_encount_df = texas_inpat_encount_df.sort_values(by=['treat'])
texas_inpat_encount_df= texas_inpat_encount_df.drop(['type','post','meas'],axis=1)                      
texas_inpat_encount_df['Child'] = texas_inpat_encount_df['Child'].map('{:,.3f}'.format)
texas_inpat_encount_df['Blind/Disabled'] = texas_inpat_encount_df['Blind/Disabled'].map('{:,.3f}'.format)
texas_inpat_encount_df['Telemonitoring'] = texas_inpat_encount_df['Telemonitoring'].map('{:,.3f}'.format)
texas_inpat_encount_df['Televisits'] = texas_inpat_encount_df['Televisits'].map('{:,.3f}'.format)
texas_inpat_encount_df['Other'] = texas_inpat_encount_df['Other'].map('{:,.3f}'.format)        
texas_inpat_encount_df = texas_inpat_encount_df.rename(columns={'Telemonitoring':'Total','Televisits':'Total'})
texas_inpat_encount_tele = texas_inpat_encount_df[texas_inpat_encount_df['treat']==1]
texas_inpat_encount_nontele = texas_inpat_encount_df[texas_inpat_encount_df['treat']==0]
texas_inpat_encount_tele=texas_inpat_encount_tele.drop(['treat','Region'],axis=1)
texas_inpat_encount_nontele=texas_inpat_encount_nontele.drop(['treat','Region'],axis=1)


#----------------------------------------------------ED Cost------------------------------------------#
ed_df = df[df['type']=='ed']

#pre cost
ed_df_precost = ed_df[ed_df['post']==0]
ed_df_precost = ed_df_precost[ed_df_precost['meas']=='cost']
#post cost
ed_df_postcost = ed_df[ed_df['post']==1]
ed_df_postcost = ed_df_postcost[ed_df_postcost['meas']=='cost']

ed_visits = ed_df[ed_df['meas']=='cnt']


texas_postcost_ed = ed_df_postcost[ed_df_postcost['Region']=='Texas']
texas_postcost_ed = texas_postcost_ed.drop(['type','post','meas'],axis=1)
texas_postcost_ed['Blind/Disabled'] = texas_postcost_ed['Blind/Disabled'].apply(np.round)
texas_postcost_ed['Child'] = texas_postcost_ed['Child'].apply(np.round)
texas_postcost_ed['Telemonitoring'] = texas_postcost_ed['Telemonitoring'].apply(np.round)
texas_postcost_ed['Other'] = texas_postcost_ed['Other'].apply(np.round)
texas_postcost_ed = texas_postcost_ed.sort_values(by=['treat'])
texas_postcost_ed['Child'] = texas_postcost_ed['Child'].map('${:,.0f}'.format)
texas_postcost_ed['Blind/Disabled'] = texas_postcost_ed['Blind/Disabled'].map('${:,.0f}'.format)
texas_postcost_ed['Telemonitoring'] = texas_postcost_ed['Telemonitoring'].map('${:,.0f}'.format) 
texas_postcost_ed['Televisits'] = texas_postcost_ed['Televisits'].map('${:,.0f}'.format)
texas_postcost_ed['Other'] = texas_postcost_ed['Other'].map('${:,.0f}'.format)
texas_postcost_ed = texas_postcost_ed.rename(columns={'Telemonitoring':'Total ','Televisits':'Total'})
texas_postcost_tele_ed = texas_postcost_ed[texas_postcost_ed['treat']==1]
texas_postcost_nontele_ed = texas_postcost_ed[texas_postcost_ed['treat']==0]
texas_postcost_tele_ed=texas_postcost_tele_ed.drop(['treat','Region'],axis=1)
texas_postcost_nontele_ed=texas_postcost_nontele_ed.drop(['treat','Region'],axis=1)

texas_ed_visits_df = ed_visits[ed_visits['Region']=='Texas']
texas_ed_visits_df = texas_ed_visits_df.sort_values(by=['treat'])
texas_ed_visits_df= texas_ed_visits_df.drop(['type','post','meas'],axis=1)                      
texas_ed_visits_df['Child'] = texas_ed_visits_df['Child'].map('{:,.3f}'.format)
texas_ed_visits_df['Blind/Disabled'] = texas_ed_visits_df['Blind/Disabled'].map('{:,.3f}'.format)
texas_ed_visits_df['Telemonitoring'] = texas_ed_visits_df['Telemonitoring'].map('{:,.3f}'.format)
texas_ed_visits_df['Televisits'] = texas_ed_visits_df['Televisits'].map('{:,.3f}'.format)
texas_ed_visits_df['Other'] = texas_ed_visits_df['Other'].map('{:,.3f}'.format)        
texas_ed_visits_df = texas_ed_visits_df.rename(columns={'Telemonitoring':'Total','Televisits':'Total'})
texas_ed_visits_tele = texas_ed_visits_df[texas_ed_visits_df['treat']==1]
texas_ed_visits_nontele = texas_ed_visits_df[texas_ed_visits_df['treat']==0]
texas_ed_visits_tele=texas_ed_visits_tele.drop(['treat','Region'],axis=1)
texas_ed_visits_nontele=texas_ed_visits_nontele.drop(['treat','Region'],axis=1)

#----------------------------------------------------Outpatient Cost------------------------------------------#
outpat_df = df[df['type']=='out']

#pre cost
outpat_df_precost = outpat_df[outpat_df['post']==0]
outpat_df_precost = outpat_df_precost[outpat_df_precost['meas']=='cost']
#post cost
outpat_df_postcost = outpat_df[outpat_df['post']==1]
outpat_df_postcost = outpat_df_postcost[outpat_df_postcost['meas']=='cost']
outpat_visits = outpat_df[outpat_df['meas']=='cnt']


texas_postcost_outpat = outpat_df_postcost[outpat_df_postcost['Region']=='Texas']
texas_postcost_outpat = texas_postcost_outpat.drop(['type','post','meas'],axis=1)
texas_postcost_outpat['Blind/Disabled'] = texas_postcost_outpat['Blind/Disabled'].apply(np.round)
texas_postcost_outpat['Child'] = texas_postcost_outpat['Child'].apply(np.round)
texas_postcost_outpat['Telemonitoring'] = texas_postcost_outpat['Telemonitoring'].apply(np.round)
texas_postcost_outpat['Other'] = texas_postcost_outpat['Other'].apply(np.round)
texas_postcost_outpat = texas_postcost_outpat.sort_values(by=['treat'])
texas_postcost_outpat['Child'] = texas_postcost_outpat['Child'].map('${:,.0f}'.format)
texas_postcost_outpat['Blind/Disabled'] = texas_postcost_outpat['Blind/Disabled'].map('${:,.0f}'.format)
texas_postcost_outpat['Telemonitoring'] = texas_postcost_outpat['Telemonitoring'].map('${:,.0f}'.format) 
texas_postcost_outpat['Televisits'] = texas_postcost_outpat['Televisits'].map('${:,.0f}'.format)
texas_postcost_outpat['Other'] = texas_postcost_outpat['Other'].map('${:,.0f}'.format)
texas_postcost_outpat = texas_postcost_outpat.rename(columns={'Telemonitoring':'Total ','Televisits':'Total'})
texas_postcost_tele_outpat = texas_postcost_outpat[texas_postcost_outpat['treat']==1]
texas_postcost_nontele_outpat = texas_postcost_outpat[texas_postcost_outpat['treat']==0]
texas_postcost_tele_outpat=texas_postcost_tele_outpat.drop(['treat','Region'],axis=1)
texas_postcost_nontele_outpat=texas_postcost_nontele_outpat.drop(['treat','Region'],axis=1)

texas_outpat_visits_df = outpat_visits[outpat_visits['Region']=='Texas']
texas_outpat_visits_df = texas_outpat_visits_df.sort_values(by=['treat'])
texas_outpat_visits_df= texas_outpat_visits_df.drop(['type','post','meas'],axis=1)                      
texas_outpat_visits_df['Child'] = texas_outpat_visits_df['Child'].map('{:,.3f}'.format)
texas_outpat_visits_df['Blind/Disabled'] = texas_outpat_visits_df['Blind/Disabled'].map('{:,.3f}'.format)
texas_outpat_visits_df['Telemonitoring'] = texas_outpat_visits_df['Telemonitoring'].map('{:,.3f}'.format)
texas_outpat_visits_df['Televisits'] = texas_outpat_visits_df['Televisits'].map('{:,.3f}'.format)
texas_outpat_visits_df['Other'] = texas_outpat_visits_df['Other'].map('{:,.3f}'.format)        
texas_outpat_visits_df = texas_outpat_visits_df.rename(columns={'Telemonitoring':'Total','Televisits':'Total'})
texas_outpat_visits_tele = texas_outpat_visits_df[texas_outpat_visits_df['treat']==1]
texas_outpat_visits_nontele = texas_outpat_visits_df[texas_outpat_visits_df['treat']==0]
texas_outpat_visits_tele=texas_outpat_visits_tele.drop(['treat','Region'],axis=1)
texas_outpat_visits_nontele=texas_outpat_visits_nontele.drop(['treat','Region'],axis=1)

treatment_cost = []
@app.route('/', methods=["GET","POST"])
@app.route('/home', methods=["GET","POST"])
def index():
    
    if request.method == 'POST':
        treatment_cost.append(request.form['treat_cost'])
        

    return render_template('index.html',treatment_cost=treatment_cost)
    

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
        num_client['Other'] = num_client['Other'].map('{:,.0f}'.format)
        num_client = num_client.rename(columns={'Telemonitoring':'Total ','Televisits':'Total'})
        numclient_tele = num_client[num_client['treat']==1]
        numclient_nontele = num_client[num_client['treat']==0]
        numclient_tele=numclient_tele.drop(['treat','Region'],axis=1)
        numclient_nontele=numclient_nontele.drop(['treat','Region'],axis=1)

        df_precost = med_df_precost[med_df_precost['Region']==sda_name]
        df_precost = df_precost.sort_values(by=['treat'])
        df_precost=df_precost.drop(['type','post','meas'],axis=1)
        df_precost['Blind/Disabled'] = df_precost['Blind/Disabled'].apply(np.round)
        df_precost['Child'] = df_precost['Child'].apply(np.round)
        df_precost['Telemonitoring'] = df_precost['Telemonitoring'].apply(np.round)
        df_precost['Other'] = df_precost['Other'].apply(np.round)
        df_precost['Child'] = df_precost['Child'].map('${:,.0f}'.format)
        df_precost['Blind/Disabled'] = df_precost['Blind/Disabled'].map('${:,.0f}'.format)
        df_precost['Telemonitoring'] = df_precost['Telemonitoring'].map('${:,.0f}'.format)
        df_precost['Televisits'] = df_precost['Televisits'].map('${:,.0f}'.format)
        df_precost['Other'] = df_precost['Other'].map('${:,.0f}'.format)
        df_precost = df_precost.rename(columns={'Telemonitoring':'Total','Televisits':'Total'})
        precost_tele = df_precost[df_precost['treat']==1]
        precost_nontele = df_precost[df_precost['treat']==0]
        precost_tele=precost_tele.drop(['treat','Region'],axis=1)
        precost_nontele=precost_nontele.drop(['treat','Region'],axis=1)

        df_postcost = med_df_postcost[med_df_postcost['Region']==sda_name]
        df_postcost = df_postcost.sort_values(by=['treat'])
        df_postcost=df_postcost.drop(['type','post','meas'],axis=1)
        df_postcost['Blind/Disabled'] = df_postcost['Blind/Disabled'].apply(np.round)
        df_postcost['Child'] = df_postcost['Child'].apply(np.round)  
        df_postcost['Telemonitoring'] = df_postcost['Telemonitoring'].apply(np.round)   
        df_postcost['Other'] = df_postcost['Other'].apply(np.round)   
        df_postcost['Child'] = df_postcost['Child'].map('${:,.0f}'.format)
        df_postcost['Blind/Disabled'] = df_postcost['Blind/Disabled'].map('${:,.0f}'.format)
        df_postcost['Telemonitoring'] = df_postcost['Telemonitoring'].map('${:,.0f}'.format)     
        df_postcost['Televisits'] = df_postcost['Televisits'].map('${:,.0f}'.format)
        df_postcost['Other'] = df_postcost['Other'].map('${:,.0f}'.format)
        df_postcost = df_postcost.rename(columns={'Telemonitoring':'Total ','Televisits':'Total'})
        postcost_tele = df_postcost[df_postcost['treat']==1]
        postcost_nontele = df_postcost[df_postcost['treat']==0]
        postcost_tele=postcost_tele.drop(['treat','Region'],axis=1)
        postcost_nontele=postcost_nontele.drop(['treat','Region'],axis=1)

        if sda_name != None:
            return render_template("medcost.html", sda_name=sda_name, sda=sda, numclient_tele=[numclient_tele.to_html(index = False)],numclient_nontele=[numclient_nontele.to_html(index = False)],
                                    precost_tele=[precost_tele.to_html(index = False)], precost_nontele=[precost_nontele.to_html(index = False)],postcost_tele=[postcost_tele.to_html(index = False)], postcost_nontele=[postcost_nontele.to_html(index = False)])
    
    return render_template('medcost1.html',sda=sda, texas_nclient_tele=[texas_nclient_tele.to_html(index=False)], texas_nclient_nontele=[texas_nclient_nontele.to_html(index=False)], texas_precost_tele=[texas_precost_tele.to_html(index=False)], 
                            texas_precost_nontele=[texas_precost_nontele.to_html(index=False)], texas_postcost_tele=[texas_postcost_tele.to_html(index = False)],  texas_postcost_nontele=[texas_postcost_nontele.to_html(index = False)])
    
    
@app.route('/inpatcost', methods=["GET", "POST"])
def inpatcost():
    if request.method == "POST":
        sda_name = request.form.get("sda", None)
        num_client = nclients[nclients['Region']==sda_name]
        num_client = num_client.sort_values(by=['treat'])
        num_client=num_client.drop(['type','post','meas'],axis=1)
        num_client['Child'] = num_client['Child'].map('{:,.0f}'.format)
        num_client['Blind/Disabled'] = num_client['Blind/Disabled'].map('{:,.0f}'.format)
        num_client['Telemonitoring'] = num_client['Telemonitoring'].map('{:,.0f}'.format)
        num_client['Televisits'] = num_client['Televisits'].map('{:,.0f}'.format)
        num_client['Other'] = num_client['Other'].map('{:,.0f}'.format)
        num_client = num_client.rename(columns={'Telemonitoring':'Total ','Televisits':'Total'})
        numclient_tele = num_client[num_client['treat']==1]
        numclient_nontele = num_client[num_client['treat']==0]
        numclient_tele=numclient_tele.drop(['treat','Region'],axis=1)
        numclient_nontele=numclient_nontele.drop(['treat','Region'],axis=1)

        postcost_inpat = inpat_df_postcost[inpat_df_postcost['Region']==sda_name]
        postcost_inpat = postcost_inpat.sort_values(by=['treat'])
        postcost_inpat=postcost_inpat.drop(['type','post','meas'],axis=1)
        postcost_inpat['Blind/Disabled'] = postcost_inpat['Blind/Disabled'].apply(np.round)
        postcost_inpat['Child'] = postcost_inpat['Child'].apply(np.round)
        postcost_inpat['Telemonitoring'] = postcost_inpat['Telemonitoring'].apply(np.round)
        postcost_inpat['Other'] = postcost_inpat['Other'].apply(np.round)
        postcost_inpat['Child'] = postcost_inpat['Child'].map('${:,.0f}'.format)
        postcost_inpat['Blind/Disabled'] = postcost_inpat['Blind/Disabled'].map('${:,.0f}'.format)
        postcost_inpat['Telemonitoring'] = postcost_inpat['Telemonitoring'].map('${:,.0f}'.format)
        postcost_inpat['Televisits'] = postcost_inpat['Televisits'].map('${:,.0f}'.format)
        postcost_inpat['Other'] = postcost_inpat['Other'].map('${:,.0f}'.format)
        postcost_inpat = postcost_inpat.rename(columns={'Telemonitoring':'Total','Televisits':'Total'})
        postcost_tele_inpat = postcost_inpat[postcost_inpat['treat']==1]
        postcost_nontele_inpat = postcost_inpat[postcost_inpat['treat']==0]
        postcost_tele_inpat=postcost_tele_inpat.drop(['treat','Region'],axis=1)
        postcost_nontele_inpat=postcost_nontele_inpat.drop(['treat','Region'],axis=1)

        inpat_encount_df = inpat_encount[inpat_encount['Region']==sda_name]
        inpat_encount_df = inpat_encount_df.sort_values(by=['treat'])
        inpat_encount_df=inpat_encount_df.drop(['type','post','meas'],axis=1)                      
        inpat_encount_df['Child'] = inpat_encount_df['Child'].map('{:,.3f}'.format)
        inpat_encount_df['Blind/Disabled'] = inpat_encount_df['Blind/Disabled'].map('{:,.3f}'.format)
        inpat_encount_df['Telemonitoring'] = inpat_encount_df['Telemonitoring'].map('{:,.3f}'.format)
        inpat_encount_df['Televisits'] = inpat_encount_df['Televisits'].map('{:,.3f}'.format)
        inpat_encount_df['Other'] = inpat_encount_df['Other'].map('{:,.3f}'.format)        
        inpat_encount_df = inpat_encount_df.rename(columns={'Telemonitoring':'Total','Televisits':'Total'})
        inpat_encount_tele = inpat_encount_df[inpat_encount_df['treat']==1]
        inpat_encount_nontele = inpat_encount_df[inpat_encount_df['treat']==0]
        inpat_encount_tele=inpat_encount_tele.drop(['treat','Region'],axis=1)
        inpat_encount_nontele=inpat_encount_nontele.drop(['treat','Region'],axis=1)

    
        if sda_name != None:
            return render_template("inpatient.html", sda_name=sda_name, sda=sda, numclient_tele=[numclient_tele.to_html(index = False)],numclient_nontele=[numclient_nontele.to_html(index = False)],
                                    postcost_tele_inpat=[postcost_tele_inpat.to_html(index = False)], postcost_nontele_inpat=[postcost_nontele_inpat.to_html(index = False)], inpat_encount_tele=[inpat_encount_tele.to_html(index = False)],inpat_encount_nontele=[inpat_encount_nontele.to_html(index = False)])
    
    
    
    return render_template('inpatient1.html',sda=sda, texas_nclient_tele=[texas_nclient_tele.to_html(index=False)], texas_nclient_nontele=[texas_nclient_nontele.to_html(index=False)], texas_postcost_tele_inpat=[texas_postcost_tele_inpat.to_html(index = False)],  texas_postcost_nontele_inpat=[texas_postcost_nontele_inpat.to_html(index = False)],
                            texas_inpat_encount_tele=[texas_inpat_encount_tele.to_html(index=False)],texas_inpat_encount_nontele=[texas_inpat_encount_nontele.to_html(index=False)])


@app.route('/edcost', methods=["GET", "POST"])
def edcost():
    if request.method == "POST":
        sda_name = request.form.get("sda", None)
        num_client = nclients[nclients['Region']==sda_name]
        num_client = num_client.sort_values(by=['treat'])
        num_client=num_client.drop(['type','post','meas'],axis=1)
        num_client['Child'] = num_client['Child'].map('{:,.0f}'.format)
        num_client['Blind/Disabled'] = num_client['Blind/Disabled'].map('{:,.0f}'.format)
        num_client['Telemonitoring'] = num_client['Telemonitoring'].map('{:,.0f}'.format)
        num_client['Televisits'] = num_client['Televisits'].map('{:,.0f}'.format)
        num_client['Other'] = num_client['Other'].map('{:,.0f}'.format)
        num_client = num_client.rename(columns={'Telemonitoring':'Total ','Televisits':'Total'})
        numclient_tele = num_client[num_client['treat']==1]
        numclient_nontele = num_client[num_client['treat']==0]
        numclient_tele=numclient_tele.drop(['treat','Region'],axis=1)
        numclient_nontele=numclient_nontele.drop(['treat','Region'],axis=1)

        postcost_ed = ed_df_postcost[ed_df_postcost['Region']==sda_name]
        postcost_ed = postcost_ed.sort_values(by=['treat'])
        postcost_ed=postcost_ed.drop(['type','post','meas'],axis=1)
        postcost_ed['Blind/Disabled'] = postcost_ed['Blind/Disabled'].apply(np.round)
        postcost_ed['Child'] = postcost_ed['Child'].apply(np.round)
        postcost_ed['Telemonitoring'] = postcost_ed['Telemonitoring'].apply(np.round)
        postcost_ed['Other'] = postcost_ed['Other'].apply(np.round)
        postcost_ed['Child'] = postcost_ed['Child'].map('${:,.0f}'.format)
        postcost_ed['Blind/Disabled'] = postcost_ed['Blind/Disabled'].map('${:,.0f}'.format)
        postcost_ed['Telemonitoring'] = postcost_ed['Telemonitoring'].map('${:,.0f}'.format)
        postcost_ed['Televisits'] = postcost_ed['Televisits'].map('${:,.0f}'.format)
        postcost_ed['Other'] = postcost_ed['Other'].map('${:,.0f}'.format)
        postcost_ed = postcost_ed.rename(columns={'Telemonitoring':'Total','Televisits':'Total'})
        postcost_tele_ed = postcost_ed[postcost_ed['treat']==1]
        postcost_nontele_ed = postcost_ed[postcost_ed['treat']==0]
        postcost_tele_ed=postcost_tele_ed.drop(['treat','Region'],axis=1)
        postcost_nontele_ed=postcost_nontele_ed.drop(['treat','Region'],axis=1)

        ed_visits_df = ed_visits[ed_visits['Region']==sda_name]
        ed_visits_df = ed_visits_df.sort_values(by=['treat'])
        ed_visits_df=ed_visits_df.drop(['type','post','meas'],axis=1)                      
        ed_visits_df['Child'] = ed_visits_df['Child'].map('{:,.3f}'.format)
        ed_visits_df['Blind/Disabled'] = ed_visits_df['Blind/Disabled'].map('{:,.3f}'.format)
        ed_visits_df['Telemonitoring'] = ed_visits_df['Telemonitoring'].map('{:,.3f}'.format)
        ed_visits_df['Televisits'] = ed_visits_df['Televisits'].map('{:,.3f}'.format)
        ed_visits_df['Other'] = ed_visits_df['Other'].map('{:,.3f}'.format)        
        ed_visits_df = ed_visits_df.rename(columns={'Telemonitoring':'Total','Televisits':'Total'})
        ed_visits_tele = ed_visits_df[ed_visits_df['treat']==1]
        ed_visits_nontele = ed_visits_df[ed_visits_df['treat']==0]
        ed_visits_tele=ed_visits_tele.drop(['treat','Region'],axis=1)
        ed_visits_nontele=ed_visits_nontele.drop(['treat','Region'],axis=1)

    
        if sda_name != None:
            return render_template("edcost.html", sda_name=sda_name, sda=sda, numclient_tele=[numclient_tele.to_html(index = False)],numclient_nontele=[numclient_nontele.to_html(index = False)],
                                    postcost_tele_ed=[postcost_tele_ed.to_html(index = False)], postcost_nontele_ed=[postcost_nontele_ed.to_html(index = False)], ed_visits_tele=[ed_visits_tele.to_html(index = False)],ed_visits_nontele=[ed_visits_nontele.to_html(index = False)])
    
    return render_template('edcost1.html',sda=sda, texas_nclient_tele=[texas_nclient_tele.to_html(index=False)], texas_nclient_nontele=[texas_nclient_nontele.to_html(index=False)], texas_postcost_tele_ed=[texas_postcost_tele_ed.to_html(index = False)],  texas_postcost_nontele_ed=[texas_postcost_nontele_ed.to_html(index = False)],
                            texas_ed_visits_tele=[texas_ed_visits_tele.to_html(index=False)],texas_ed_visits_nontele=[texas_ed_visits_nontele.to_html(index=False)])


@app.route('/outpatcost', methods=["GET", "POST"])
def outpatcost():
    if request.method == "POST":
        sda_name = request.form.get("sda", None)
        num_client = nclients[nclients['Region']==sda_name]
        num_client = num_client.sort_values(by=['treat'])
        num_client=num_client.drop(['type','post','meas'],axis=1)
        num_client['Child'] = num_client['Child'].map('{:,.0f}'.format)
        num_client['Blind/Disabled'] = num_client['Blind/Disabled'].map('{:,.0f}'.format)
        num_client['Telemonitoring'] = num_client['Telemonitoring'].map('{:,.0f}'.format)
        num_client['Televisits'] = num_client['Televisits'].map('{:,.0f}'.format)
        num_client['Other'] = num_client['Other'].map('{:,.0f}'.format)
        num_client = num_client.rename(columns={'Telemonitoring':'Total ','Televisits':'Total'})
        numclient_tele = num_client[num_client['treat']==1]
        numclient_nontele = num_client[num_client['treat']==0]
        numclient_tele=numclient_tele.drop(['treat','Region'],axis=1)
        numclient_nontele=numclient_nontele.drop(['treat','Region'],axis=1)

        postcost_outpat = outpat_df_postcost[outpat_df_postcost['Region']==sda_name]
        postcost_outpat = postcost_outpat.sort_values(by=['treat'])
        postcost_outpat=postcost_outpat.drop(['type','post','meas'],axis=1)
        postcost_outpat['Blind/Disabled'] = postcost_outpat['Blind/Disabled'].apply(np.round)
        postcost_outpat['Child'] = postcost_outpat['Child'].apply(np.round)
        postcost_outpat['Telemonitoring'] = postcost_outpat['Telemonitoring'].apply(np.round)
        postcost_outpat['Other'] = postcost_outpat['Other'].apply(np.round)
        postcost_outpat['Child'] = postcost_outpat['Child'].map('${:,.0f}'.format)
        postcost_outpat['Blind/Disabled'] = postcost_outpat['Blind/Disabled'].map('${:,.0f}'.format)
        postcost_outpat['Telemonitoring'] = postcost_outpat['Telemonitoring'].map('${:,.0f}'.format)
        postcost_outpat['Televisits'] = postcost_outpat['Televisits'].map('${:,.0f}'.format)
        postcost_outpat['Other'] = postcost_outpat['Other'].map('${:,.0f}'.format)
        postcost_outpat = postcost_outpat.rename(columns={'Telemonitoring':'Total','Televisits':'Total'})
        postcost_tele_outpat = postcost_outpat[postcost_outpat['treat']==1]
        postcost_nontele_outpat = postcost_outpat[postcost_outpat['treat']==0]
        postcost_tele_outpat=postcost_tele_outpat.drop(['treat','Region'],axis=1)
        postcost_nontele_outpat=postcost_nontele_outpat.drop(['treat','Region'],axis=1)


        outpat_visits_df = outpat_visits[outpat_visits['Region']==sda_name]
        outpat_visits_df = outpat_visits_df.sort_values(by=['treat'])
        outpat_visits_df=outpat_visits_df.drop(['type','post','meas'],axis=1)                      
        outpat_visits_df['Child'] = outpat_visits_df['Child'].map('{:,.3f}'.format)
        outpat_visits_df['Blind/Disabled'] = outpat_visits_df['Blind/Disabled'].map('{:,.3f}'.format)
        outpat_visits_df['Telemonitoring'] = outpat_visits_df['Telemonitoring'].map('{:,.3f}'.format)
        outpat_visits_df['Televisits'] = outpat_visits_df['Televisits'].map('{:,.3f}'.format)
        outpat_visits_df['Other'] = outpat_visits_df['Other'].map('{:,.3f}'.format)        
        outpat_visits_df = outpat_visits_df.rename(columns={'Telemonitoring':'Total','Televisits':'Total'})
        outpat_visits_tele = outpat_visits_df[outpat_visits_df['treat']==1]
        outpat_visits_nontele = outpat_visits_df[outpat_visits_df['treat']==0]
        outpat_visits_tele=outpat_visits_tele.drop(['treat','Region'],axis=1)
        outpat_visits_nontele=outpat_visits_nontele.drop(['treat','Region'],axis=1)



    
        if sda_name != None:
            return render_template("outpatient.html", sda_name=sda_name, sda=sda, numclient_tele=[numclient_tele.to_html(index = False)],numclient_nontele=[numclient_nontele.to_html(index = False)],
                                    postcost_tele_outpat=[postcost_tele_outpat.to_html(index = False)], postcost_nontele_outpat=[postcost_nontele_outpat.to_html(index = False)], outpat_visits_tele=[outpat_visits_tele.to_html(index = False)],outpat_visits_nontele=[outpat_visits_nontele.to_html(index = False)])
    
    return render_template('outpatient1.html',sda=sda, texas_nclient_tele=[texas_nclient_tele.to_html(index=False)], texas_nclient_nontele=[texas_nclient_nontele.to_html(index=False)], texas_postcost_tele_outpat=[texas_postcost_tele_outpat.to_html(index = False)],  texas_postcost_nontele_outpat=[texas_postcost_nontele_outpat.to_html(index = False)],
                            texas_outpat_visits_tele=[texas_outpat_visits_tele.to_html(index=False)],texas_outpat_visits_nontele=[texas_outpat_visits_nontele.to_html(index=False)])







@app.route('/documents', methods = ["GET","POST"])
def documents(): 
    return render_template('documents.html')

if __name__ == "__main__":
    app.run(debug=True) 