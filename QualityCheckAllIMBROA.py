#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      NLSGRO
#
# Created:     28-06-2018
# Copyright:   (c) NLSGRO 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import time
start = time.time()



# Import the relevant Python modules into the script
import json
import csv
import gdal
import subprocess
import pandas
import geopandas
from geojson import Point
from math import exp, sqrt
import sys
import pprint
from itertools import chain
from flask import jsonify
import re
import operator
import pprint
from collections import OrderedDict
sys.path.append("C:\Program Files\FME\fmeobjects\python27")
import fmeobjects
import arcpy
from arcpy import env
import xlwt
import matplotlib.pyplot as plt
import numpy as np

arcpy.env.workspace = "C:/Users/NLsgro/Documents/Internship/InternshipData/brogeotechnischsondeeronderzoek/"



def qualityCheck(CPTgeojson, Benchmarkgeojson, OutputCSV):

    with open(CPTgeojson) as cpt_data:
        testee = json.load(cpt_data)

    #with open(Benchmarkgeojson) as bm_data:
        #tester = json.load(bm_data)
    features = []

    print "BRO-ID"+'\t\t\t\t'+"Score"

    for feature in testee["features"]:
        #pprint.pprint(feature)

        number = 0
        #print feature["properties"]["BroID"]
        if feature["properties"]["BroID"] != "onbekend":
            number += 1

        if feature["properties"]["UitvoerderOnderzoek"] != "onbekend":
            number += 1

        if feature["properties"]["KwaliteitsRegime"] != "onbekend":
            number += 1

        if feature["properties"]["Conustype"] != "onbekend":
            number += 1

        if feature["properties"]["OmschrijvingConustype"] != "onbekend":
            number += 1

        if feature["properties"]["Sondeernorm"] != "onbekend":
            number += 1

        if feature["properties"]["Kwaliteitsklasse"] != "onbekend":
            number += 1

        if feature["properties"]["LokaalVerticaalReferentiepunt"] != "onbekend":
            number += 1
            if feature["properties"]["LokaalVerticaalReferentiepunt"] == "waterbodem":
                if feature["properties"]["Waterdiepte"] != "onbekend":
                    number += 1

        if feature["properties"]["SignaalbewerkingUitgevoerd"] != "onbekend":
            number += 1

        if feature["properties"]["BewerkingOnderbrekingenUitgevoerd"] != "onbekend":
            number += 1

        if feature["properties"]["MethodeVerticalePositiebepaling"] != "onbekend":
            number += 1

        if feature["properties"]["MethodeLocatiebepaling"] != "onbekend":
            number += 1

        if feature["properties"]["Bronhouder"] != "onbekend":
            number += 1

#        if feature["properties"]["KaderAanlevering"] != "onbekend":
#            number += 1

#        if feature["properties"]["KaderInwinning"] != "onbekend":
#            number += 1

#        if feature["properties"]["UitvoerderLocatiebepaling"] != "onbekend":
#            number += 1

#        if feature["properties"]["DatumLocatiebepaling"] != "onbekend":
#            number += 1

#        if feature["properties"]["UitvoerderVerticalePositiebepaling"] != "onbekend":
#            number += 1

#        if feature["properties"]["DatumVerticalePositiebepaling"] != "onbekend":
#            number += 1

#        if feature["properties"]["DissipatietestUitgevoerd"] != "onbekend":
#            number += 1

#        if feature["properties"]["ExpertcorrectieUitgevoerd"] != "onbekend":
#            number += 1

        if feature["properties"]["AanvullendOnderzoekUitgevoerd"] != "onbekend":
            number += 1
            if feature["properties"]["DatumOnderzoek"] != "onbekend":
                number += 1
            if feature["properties"]["Omstandigheden"] != "onbekend":
                number += 1
