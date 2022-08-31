dic_TGV_reg = {'Date' : 'date',
 'Service' : 'service',
 'Gare de départ' : 'gare_dep',
 "Gare d'arrivée" : 'gare_arr',
 'Durée moyenne du trajet' : 'trajet_temps_moy',
 'Nombre de circulations prévues' : 'nb_train',
 'Nombre de trains annulés' : 'nb_train_annule',
 'Commentaire annulations' : 'commentaire_annulation',
 'Nombre de trains en retard au départ' : 'nb_train_retard_dep',
 'Retard moyen des trains en retard au départ' : 'retard_train_retard_dep_moy',
 'Retard moyen de tous les trains au départ' : 'retard_train_dep_moy',
 'Commentaire retards au départ' : 'commentaire_retard_dep',
 "Nombre de trains en retard à l'arrivée" : 'nb_train_retard_arr',
 "Retard moyen des trains en retard à l'arrivée" : 'retard_train_retard_arr_moy' ,
 "Retard moyen de tous les trains à l'arrivée": 'retard_train_arr_moy',
 "Commentaire retards à l'arrivée" : 'commentaire_retard_arr',
 'Nombre trains en retard > 15min' : 'nb_train_retard_min_15',
 'Retard moyen trains en retard > 15 (si liaison concurrencée par vol)' : 'retard_train_retard_min_15_moy',
 'Nombre trains en retard > 30min' : 'nb_train_retard_min_30',
 'Nombre trains en retard > 60min' : 'nb_train_retard_min_60',
 'Prct retard pour causes externes' : 'prct_retard_causes_externes',
 'Prct retard pour cause infrastructure' : 'prct_retard_causes_infrastructure',
 'Prct retard pour cause gestion trafic' : 'prct_retard_causes_gestion_trafic',
 'Prct retard pour cause matériel roulant' : 'prct_retard_causes_materiel_roulant',
 'Prct retard pour cause gestion en gare et réutilisation de matériel' : 'prct_retard_causes_gestion_gare_reutilisation_materiel',
 'Prct retard pour cause prise en compte voyageurs (affluence, gestions PSH, correspondances)' : 'prct_retard_causes_voyageurs'}

dic_TGV_eco = {'Type de trajet': 'type_trajet',
               'Liaison': 'trajet_liaison',
               'Distance (km)' : 'distance',
               'TGV (1 pers.) - Empreinte CO2e (kgCO2e/voyageur)' : 'empreinte'}

dic_trajet_histo = {'Relations': 'trajet',
                     'Annee': 'annee',
                     'Temps estime en minutes' : 'est_temps_min'}


L_prct = ['prct_retard_causes_externes',
          'prct_retard_causes_infrastructure',
          'prct_retard_causes_gestion_trafic',
          'prct_retard_causes_materiel_roulant',
          'prct_retard_causes_gestion_gare_reutilisation_materiel',
          'prct_retard_causes_voyageurs']

L_retard = ['nb_train_annule', 'nb_train_retard_arr', 'nb_train_retard_min_15', 'nb_train_retard_min_30', 'nb_train_retard_min_60']

