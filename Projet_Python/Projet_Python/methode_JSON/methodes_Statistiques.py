#File contenant toutes les méthodes liées à la page de la commune pour visualiser différentes données statistiques
#! SAVE dans le dossier "Projet_Python/Graphs_Stats/"

#! """ Import """
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import squarify #Pour le TreeMap
import os
import pandas as pd
from pandas import DataFrame
import datetime
from datetime import timedelta, date
import json
from matplotlib.ticker import  MaxNLocator


import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot




#! """ Dataset"""
#Rappel :
#Data récupérées en sortie de commande : {'Qt_Pain': '2', 'Qt_Riz': '3', 'Qt_Farine': '0', 'Qt_Pommes': '6', 'Qt_lait': '10'}
#! Il faut un dataset de cette forme pour vouvir le convertir en DataFrame panda
#commandeJson = {"tomates" : 12, "pain" : 5, "riz": 9, "pate" : 6, "farine":4}
commandeJson = dict()

def ConvertToStatisticsUse():
    with open('./JSON/commandes_faites.json') as json_file: #On importe le fichier des commanes
        fichier = json.load(json_file)
        print(fichier)
    json_file.close()
    #On va le travailler pour l'avoir sous le format : commandeJson = {"tomates" : 12, "pain" : 5, "riz": 9, "pate" : 6, "farine":4}
    for uneCommande in fichier["commandes"]:#Commande n°1
        print("uneCommande => ", uneCommande)
        for unProduit in uneCommande:
            #SI Le produit est déjà dans notre dictionnaire final et ce n'est pas l'id ou la date ou le CP
            if(unProduit in commandeJson.keys() and unProduit != "id" and unProduit != "Date" and unProduit != "CP" and uneCommande[str(unProduit)] != "0"): 
                addValue = commandeJson[unProduit] + int(uneCommande[unProduit])
                commandeJson[unProduit] = addValue
            #Sinon si ce n'est pas l'id ou la date
            #Alors on l'ajoute au dico final
            elif(unProduit != "id" and unProduit != "Date" and unProduit != "CP" and uneCommande[str(unProduit)] != "0"):
                commandeJson[unProduit] = int(uneCommande[unProduit])
    print("CommandesJSON",commandeJson)

### Histogramme de la quantité de commande de chaque produit ###

# Lien Web : 
# https://www.science-emergence.com/Articles/Simple-histogramme-avec-matplotlib/
# http://www.python-simple.com/python-matplotlib/histogram.php 
def Histo_Product():
    if(os.path.isfile("assets/Image/Histo_Quantite-totale-produit.png")):
        os.remove("assets/Image/Histo_Quantite-totale-produit.png") #Supprimer l'image actuelle
    plt.bar(x=commandeJson.keys(), height=commandeJson.values(), align='center', color='b')
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Produits')
    plt.ylabel('Quantité totale')
    plt.title('Histogramme des quantités totales commandées pour chaque produit')  
    
    plt.savefig("assets/Image/Histo_Quantite-totale-produit.png")
    #plt.show() #! D'abord SAVE et ensuite SHOW
    plt.close()#On ferme le plot sinon les figures se superposent et l'enregistrement est corrompu
    #Emplacement : D:\Programmes\Git-Hub_Projet\Projet-Python_A3
    #!On peut préciser l'emplacement de stockage : plt.savefig('Sub Directory/graph.png')
    


### Diagramme circulaire (Pie Chart) ###
#Site Web : Pie Chart : 
# https://www.science-emergence.com/Articles/Simple-diagramme-circulaire-avec-matplotlib/

def PieChart_Product():
    if(os.path.isfile('assets/Image/Pie-Chart_Quantite-totale-produit.png')):
        os.remove('assets/Image/Pie-Chart_Quantite-totale-produit.png')#Supprimer l'image actuelle
    plt.pie(commandeJson.values(), labels=commandeJson.keys(), autopct='%1.1f%%', shadow=True, startangle=90)
    #Couleurs gérées automatiquement 
    # (possibilité de forcer avec : myColors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
    #  et dans plt.pie() rajouter : colors = myColors MAIS que 4 couleurs
    plt.axis('equal')
    plt.title('Pie-Chart des quantités totales commandées pour chaque produit')

    plt.savefig('assets/Image/Pie-Chart_Quantite-totale-produit.png')
    #plt.show()
    plt.close()#On ferme le plot sinon les figures se superposent et l'enregistrement est corrompu
    