#            elif feature["properties"]["HoedanigheidOppervlakte"] != "onbekend":
#                number += 1
            elif feature["properties"]["Grondwaterstand"] != "onbekend":
                number += 1
            else:
                if feature["properties"]["Volgnummer"] != "onbekend":
                    number += 0.25
                if feature["properties"]["Bovengrens"] != "onbekend":
                    number += 0.25
                if feature["properties"]["Ondergrens"] != "onbekend":
                    number += 0.25
                if feature["properties"]["BeschrijvingVerwijderdeLaag"] != "onbekend":
                    number += 0.25

        if feature["properties"]["RapportagedatumOnderzoek"] != "onbekend":
            number += 1

#        if feature["properties"]["DatumLaatsteBewerking"] != "onbekend":
#            number += 1

        if feature["properties"]["ObjectIDBronhouder"] != "onbekend":
            number += 1

        if feature["properties"]["OppervlakteConuspunt"] != "onbekend":
            number += 1

        if feature["properties"]["OppervlaktequotientConuspunt"] != "onbekend":
            number += 1

        if feature["properties"]["Sondeermethode"] != "onbekend":
            number += 1

        if feature["properties"]["VoorgeboordTot"] != "onbekend":
            number += 1

        if feature["properties"]["Einddiepte"] != "onbekend":
            number += 1

        if feature["properties"]["Stopcriterium"] != "onbekend":
            number += 1

        if feature["properties"]["ConusweerstandVooraf"] != "onbekend":
            number += 1

        if feature["properties"]["ConusweerstandAchteraf"] != "onbekend":
            number += 1

        if feature["properties"]["PlaatselijkeWrijvingVooraf"] != "onbekend":
            number += 1

        if feature["properties"]["PlaatselijkeWrijvingAchteraf"] != "onbekend":
            number += 1

        if feature["properties"]["WaterspanningU1Vooraf"] != "onbekend":
            number += 1

        if feature["properties"]["WaterspanningU1Achteraf"] != "onbekend":
            number += 1

        if feature["properties"]["WaterspanningU2Vooraf"] != "onbekend":
            number += 1

        if feature["properties"]["WaterspanningU2Achteraf"] != "onbekend":
            number += 1

        if feature["properties"]["WaterspanningU3Vooraf"] != "onbekend":
            number += 1

        if feature["properties"]["WaterspanningU3Achteraf"] != "onbekend":
            number += 1

        if feature["properties"]["HellingresultanteVooraf"] != "onbekend":
            number += 1

        if feature["properties"]["HellingresultanteAchteraf"] != "onbekend":
            number += 1

        if feature["properties"]["HellingNoordZuidVooraf"] != "onbekend":
            number += 1

        if feature["properties"]["HellingNoordZuidAchteraf"] != "onbekend":
            number += 1

        if feature["properties"]["HellingOostWestVooraf"] != "onbekend":
            number += 1

        if feature["properties"]["HellingOostWestAchteraf"] != "onbekend":
            number += 1

        if feature["properties"]["ElektrischeGeleidbaarheidVooraf"] != "onbekend":
            number += 1

        if feature["properties"]["ElektrischeGeleidbaarheidAchteraf"] != "onbekend":
            number += 1

        if feature["properties"]["SensorAzimuth"] != "onbekend":
            number += 1

