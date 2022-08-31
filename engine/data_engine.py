import pandas as pd
import numpy as np
import plotly.express as px
import datetime as dt
from dateutil.relativedelta import relativedelta

from engine.dic.dic import *

def create_df(path, dic = None):
    data = pd.read_csv(path, header=0, sep = ';')
    if dic :
        data.rename(columns = dic, inplace = True)
    return data

def sel_annee(aaaa_mm):
    return aaaa_mm[:4]

data_TGV_reg = create_df("engine/data/SNCF/regularite-mensuelle-tgv-aqst.csv", dic = dic_TGV_reg)
data_TGV_reg['annee'] = data_TGV_reg.date.apply(lambda x : sel_annee(x))

data_TGV_eco = create_df("engine/data/SNCF/emission-co2-tgv.csv", dic = dic_TGV_eco)
data_TGV_eco.sort_values('trajet_liaison', inplace = True)

data_trajet_histo = create_df("engine/data/SNCF/meilleurs-temps-des-parcours-des-trains.csv", dic = dic_trajet_histo)
data_trajet_histo.sort_values(['annee', 'trajet'], inplace = True)

def selection_data(sel):
    if sel == "Paris - Lyon":
        gares = ('PARIS LYON', 'LYON PART DIEU') 
        trajet_liaison = 'Paris - Lyon Part Dieu'
        trajet = "PARIS - LYON"
    if sel == 'Paris - Bordeaux':
        gares = ('PARIS MONTPARNASSE', 'BORDEAUX ST JEAN') 
        trajet_liaison = 'Paris - Bordeaux'
        trajet = 'PARIS - BORDEAUX'
    if sel == "Lyon - Lille":
        gares = ('LYON PART DIEU', 'LILLE') 
        trajet_liaison = 'Lille Europe - Lyon Part Dieu'
        trajet = 'LYON - LILLE'
    if sel == 'Paris - Angers':
        gares = ('PARIS MONTPARNASSE', 'ANGERS SAINT LAUD') 
        trajet_liaison = 'Paris - Anger St Laud'
        trajet = 'PARIS - ANGERS'
    if sel == 'Paris - Arras':
        gares = ('PARIS NORD', 'ARRAS') 
        trajet_liaison = 'Paris - Arras'
        trajet = 'PARIS - ARRAS'
    if sel == 'Paris - Brest':
        gares = ('PARIS MONTPARNASSE', 'BREST') 
        trajet_liaison = 'Paris - Arras'
        trajet = 'PARIS - BREST'
    if sel == 'Paris - Dijon':
        gares = ('PARIS LYON', 'DIJON VILLE') 
        trajet_liaison = 'Paris - Dijon'
        trajet = 'PARIS - DIJON'
    if sel == 'Paris - Grenoble':
        gares = ('PARIS LYON', 'GRENOBLE') 
        trajet_liaison = 'Paris - Grenoble'
        trajet = 'PARIS - GRENOBLE'
    if sel == 'Paris - La Rochelle':
        gares = ('PARIS MONTPARNASSE', 'LA ROCHELLE VILLE') 
        trajet_liaison = 'Paris - La Rochelle'
        trajet = 'PARIS - LA ROCHELLE'
        
    data_TGV_eco_sel = data_TGV_eco[data_TGV_eco.trajet_liaison == trajet_liaison].copy()
    data_trajet_histo_sel = data_trajet_histo[data_trajet_histo.trajet == trajet].copy()
    data_TGV_reg_sel = data_TGV_reg.query("gare_dep == "+ "'" + gares[0] + "'" + "& gare_arr == " + "'" + gares[1] + "'").copy()
    data_TGV_reg_sel_inv = data_TGV_reg.query("gare_dep == "+ "'" + gares[1] + "'" + "& gare_arr == " + "'" + gares[0] + "'").copy()
    return data_TGV_eco_sel, data_trajet_histo_sel, data_TGV_reg_sel, data_TGV_reg_sel_inv