### TreeMap ###
#Site Web : https://jingwen-z.github.io/data-viz-with-matplotlib-series5-treemap/

def TreeMap_Product():
    if(os.path.isfile('assets/Image/TreeMap_Quantite-totale-produit.png')):
        os.remove('assets/Image/TreeMap_Quantite-totale-produit.png')#Supprimer l'image actuelle
    plt.rc('font', size=14)
    squarify.plot(sizes = commandeJson.values(), label=commandeJson.keys(), alpha=0.7)
    plt.axis('off')
    plt.title('TreeMap des quantités par produit')

    plt.savefig('assets/Image/TreeMap_Quantite-totale-produit.png')
    plt.close()
    #plt.show()


### Nombre de commandes par jour depuis le début (2020-05-01)
def GraphTotalCommande():
    # On fait une liste des dates entre le 01/05 et aujourd'hui
    startdate = date(2020,5,1)#Date du début
    enddate = date.today()#Date d'aujourd'hui 
    listejours=[]#tableau de chaque date entre le début et aujourd'hui
    for n in range(int ((enddate - startdate).days)+1):
        listejours.append( (startdate + timedelta(n)).strftime("%Y-%m-%d"))
        #Save sous forme de string de la forme dd-mm-YYYY de toutes les dates de l'intervalle
    #on cherche le nb de commande par date
    #listejours = ['2020-05-01', '2020-05-02', '2020-05-03']

    #Beosin d'avoir un dico de la forme suivante pour utilisation de Panda : (DATES sous la forme YYYY-mm-dd et non dd-mm-YYYY)
    #dicoJourNmbCommande = {"Date":['01-05-2020', '02-05-2020', '03-05-2020', '04-05-2020', '05-05-2020', '06-05-2020', '07-05-2020', '08-05-2020', '09-05-2020'],
                            #"TotalCommandeJour" : [4,6,8,5,3,7,5,11,6],
                            #"TotalCommandeCumule":[4,10,18,23,26,33,38,49,55]}
    dicoJourNmbCommande = {"Date":listejours, "TotalCommandeJour":[], "TotalCommandeCumule":[]}

    with open('./JSON/commandes_faites.json') as json_file:
        fichier = json.load(json_file)
        listCommandes = fichier['commandes']
        cumulNbCommande = 0
        for day in listejours :
            total = 0
            for order in listCommandes :
                if(order["Date"] == day):
                    total += 1
            dicoJourNmbCommande["TotalCommandeJour"].extend([total])
            dicoJourNmbCommande["TotalCommandeCumule"].extend([cumulNbCommande + total])
            cumulNbCommande += total
    json_file.close()

    pandaJourCommande = DataFrame(dicoJourNmbCommande)
    #print(pandaJourCommande)
    pandaJourCommande['Date'] = pd.to_datetime(pandaJourCommande['Date'])
    myFig = pandaJourCommande.plot(x="Date", y="TotalCommandeCumule", x_compat=True,
                            kind='line',title="Graphique des commandes cumulées depuis le " + startdate.strftime(("%Y-%m-%d")),
                            grid=True, legend = False, figsize=(15,6), color='g')
    myFig.xaxis.set_major_locator(mdates.DayLocator(bymonthday=range(1,32,2)))
    myFig.get_figure().savefig('assets/Image/Cumule-Commandes.png')



#n'est jamais appelé car elle a pour but de ne pas faire planter la carte si le produit choisi par l'admin n'a jamais été commandé
def Sauvegarde_Commande_Initialisation_Carte():
    {
            "CP":"75001",
            "id":"a",
            "Date":"2020-04-30",
            "Choucroute":"0",
            "Farine":"0",
            "Frites":"0",
            "Oeuf":"0",
            "Pate":"0",
            "Poulet":"0",
            "SelPoivre":"0",
            "Epice":"0",
            "Assaisonnements":"0",
            "Pomme_de_terre":"0",
            "Tomate":"0",
            "Pomme":"0",
            "Citron":"0",
            "Riz":"0",
            "Sucre":"0",
            "Pain":"0",
            "Lait":"0",
            "Beurre":"0",
            "Fromage":"0",
            "Creme":"0",
            "Poisson":"0",
            "MedKit":"0",
            "Pilule":"0",
            "KitSoin":"0",
            "KitEntretien":"0"
        },




