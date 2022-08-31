import streamlit as st

from engine.data_engine import *



st.set_page_config(layout="wide")

with st.sidebar:
    select_elem = st.selectbox(
        "Choix élément",
        ('Paris - Angers', 'Paris - Arras', 'Paris - Bordeaux', 'Paris - Brest', 'Paris - Dijon', 'Paris - Grenoble', 'Paris - La Rochelle', "Paris - Lyon", "Lyon - Lille")
    )
    map = st.map()

    
sel = select_elem
aaaa = str(dt.datetime.now().year)
L_AR = gen_L_AR(sel)

data_TGV_eco_sel, data_trajet_histo_sel, data_TGV_reg_sel, data_TGV_reg_sel_inv = selection_data(sel)

data_trajet_histo_sel, temps, distance, vitesse, emission = exploitation_data_caracteristique(data_TGV_eco_sel, data_trajet_histo_sel)


container = st.container()
with container :
    
    st.markdown("***")

    col1, col2, col3, col4 = st.columns(4)

    with col1 :
        st.metric(label="Temps de trajet moyen", value=str(temps) + " minutes")
    with col2 :
        st.metric(label="Distance à parcourir", value=str(distance) + " km")
    with col3 :
        st.metric(label="Vitesse moyenne", value=str(vitesse) + " km/h")
    with col4 : 
        st.metric(label="Emission CO2", value=str(emission) + " kg")
    
    st.markdown("***")
    
    
    #col21, col22 = st.columns([2, 6])
    #with col21 :
        
        #
    #with col22:
    choice = st.radio("Paramètre en fonction du temps", ('Vitesse', 'Temps'), horizontal = True)
    fig1 = graph_data_caractéristique(data_trajet_histo_sel, choice)
    st.markdown(choice + " du trajet au fil des années")
    st.plotly_chart(fig1, use_container_width=True)
    
    
    
    
    
    st.markdown("***") 
    
    
    
    col31, col32, col33, col34, col35 = st.columns([2,2,3,3,3])
    
    
    with col31 :
        dire = st.checkbox('Inverser gare de départ')
    with col32:
        st.markdown(dest(L_AR, dire))
    retard_moy, evol_retard_moy, prct_retard, nb_train, nb_train_j  = exploitation_data_retard(choose_df_reg(dire, data_TGV_reg_sel, data_TGV_reg_sel_inv), temps, aaaa)
    choice2 = "Pourcentage"
    fig2 = graph_pie_retard(choose_df_reg(dire, data_TGV_reg_sel, data_TGV_reg_sel_inv), aaaa)
    fig3 = graph_bar_retard(choose_df_reg(dire, data_TGV_reg_sel, data_TGV_reg_sel_inv), aaaa, choice2)
    
    with col33 :
        st.markdown(desc(L_AR, nb_train, nb_train_j, dire, aaaa))
    with col34 :
        st.metric(label = "Retard moyen", value = str(retard_moy) + " minutes", delta = str(evol_retard_moy) + " %", delta_color = "inverse")   
    with col35 :
        st.metric(label = "Trajet allongé de", value = str(prct_retard) + " %")

    st.markdown("***")  
        
    col41, col42= st.columns(2)
    
    with col41 :
        st.markdown("Cause des retards et annulations de train en " + aaaa)   
        st.plotly_chart(fig2, use_container_width=True)
    with col42 :
        st.markdown("Répartitions des retards et annulations de train en " + aaaa)
        st.plotly_chart(fig3, use_container_width=True)
        #choice2 = st.radio("Valeur représentée", ('Temps', 'Vitesse'), horizontal = True)
              
    