#########################################################################################

def exploitation_data_caracteristique(data_TGV_eco_sel, data_trajet_histo_sel):
    temps = int(data_trajet_histo_sel.est_temps_min.values[-1])
    distance = data_TGV_eco_sel.distance.values[0]
    temps_h = temps / 60
    vitesse = round(distance / temps_h, 2)
    emission = round(data_TGV_eco_sel.empreinte.values[0], 3)
    data_trajet_histo_sel["vitesse"] = distance * 60 / data_trajet_histo_sel.est_temps_min
    return data_trajet_histo_sel, temps, distance, vitesse, emission

def graph_data_caractéristique(data_trajet_histo_sel, choice):
    if choice == "Temps":
        y = "est_temps_min"
        y_lab = "Temps (min)"
    if choice == "Vitesse" :
        y = "vitesse"
        y_lab = "Vitesse (km/h)"
    fig = px.line(data_trajet_histo_sel,
              x="annee",
              y=y,
              labels={"annee":'Années', y:y_lab},
              template = "ggplot2"
             )
    return fig

#########################################################################################

def prct_nb(data, prc, nb):
    data[prc] = (data[prc] * data[nb] / 100).astype('int64')
    return data

def create_df_prct(data_TGV_reg_sel, aaaa, L_prct = L_prct):
    data_TGV_reg_sel_prct = data_TGV_reg_sel.query('annee == ' + '"' + aaaa + '"').copy()
    data_TGV_reg_sel_prct = data_TGV_reg_sel_prct[['nb_train'] + L_prct].copy()
    for prct in L_prct :
        data_TGV_reg_sel_prct = prct_nb(data_TGV_reg_sel_prct, prct, 'nb_train')
    data_TGV_reg_sel_prct = data_TGV_reg_sel_prct[L_prct].copy()
    L_num= []
    for prct in L_prct:
        new_prct = data_TGV_reg_sel_prct[prct].sum()
        L_num.append(new_prct)
    L_cause = ['Cause externe', 'Cause infrastructure', 'Cause gestion trafic', 'Cause matériel roulant', 'Cause gestion gare & réutilisation matériel', 'Cause voyageurs']
    data_TGV_reg_sel_prct = pd.DataFrame(list(zip(L_cause,L_num)), columns = ['Cause','Nb'])
    return data_TGV_reg_sel_prct

def graph_pie_retard(data_TGV_reg_sel, aaaa):
    data_TGV_reg_sel_prct = create_df_prct(data_TGV_reg_sel, aaaa)
    fig = px.pie(data_TGV_reg_sel_prct, values='Nb', names = 'Cause', color_discrete_sequence=px.colors.qualitative.Pastel1,
              template = "ggplot2")
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(showlegend=False)
    return fig

def create_df_nb_retard(data_TGV_reg_sel, aaaa, L_retard = L_retard): #= aaaa
    data_TGV_reg_sel_nb_retard = data_TGV_reg_sel.query('annee == ' + '"' + aaaa + '"')[['nb_train'] + L_retard].copy()
    return data_TGV_reg_sel_nb_retard

def graph_bar_retard(data_TGV_reg_sel, aaaa, choice):
    data_TGV_reg_sel_nb_retard = create_df_nb_retard(data_TGV_reg_sel, aaaa)
    data_TGV_reg_sel_nb_retard.rename(columns = {"nb_train_annule" : "Trains annulés",
                          "nb_train_retard_arr" : "Trains en retard",
                          "nb_train_retard_min_15" : "Trains en retard d'au moins 15 minutes",
                          "nb_train_retard_min_30" : "Trains en retard d'au moins 30 minutes",
                          "nb_train_retard_min_60" : "Trains en retard d'au moins 1 heure"}, inplace = True)
    x = data_TGV_reg_sel_nb_retard.sum(axis = 0).index[1:]
    if choice == "Pourcentage":
        y = 100 * data_TGV_reg_sel_nb_retard.sum(axis = 0).values[1:]/data_TGV_reg_sel_nb_retard.sum(axis = 0).values[0]
        y_lab = "Pourcentage de train"
    if choice == "Nombre":
        y = data_TGV_reg_sel_nb_retard.sum(axis = 0).values[1:]
        y_lab = "Nombre de train"
    fig = px.bar(x=x,
                 y=y,
                template = "ggplot2",
                 labels = {"x" : "Catégorie du retard",
                          "y" : y_lab
                         },
                 color_discrete_sequence=px.colors.qualitative.Pastel1
                )
    return fig