def Arrondissement_Map(Product_name):
    with open('./JSON/arrondissements.geojson') as json_file:
        data_arrondissements = json.load(json_file)


    with open('./JSON/commandes_faites.json') as json_file:
        fichier = json.load(json_file)
        commandes=fichier['commandes']

    df = pd.DataFrame(commandes)
    df = df.fillna(0) #si une commande contient certains produits mais pas d'autres, leur valeur dans le dataframe sera "NaN" et ne pourra être lu lors de la conversion en int

    #on fait un astype(dict) avec dict contenant le nom d'une colonne et un type pour convertir une colonne en un type particulier
    #chaque colonne de produit ayant une quantité de type str, on convertit la colonne voulu (=le produit selectionné) en int afin de pouvoir faire sum
    #on met le reset index pour conserver un dataframe, sinon on a un SeriesFrame
    #on groupy by CP et on compte dans chaque CP le nombre de produit commandés
    fig = go.Figure(px.choropleth_mapbox(df.astype({Product_name:int}).groupby('CP')[Product_name].sum().reset_index(), 
                    geojson=data_arrondissements, 
                    locations='CP', 
                    color=Product_name,
                    #color_continuous_scale="Viridis", #couleur peut etre changer surement
                    mapbox_style="carto-positron",
                    zoom=10, center = {"lat": 48.8534, "lon": 2.3488},
                    opacity=0.5,
                    labels={'quantite':'quantite de produit'},
                    ))
    
    fig.update_layout(height=600,
                    width=600,
                    title_text='Quantité du produit commandé par arrondissement',
                    )

    return plot(fig, output_type='div')

def Quantite_Client():
    if(os.path.isfile('assets/Image/Totaux_Personnes_Courbe.png')):
        os.remove('assets/Image/Totaux_Personnes_Courbe.png')#Supprimer l'image actuelle

    # Je veux montrer l'évolution du nb de personne avec un compte depuis le lancement du site, on va dire que le site est lancé le 01/05
    # On fait une liste des dates entre le 01/05 et aujourd'hui
    startdate = datetime.date(2020,5,1)
    enddate = datetime.date.today()
    listejours=[]
    for n in range(int ((enddate - startdate).days)+1):
        listejours.append( (startdate + timedelta(n)).strftime("%Y-%m-%d"))
    #on cherche le nb de client par date
    Liste_Totaux_Personnes = [0]
    #* On initialise le premier terme
    f=open('./JSON/infos_client.json')
    fichier = json.load(f)
    temp = fichier['foyers']
    for element in temp:
        if(element['Date']==startdate.strftime("%Y-%m-%d")):
            Liste_Totaux_Personnes[0]+=len(element['Personnes'])
    #* Maintenant on fait les autres dates
    for index_jour in range(1,len(listejours)):
        date_actu = listejours[index_jour]
        Liste_Totaux_Personnes.append(0)
        for element in temp:
            if(element['Date']==date_actu):
                Liste_Totaux_Personnes[index_jour]+=len(element['Personnes'])
        Liste_Totaux_Personnes[index_jour]+= Liste_Totaux_Personnes[index_jour-1]
    print('Liste', Liste_Totaux_Personnes)
    Data={
        'Jours' : listejours,
        'Totaux_Personnes':Liste_Totaux_Personnes
    }
    df=DataFrame(Data,columns=['Jours','Totaux_Personnes'])
    df['Jours']= pd.to_datetime(df['Jours'])
    fig = df.plot(x='Jours', y='Totaux_Personnes',figsize=(10,10),x_compat=True)
    fig.xaxis.set_major_locator(mdates.DayLocator(bymonthday=range(1,32,2)))
    fig.get_figure().savefig('assets/Image/Totaux_Personnes_Courbe.png')