#        if feature["properties"]["Conusdiameter"] != "onbekend":
#            number += 1

        if feature["properties"]["Sondeertrajectlengte"] == "ja":
            number += 2

        if feature["properties"]["Conusweerstand"] == "ja":
            number += 2

        if feature["properties"]["PlaatselijkeWrijving"] == "ja":
            number += 2
            if feature["properties"]["OppervlakteKleefmantel"] != "onbekend":
                number += 1
            if feature["properties"]["OppervlaktequotientKleefmantel"] != "onbekend":
                number += 1
            if feature["properties"]["AfstandConusTotMiddenKleefmantel"] != "onbekend":
                number += 1

        if feature["properties"]["Wrijvingsgetal"] == "ja":
            number += 2
        else:
            number += 1

        if feature["properties"]["WaterspanningU1"] == "ja":
            number += 2
        else:
            number += 1

        if feature["properties"]["WaterspanningU2"] == "ja":
            number += 2
        else:
            number += 1

        if feature["properties"]["WaterspanningU3"] == "ja":
            number += 2
        else:
            number += 1

        if feature["properties"]["Hellingresultante"] == "ja":
            number += 2
        else:
            number += 1

        if feature["properties"]["HellingNoordZuid"] == "ja":
            number += 2
        else:
            number += 1

        if feature["properties"]["HellingOostWest"] == "ja":
            number += 2
        else:
            number += 1

        if feature["properties"]["Diepte"] == "ja":
            number += 2
        else:
            number += 1

        if feature["properties"]["VerlopenTijd"] == "ja":
            number += 2
        else:
            number += 1

        if feature["properties"]["GecorrigeerdeConusweerstand"] == "ja":
            number += 2
        else:
            number += 1

        if feature["properties"]["NettoConusweerstand"] == "ja":
            number += 2
        else:
            number += 1

        if feature["properties"]["Porienratio"] == "ja":
            number += 2
        else:
            number += 1

        if feature["properties"]["HellingX"] == "ja":
            number += 2
        else:
            number += 1

        if feature["properties"]["HellingY"] == "ja":
            number += 2
        else:
            number += 1

        if feature["properties"]["ElektrischeGeleidbaarheid"] == "ja":
            number += 2
        else:
            number += 1

        if feature["properties"]["MagnetischeVeldsterkteX"] == "ja":
            number += 2
        else:
            number += 1

        if feature["properties"]["MagnetischeVeldsterkteY"] == "ja":
            number += 2
        else:
            number += 1

        if feature["properties"]["MagnetischeVeldsterkteZ"] == "ja":
            number += 2
        else:
            number += 1

        if feature["properties"]["MagnetischeVeldsterkteTotaal"] == "ja":
            number += 2
        else:
            number += 1

        if feature["properties"]["MagnetischeInclinatie"] == "ja":
            number += 2
        else:
            number += 1

        if feature["properties"]["MagnetischeDeclinatie"] == "ja":
            number += 2
        else:
            number += 1

        if feature["properties"]["Temperatuur"] == "ja":
            number += 2
        else:
            number += 1

        if feature["properties"]["StarttijdMeten"] != "onbekend":
            number += 1

        if feature["properties"]["Coordinaten"] != "onbekend":
            number += 1

        if feature["properties"]["Referentiestelsel"] != "onbekend":
            number += 1

        if feature["properties"]["Verschuiving"] != "onbekend":
            number += 1

        if feature["properties"]["VerticaalReferentieVlak"] != "onbekend":
            number += 1

        #if feature["properties"][""] != "onbekend":
            #number += 1

        numberfloat = float(number)
        numberstring = str(numberfloat)
        grade = numberfloat/102*100

        features.append([feature["properties"]["BroID"], feature["properties"]["KwaliteitsRegime"], numberfloat, grade])


        #print feature["properties"]["BroID"]+'\t\t\t'+numberstring
    mergedFeatures = list(chain.from_iterable(features))
    pprint.pprint(mergedFeatures)

    """plt.hist(mergedFeatures, bins=200, histtype='barstacked', rwidth=1, facecolor='g', alpha=1)
    plt.axis([20, 112, 0, 350])
    plt.xlabel("CPT Score")
    plt.ylabel("N")
    plt.title("CPT IMBRO/A Scores")
    plt.show()"""

    with open(OutputCSV, 'w') as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(features)








#if feature["properties"][""] != "onbekend":
    #number += 1




CPTgeojson = "C:/Users/NLsgro/Documents/Internship/InternshipData/brogeotechnischsondeeronderzoek/bro_cpt_sample.geojson"
Benchmarkgeojson = "C:/Users/NLsgro/Documents/Internship/InternshipData/brogeotechnischsondeeronderzoek/bro_benchmark.geojson"
OutputCSV = "C:/Users/NLsgro/Documents/Internship/InternshipData/brogeotechnischsondeeronderzoek/cpt_IMBROA_quality_scores.csv"

qualityCheck(CPTgeojson, Benchmarkgeojson, OutputCSV)
print 'It took', time.time()-start, 'seconds.'