def create_df_stat_retard(data_TGV_reg_sel, temps, aaaa, L_retard = L_retard): #= aaaa
    data_TGV_reg_sel_stat_retard = data_TGV_reg_sel.copy()
    data_TGV_reg_sel_stat_retard['nb_min_retard'] = data_TGV_reg_sel_stat_retard.retard_train_arr_moy * (data_TGV_reg_sel_stat_retard.nb_train)
    data_TGV_reg_sel_stat_retard = data_TGV_reg_sel_stat_retard[['annee', 'nb_min_retard', 'nb_train']].groupby('annee').sum()
    data_TGV_reg_sel_stat_retard.nb_min_retard = data_TGV_reg_sel_stat_retard.nb_min_retard / data_TGV_reg_sel_stat_retard.nb_train
    data_TGV_reg_sel_stat_retard['prct_retard'] = data_TGV_reg_sel_stat_retard.nb_min_retard * 100 / temps
    return data_TGV_reg_sel_stat_retard

def nb_jours(d):
    d= d.replace('-', ' ')
    d = dt.datetime.strptime(d, '%Y %m') + relativedelta(months=1)
    d = int(d.strftime('%j'))
    return d - 1

def exploitation_data_retard(data_TGV_reg_sel, temps, aaaa) :
    nb_train = create_df_nb_retard(data_TGV_reg_sel, aaaa, L_retard = L_retard).nb_train.sum()
    nb_jour = nb_jours(data_TGV_reg_sel.date.max())
    data_TGV_reg_sel_stat_retard = create_df_stat_retard(data_TGV_reg_sel, temps, aaaa, L_retard = L_retard)
    retard_moy = data_TGV_reg_sel_stat_retard.nb_min_retard.values[-1]
    retard_moy_n1 = data_TGV_reg_sel_stat_retard.nb_min_retard.values[-2]
    evol_retard_moy = 100 * (retard_moy - retard_moy_n1) / retard_moy_n1
    prct_retard = 100 * retard_moy / temps
    return round(retard_moy,1), round(evol_retard_moy,1) , round(prct_retard,1), nb_train, round(nb_train/nb_jour, 1)

def dest(L_AR, dire):
    if dire :
        nom_traj = L_AR[1] + " - " + L_AR[0]
    else :
        nom_traj = L_AR[0] + " - " + L_AR[1]        
    return nom_traj

def desc(L_AR, nb_train, nb_train_j, dire, aaaa):
    if dire :
        descr = "Il y a **" + str(nb_train) + " TGV** de " + L_AR[1] + " vers " + L_AR[0] + "en " + aaaa + ". Soit " + str(nb_train_j) + " trains/jour."
    else :
        descr = "Il y a **" + str(nb_train) + " TGV** de " + L_AR[0] + " vers " + L_AR[1] + "en " + aaaa + ". Soit " + str(nb_train_j) + " trains/jour."
    return descr

def gen_L_AR(sel):
    L_AR = sel.split("-")
    L_AR[0] = L_AR[0][:-1]
    L_AR[-1] = L_AR[-1][1:]
    return L_AR

def choose_df_reg(dire, data_TGV_reg_sel, data_TGV_reg_sel_inv):
    if dire : 
        return data_TGV_reg_sel_inv
    return data_TGV_reg_sel