def EntrepotArrondissement():
    df=pd.DataFrame({ 'Arrondissement':[75001,75002,75003,75004,75005,75006,75007,75008,75009,75010,75011,75012,75013,75014,75015,75016,75017,75018,75019,75020],
    'N_tel_Entrepôt':['013075001','013075002','013075003','013075004','013075005','013075006','013075007','013075008',
    '013075009','013075010','013075011','013075012','013075013','013075014','013075015','013075016','013075017','0130750018','0130750019','013075020'],
    'Adresse':['adresse entrepôt','adresse entrepôt','adresse entrepôt','adresse entrepôt','adresse entrepôt','adresse entrepôt','adresse entrepôt',
    'adresse entrepôt','adresse entrepôt','adresse entrepôt','adresse entrepôt','adresse entrepôt','adresse entrepôt','adresse entrepôt','adresse entrepôt',
    'adresse entrepôt','adresse entrepôt','adresse entrepôt','adresse entrepôt','adresse entrepôt']

    })
    df.index = df.index + 1
    html = df.to_html(table_id='Entrepot', justify='center')
    return html

def DetailCommandeToday():
    dataBrute = {"Produit":["Frites", "Poivre", "Fromage","Lait", "Tomate"],
            "Quantite":[15, 6, 30,40,25],
            "Arrondissement":["75001","75002","75001","75003","75002"]}

    listArrondissements = ["75001","75002","75003","75004","75005","75006","75007","75008","75009","75010",
                            "75011","75012","75013","75014","75015","75016","75017","75018","75019","75020"]

    dicoPorduitOneDay = {"Produit":[], "Quantite":[], "Arrondissement":[]}
    todayDate = date.today().strftime("%Y-%m-%d")
    #Lecture du fichier des commandes pour prendre celles du jour
    with open('./JSON/commandes_faites.json') as json_file: #./JSON/commandes_faites.json
        fichier = json.load(json_file)
        listCommandes = fichier['commandes']
        for arrondissement in listArrondissements :
            listProduit_UnArrondissement = dict()
            for order in listCommandes :
                if(order["Date"] == todayDate and order["CP"]== arrondissement):
                    for unProduit in order:
                        #SI Le produit est déjà dans notre dictionnaire de l'arrondissement et ce n'est pas l'id ou la date ou le CP
                        if(unProduit in listProduit_UnArrondissement.keys() and unProduit != "id" and unProduit != "Date" and unProduit != "CP"): 
                            addValue = listProduit_UnArrondissement[unProduit] + int(order[unProduit])
                            listProduit_UnArrondissement[unProduit] = addValue
                        #Sinon si ce n'est pas l'id ou la date ou le CP
                        #Alors on l'ajoute au dico final
                        elif(unProduit != "id" and unProduit != "Date" and unProduit != "CP"):
                            listProduit_UnArrondissement[unProduit] = int(order[unProduit])
            #On ajoute les clés (donc les produits) à la liste des produits           
            dicoPorduitOneDay['Produit'].extend(listProduit_UnArrondissement.keys())
            #On ajoute la quantité totale de chaque porduit pr cet arrondissement à la liste des quantités  
            dicoPorduitOneDay['Quantite'].extend(listProduit_UnArrondissement.values())
            dicoPorduitOneDay['Arrondissement'].extend([arrondissement]*len(listProduit_UnArrondissement.keys()))
        
        
    dataPandasFormat = pd.DataFrame(dicoPorduitOneDay)
    #Trie par ordre décroissant
    dataPandasFormat_Sorted_Desc = dataPandasFormat.sort_values(by="Quantite", ascending=False).reset_index(drop=True)
    print("Sorted_Desc : \n", dataPandasFormat_Sorted_Desc)
    #Modification des colonnes en mettant les CP en index de colonne
    dataPandasFormat_Pivot = dataPandasFormat_Sorted_Desc.pivot("Produit","Arrondissement","Quantite")
    dataPandasFormat_Pivot = dataPandasFormat_Pivot.fillna(0) #Remplace tous les NaN par des 0
    dataPandas_HtmlFormat = dataPandasFormat_Pivot.to_html(table_id='OrderOfTheDay', justify='center')
    return dataPandas_HtmlFormat