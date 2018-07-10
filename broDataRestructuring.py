#-------------------------------------------------------------------------------
# Name:        JSON reformattor
# Purpose:     To restructure a geojson file that was transformed from bro-xml
#
# Author:      Simon Groen
#
# Created:     13-06-2018
# Copyright:   (c) NLSGRO 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------



"""
De benodigde Python modules worden geimporteerd en omgevingvariabelen worden bepaald
"""
import json
import gdal
import subprocess
import pandas
import geopandas
from geojson import Point
from math import exp, sqrt
import sys
import pprint
from itertools import izip
from flask import jsonify
import re
import operator
from collections import OrderedDict
sys.path.append("C:\Program Files\FME\fmeobjects\python27")
import fmeobjects



"""
Een definitie waarmee de workspace die het xml bestand omzet in een geojson bestand wordt gerunned
"""
# https://stackoverflow.com/questions/5967500/how-to-correctly-sort-a-string-with-a-number-inside
# https://stackoverflow.com/questions/2545532/python-analog-of-natsort-function-sort-a-list-using-a-natural-order-algorithm
def xmlToJSON(in_xml, out_geojson):
    runner = fmeobjects.FMEWorkspaceRunner()
    workspace = "C:\Users\NLsgro\Documents\Internship\Workspaces\bro_xml_conversions.fmw"
    parameters = {}
    parameters['SourceDataset_SHAPE'] = in_file
    parameters['DestDataset_SHAPE'] = out_file
    runner.runWithParameters(workspace, parameters)



"""
Twee definities die zorgen dat wanneer het geojson bestand aan het einde nog naar een correcte structuur wordt gezet, de meetwaardes op volgorde blijven staan
"""
def atof(text):
    try:
        retval = float(text)
    except ValueError:
        retval = text
    return retval



def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    float regex comes from https://stackoverflow.com/a/12643073/190597
    '''
    return [ atof(c) for c in re.split(r'[+-]?([0-9]+(?:[.][0-9]*)?|[.][0-9]+)', text) ]



"""
Een Python definitie waarmee de aangeleverde en van xml naar json omgezette BRO conforme bestanden worden geherstructureerd en overzichtelijker worden gemaakt
"""
def RestructuringJSON(inputPoints, outputPoints):

    # Het json bestand wordt geopend in het script
    with open(inputPoints) as json_data:
        data = json.load(json_data)

    # Er wordt een lege list aangemaakt die opgevuld gaat worden met waardes
    features = []

    # Er wordt een lege list aangemaakt die opgevuld gaat worden met de features
    objects = []

    # Het beginnummer van de opvolgende 'for loop' wordt bepaald op het eerste json object
    number = 0

    # Het gebruikte referentiestelsel, welke bij de algemene info staat voor alle json objecten
    #Referentiestelsel = data["crs"]["properties"]["name"]
    Referentiestelsel = "EPSG:4258"

    for feature in data["features"]:

        # De waardes per variabel worden ingeladen
        # Algemene variabelen
        try:
            BroID = feature["properties"]["broId"]
        except KeyError:
            BroID = "onbekend"

        try:
            UitvoerderOnderzoek = feature["properties"]["deliveryAccountableParty"]
        except KeyError:
            UitvoerderOnderzoek = "onbekend"

        try:
            KwaliteitsRegime = feature["properties"]["qualityRegime"]
        except KeyError:
            KwaliteitsRegime = "onbekend"

        try:
            Conustype = feature["properties"]["conePenetrometerSurvey.conePenetrometer.conePenetrometerType"]
        except KeyError:
            Conustype = "onbekend"

        try:
            OmschrijvingConustype = feature["properties"]["conePenetrometerSurvey.conePenetrometer.description"]
        except KeyError:
            OmschrijvingConustype = "onbekend"

        try:
            Sondeernorm = feature["properties"]["cptStandard"]
        except KeyError:
            Sondeernorm = "onbekend"

        try:
            Kwaliteitsklasse = feature["properties"]["conePenetrometerSurvey.qualityClass"]
        except KeyError:
            Kwaliteitsklasse = "onbekend"

        try:
            LokaalVerticaalReferentiepunt = feature["properties"]["deliveredVerticalPosition.localVerticalReferencePoint"]
        except KeyError:
            LokaalVerticaalReferentiepunt = "onbekend"

        try:
            Omstandigheden = feature["properties"]["additionalInvestigationPerformed.circumstances"]   ##Check it!!!
        except KeyError:
            Omstandigheden = "onbekend"

        try:
            SignaalbewerkingUitgevoerd = feature["properties"]["conePenetrometerSurvey.procedure.signalProcessingPerformed"]
        except KeyError:
            SignaalbewerkingUitgevoerd = "onbekend"

        try:
            BewerkingOnderbrekingenUitgevoerd = feature["properties"]["conePenetrometerSurvey.procedure.interruptionProcessingPerformed"]
        except KeyError:
            BewerkingOnderbrekingenUitgevoerd = "onbekend"

        try:
            MethodeVerticalePositiebepaling = feature["properties"]["deliveredVerticalPosition.verticalPositioningMethod"]
        except KeyError:
            MethodeVerticalePositiebepaling = "onbekend"

        try:
            MethodeLocatiebepaling = feature["properties"]["deliveredLocation.horizontalPositioningMethod"]
        except KeyError:
            MethodeLocatiebepaling = "onbekend"

        try:
            Bronhouder = feature["properties"]["deliveryAccountableParty"]
        except KeyError:
            Bronhouder = "onbekend"

        try:
            KaderAanlevering = feature["properties"]["deliveryContext"]
        except KeyError:
            KaderAanlevering = "onbekend"

        try:
            KaderInwinning = feature["properties"]["surveyPurpose"]
        except KeyError:
            KaderInwinning = "onbekend"

        try:
            UitvoerderLocatiebepaling = "onbekend"
        except KeyError:
            UitvoerderLocatiebepaling = "onbekend"

        try:
            DatumLocatiebepaling = feature["properties"]["deliveredLocation.horizontalPositioningDate.date"]
        except KeyError:
            DatumLocatiebepaling = "onbekend"

        try:
            UitvoerderVerticalePositiebepaling = "onbekend"
        except KeyError:
            UitvoerderVerticalePositiebepaling = "onbekend"

        try:
            DatumVerticalePositiebepaling = feature["properties"]["deliveredVerticalPosition.verticalPositioningDate.date" ]
        except KeyError:
            DatumVerticalePositiebepaling = "onbekend"

        try:
            HoedanigheidOppervlakte = "onbekend"
        except KeyError:
            HoedanigheidOppervlakte = "onbekend"

        try:
            DissipatietestUitgevoerd = feature["properties"]["conePenetrometerSurvey.dissipationTestPerformed"]
        except KeyError:
            DissipatietestUitgevoerd = "onbekend"

        try:
            ExpertcorrectieUitgevoerd = feature["properties"]["conePenetrometerSurvey.procedure.expertCorrectionPerformed"]
        except KeyError:
            ExpertcorrectieUitgevoerd = "onbekend"

        try:
            AanvullendOnderzoekUitgevoerd = feature["properties"]["additionalInvestigationPerformed"]
        except KeyError:
            AanvullendOnderzoekUitgevoerd = "onbekend"

        try:
            RapportagedatumOnderzoek = feature["properties"]["researchReportDate.date"]
        except KeyError:
            RapportagedatumOnderzoek = "onbekend"

        try:
            DatumLaatsteBewerking = feature["properties"]["conePenetrometerSurvey.finalProcessingDate.voidReason"]
        except KeyError:
            DatumLaatsteBewerking = "onbekend"

        try:
            DatumOnderzoek = feature["properties"]["additionalInvestigation.investigationDate.date"]
        except KeyError:
            DatumOnderzoek = "onbekend"

        try:
            ObjectIDBronhouder = "onbekend"
        except KeyError:
            ObjectIDBronhouder = "onbekend"



        # Meetapparaat eigenschappen variabelen
        try:
            if feature["properties"]["conePenetrometerSurvey.conePenetrometer.coneSurfaceArea"] != "":
                OppervlakteConuspunt = feature["properties"]["conePenetrometerSurvey.conePenetrometer.coneSurfaceArea"]
            else:
                OppervlakteConuspunt = "onbekend"
        except KeyError:
            OppervlakteConuspunt = "onbekend"

        try:
            if feature["properties"]["conePenetrometerSurvey.conePenetrometer.frictionSleeveSurfaceArea"] != "":
                OppervlakteKleefmantel = feature["properties"]["conePenetrometerSurvey.conePenetrometer.frictionSleeveSurfaceArea"]
            else:
                OppervlakteKleefmantel = "onbekend"
        except KeyError:
            OppervlakteKleefmantel = "onbekend"

        try:
            if feature["properties"]["conePenetrometerSurvey.conePenetrometer.coneSurfaceQuotient"] != "":
                OppervlaktequotientConuspunt = feature["properties"]["conePenetrometerSurvey.conePenetrometer.coneSurfaceQuotient"]
            else:
                OppervlaktequotientConuspunt = "onbekend"
        except KeyError:
            OppervlaktequotientConuspunt = "onbekend"

        try:
            if feature["properties"]["conePenetrometerSurvey.conePenetrometer.frictionSleeveSurfaceQuotient"] != "":
                OppervlaktequotientKleefmantel = feature["properties"]["conePenetrometerSurvey.conePenetrometer.frictionSleeveSurfaceQuotient"]
            else:
                OppervlaktequotientKleefmantel = "onbekend"
        except KeyError:
            OppervlaktequotientKleefmantel = "onbekend"

        try:
            if feature["properties"]["conePenetrometerSurvey.conePenetrometer.coneToFrictionSleeveDistance"] != "":
                AfstandConusTotMiddenKleefmantel = feature["properties"]["conePenetrometerSurvey.conePenetrometer.coneToFrictionSleeveDistance"]
            else:
                AfstandConusTotMiddenKleefmantel = "onbekend"
        except KeyError:
            AfstandConusTotMiddenKleefmantel = "onbekend"

        try:
            Sondeermethode = feature["properties"]["conePenetrometerSurvey.cptMethod"]
        except KeyError:
            Sondeermethode = "onbekend"

        try:
            VoorgeboordTot = feature["properties"]["conePenetrometerSurvey.trajectory.predrilledDepth"]
        except KeyError:
            VoorgeboordTot = "onbekend"

        try:
            Grondwaterstand = feature["properties"]["additionalInvestigation.groundwaterLevel"] ##Check!!
        except KeyError:
            Grondwaterstand = "onbekend"

        try:
            Waterdiepte = feature["properties"]["deliveredVerticalPosition.waterDepth"]
        except KeyError:
            Waterdiepte = "onbekend"

        try:
            Einddiepte = feature["properties"]["conePenetrometerSurvey.trajectory.finalDepth"]
        except KeyError:
            Einddiepte = "onbekend"

        try:
            Stopcriterium = feature["properties"]["conePenetrometerSurvey.stopCriterion"]
        except KeyError:
            Stopcriterium = "onbekend"



        # Nulmeting variabelen
        try:
            ConusweerstandVooraf = feature["properties"]["conePenetrometerSurvey.conePenetrometer.zeroLoadMeasurement.coneResistanceBefore"]
        except KeyError:
            ConusweerstandVooraf = "onbekend"

        try:
            ConusweerstandAchteraf = feature["properties"]["conePenetrometerSurvey.conePenetrometer.zeroLoadMeasurement.coneResistanceAfter"]
        except KeyError:
            ConusweerstandAchteraf = "onbekend"

        try:
            PlaatselijkeWrijvingVooraf = feature["properties"]["conePenetrometerSurvey.conePenetrometer.zeroLoadMeasurement.localFrictionBefore"]
        except KeyError:
            PlaatselijkeWrijvingVooraf = "onbekend"

        try:
            PlaatselijkeWrijvingAchteraf = feature["properties"]["conePenetrometerSurvey.conePenetrometer.zeroLoadMeasurement.localFrictionAfter"]
        except KeyError:
            PlaatselijkeWrijvingAchteraf = "onbekend"

        try:
            WaterspanningU1Vooraf = feature["properties"]["conePenetrometerSurvey.conePenetrometer.zeroLoadMeasurement.porePressureU1Before"]
        except KeyError:
            WaterspanningU1Vooraf = "onbekend"

        try:
            WaterspanningU1Achteraf = feature["properties"]["conePenetrometerSurvey.conePenetrometer.zeroLoadMeasurement.porePressureU1After"]
        except KeyError:
            WaterspanningU1Achteraf = "onbekend"

        try:
            WaterspanningU2Vooraf = feature["properties"]["conePenetrometerSurvey.conePenetrometer.zeroLoadMeasurement.porePressureU2Before"]
        except KeyError:
            WaterspanningU2Vooraf = "onbekend"

        try:
            WaterspanningU2Achteraf = feature["properties"]["conePenetrometerSurvey.conePenetrometer.zeroLoadMeasurement.porePressureU2After"]
        except KeyError:
            WaterspanningU2Achteraf = "onbekend"

        try:
            WaterspanningU3Vooraf = feature["properties"]["conePenetrometerSurvey.conePenetrometer.zeroLoadMeasurement.porePressureU3Before"]
        except KeyError:
            WaterspanningU3Vooraf = "onbekend"

        try:
            WaterspanningU3Achteraf = feature["properties"]["conePenetrometerSurvey.conePenetrometer.zeroLoadMeasurement.porePressureU3After"]
        except KeyError:
            WaterspanningU3Achteraf = "onbekend"

        try:
            HellingresultanteVooraf = feature["properties"]["conePenetrometerSurvey.conePenetrometer.zeroLoadMeasurement.inclinationResultantBefore"]
        except KeyError:
            HellingresultanteVooraf = "onbekend"

        try:
            HellingresultanteAchteraf = feature["properties"]["conePenetrometerSurvey.conePenetrometer.zeroLoadMeasurement.inclinationResultantAfter"]
        except KeyError:
            HellingresultanteAchteraf = "onbekend"

        try:
            HellingNoordZuidVooraf = feature["properties"]["conePenetrometerSurvey.conePenetrometer.zeroLoadMeasurement.inclinationNSBefore"]
        except KeyError:
            HellingNoordZuidVooraf = "onbekend"

        try:
            HellingNoordZuidAchteraf = feature["properties"]["conePenetrometerSurvey.conePenetrometer.zeroLoadMeasurement.inclinationNSAfter"]
        except KeyError:
            HellingNoordZuidAchteraf = "onbekend"

        try:
            HellingOostWestVooraf = feature["properties"]["conePenetrometerSurvey.conePenetrometer.zeroLoadMeasurement.inclinationEWBefore"]
        except KeyError:
            HellingOostWestVooraf = "onbekend"

        try:
            HellingOostWestAchteraf = feature["properties"]["conePenetrometerSurvey.conePenetrometer.zeroLoadMeasurement.inclinationEWAfter"]
        except KeyError:
            HellingOostWestAchteraf = "onbekend"

        try:
            ElektrischeGeleidbaarheidVooraf = feature["properties"]["conePenetrometerSurvey.conePenetrometer.zeroLoadMeasurement.electricalConductivityBefore"]
        except KeyError:
            ElektrischeGeleidbaarheidVooraf = "onbekend"

        try:
            ElektrischeGeleidbaarheidAchteraf = feature["properties"]["conePenetrometerSurvey.conePenetrometer.zeroLoadMeasurement.electricalConductivityAfter"]
        except KeyError:
            ElektrischeGeleidbaarheidAchteraf = "onbekend"

        try:
            SensorAzimuth = feature["properties"]["conePenetrometerSurvey.conePenetrometer.zeroLoadMeasurement.sensorAzimuth"]
        except KeyError:
            SensorAzimuth = "onbekend"

        try:
            Conusdiameter = feature["properties"]["conePenetrometerSurvey.conePenetrometer.zeroLoadMeasurement.coneDiameter"]
        except KeyError:
            Conusdiameter = "onbekend"



        # De volgende 25 variabelen bevatten een indicatie of er waardes zijn en zo ja, dan zitten die waardes per meting in een string opgeslagen (altijd aanwezig)
        Sondeertrajectlengte = feature["properties"]["conePenetrometerSurvey.parameters.penetrationLength"]
        Conusweerstand = feature["properties"]["conePenetrometerSurvey.parameters.coneResistance"]
        PlaatselijkeWrijving = feature["properties"]["conePenetrometerSurvey.parameters.localFriction"]
        Wrijvingsgetal = feature["properties"]["conePenetrometerSurvey.parameters.frictionRatio"]
        WaterspanningU1 = feature["properties"]["conePenetrometerSurvey.parameters.porePressureU1"]
        WaterspanningU2 = feature["properties"]["conePenetrometerSurvey.parameters.porePressureU2"]
        WaterspanningU3 = feature["properties"]["conePenetrometerSurvey.parameters.porePressureU3"]
        Hellingresultante = feature["properties"]["conePenetrometerSurvey.parameters.inclinationResultant"]
        HellingNoordZuid = feature["properties"]["conePenetrometerSurvey.parameters.inclinationNS"]
        HellingOostWest = feature["properties"]["conePenetrometerSurvey.parameters.inclinationEW"]
        Diepte = feature["properties"]["conePenetrometerSurvey.parameters.depth"]
        VerlopenTijd = feature["properties"]["conePenetrometerSurvey.parameters.elapsedTime"]
        GecorrigeerdeConusweerstand = feature["properties"]["conePenetrometerSurvey.parameters.correctedConeResistance"]
        NettoConusweerstand = feature["properties"]["conePenetrometerSurvey.parameters.netConeResistance"]
        Porienratio = feature["properties"]["conePenetrometerSurvey.parameters.poreRatio"]
        HellingX = feature["properties"]["conePenetrometerSurvey.parameters.inclinationX"]
        HellingY = feature["properties"]["conePenetrometerSurvey.parameters.inclinationY"]
        ElektrischeGeleidbaarheid = feature["properties"]["conePenetrometerSurvey.parameters.electricalConductivity"]
        MagnetischeVeldsterkteX = feature["properties"]["conePenetrometerSurvey.parameters.magneticFieldStrengthX"]
        MagnetischeVeldsterkteY = feature["properties"]["conePenetrometerSurvey.parameters.magneticFieldStrengthY"]
        MagnetischeVeldsterkteZ = feature["properties"]["conePenetrometerSurvey.parameters.magneticFieldStrengthZ"]
        MagnetischeVeldsterkteTotaal = feature["properties"]["conePenetrometerSurvey.parameters.magneticFieldStrengthTotal"]
        MagnetischeInclinatie = feature["properties"]["conePenetrometerSurvey.parameters.magneticInclination"]
        MagnetischeDeclinatie = feature["properties"]["conePenetrometerSurvey.parameters.magneticDeclination"]
        Temperatuur = feature["properties"]["conePenetrometerSurvey.parameters.temperature"]



        # De variabel waarin alle meetwaardes opgeslagen zijn (altijd aanwezig)
        ResultatenString = feature["properties"]["conePenetrometerSurvey.conePenetrationTest.cptResult.values"]



        # Verwijderde lagen variabelen
        try:
            Volgnummer = feature["properties"]["additionalInvestigation.removedLayer.sequenceNumber"]
        except KeyError:
            Volgnummer = "onbekend"

        try:
            Bovengrens = feature["properties"]["additionalInvestigation.removedLayer.upperBoundary"]
        except KeyError:
            Bovengrens = "onbekend"

        try:
            Ondergrens = feature["properties"]["additionalInvestigation.removedLayer.lowerBoundary"]
        except KeyError:
            Ondergrens = "onbekend"

        try:
            BeschrijvingVerwijderdeLaag = feature["properties"]["additionalInvestigation.removedLayer.description"]
        except KeyError:
            BeschrijvingVerwijderdeLaag = "onbekend"

        try:
            StarttijdMeten = feature["properties"]["conePenetrometerSurvey.conePenetrationTest.phenomenonTime.TimeInstant.timePosition"]
        except KeyError:
            StarttijdMeten = "onbekend"



        # Geografische locatie variabelen (altijd aanwezig)
        Coordinaten = feature["geometry"]["coordinates"]
        Verschuiving = feature["properties"]["deliveredVerticalPosition.offset"]
        VerticaalReferentieVlak = feature["properties"]["deliveredVerticalPosition.verticalDatum"]



        # Maak lege lijsten aan om de waardes van de 25 meetvariabelen in op te slaan
        SondeertrajectlengteWaarde = []
        ConusweerstandWaarde = []
        PlaatselijkeWrijvingWaarde = []
        WrijvingsgetalWaarde = []
        WaterspanningU1Waarde = []
        WaterspanningU2Waarde = []
        WaterspanningU3Waarde = []
        HellingresultanteWaarde = []
        HellingNoordZuidWaarde = []
        HellingOostWestWaarde = []
        DiepteWaarde = []
        VerlopenTijdWaarde = []
        GecorrigeerdeConusweerstandWaarde = []
        NettoConusweerstandWaarde = []
        PorienratioWaarde = []
        HellingXWaarde = []
        HellingYWaarde = []
        ElektrischeGeleidbaarheidWaarde = []
        MagnetischeVeldsterkteXWaarde = []
        MagnetischeVeldsterkteYWaarde = []
        MagnetischeVeldsterkteZWaarde = []
        MagnetischeVeldsterkteTotaalWaarde = []
        MagnetischeInclinatieWaarde = []
        MagnetischeDeclinatieWaarde = []
        TemperatuurWaarde = []



        # Split de lijst met alle meetwaardes naar lijsten met de meetwaardes per meting en verwijder de laatste meting zonder waardes erin
        ResultatenList = ResultatenString.split(";")
        ResultatenList = ResultatenList[:-1]

        # Sorteer de metingen die bij de json naar xml conversie door de war zijn geraakt op basis van de sondeertrajectlengte
        # https://stackoverflow.com/questions/5967500/how-to-correctly-sort-a-string-with-a-number-inside
        # https://stackoverflow.com/questions/2545532/python-analog-of-natsort-function-sort-a-list-using-a-natural-order-algorithm
        ResultatenSorted = sorted(ResultatenList, key=natural_keys)



        for Measurement in ResultatenSorted:

            # De waardes per meting worden opnieuw gesplit zodat elke waarde een eigen getal is
            ResulatatenMeting = Measurement.split(",")

            # Wanneer er sprake is van meetwaardes voor een attibuut worden deze aan een nieuwe attribuut gekoppeld, anders wordt de waarde op 'onbekend' gezet
            if Sondeertrajectlengte == 'ja':
                STLW = ResulatatenMeting[0]
                SondeertrajectlengteWaarde.append(STLW)
            elif Sondeertrajectlengte == 'nee':
                STLW = "onbekend"

            if Conusweerstand == 'ja':
                CWW = ResulatatenMeting[3]
                ConusweerstandWaarde.append(CWW)
            elif Conusweerstand == 'nee':
                CWW = "onbekend"

            if PlaatselijkeWrijving == 'ja':
                PWW = ResulatatenMeting[18]
                PlaatselijkeWrijvingWaarde.append(PWW)
            elif PlaatselijkeWrijving == 'nee':
                PWW = "onbekend"

            if Wrijvingsgetal == 'ja':
                WgW = ResulatatenMeting[24]
                WrijvingsgetalWaarde.append(WgW)
            elif Wrijvingsgetal == 'nee':
                WgW = "onbekend"

            if WaterspanningU1 == 'ja':
                WsU1W = ResulatatenMeting[21]
                WaterspanningU1Waarde.append(WsU1W)
            elif WaterspanningU1 == 'nee':
                WsU1W = "onbekend"

            if WaterspanningU2 == 'ja':
                WsU2W = ResulatatenMeting[22]
                WaterspanningU2Waarde.append(WsU2W)
            elif WaterspanningU2 == 'nee':
                WsU2W = "onbekend"

            if WaterspanningU3 == 'ja':
                WsU3W = ResulatatenMeting[23]
                WaterspanningU3Waarde.append(WsU3W)
            elif WaterspanningU3 == 'nee':
                WsU3W = "onbekend"

            if Hellingresultante == 'ja':
                HrW = ResulatatenMeting[15]
                HellingresultanteWaarde.append(HrW)
            elif Hellingresultante == 'nee':
                HrW = "onbekend"

            if HellingNoordZuid == 'ja':
                HNZW = ResulatatenMeting[12]
                HellingNoordZuidWaarde.append(HNZW)
            elif HellingNoordZuid == 'nee':
                HNZW = "onbekend"

            if HellingOostWest == 'ja':
                HOWW = ResulatatenMeting[11]
                HellingOostWestWaarde.append(HOWW)
            elif HellingOostWest == 'nee':
                HOWW = "onbekend"

            if Diepte == 'ja':
                DptW = ResulatatenMeting[1]
                DiepteWaarde.append(DptW)
            elif Diepte == 'nee':
                DptW = "onbekend"

            if VerlopenTijd == 'ja':
                VTW = ResulatatenMeting[2]
                VerlopenTijdWaarde.append(VTW)
            elif VerlopenTijd == 'nee':
                VTW = "onbekend"

            if GecorrigeerdeConusweerstand == 'ja':
                GCwW = ResulatatenMeting[4]
                GecorrigeerdeConusweerstandWaarde.append(GCwW)
            elif GecorrigeerdeConusweerstand == 'nee':
                GCwW = "onbekend"

            if NettoConusweerstand == 'ja':
                NCwW = ResulatatenMeting[4]
                NettoConusweerstandWaarde.append(NCwW)
            elif NettoConusweerstand == 'nee':
                NCwW = "onbekend"

            if Porienratio == 'ja':
                PrW = ResulatatenMeting[19]
                PorienratioWaarde.append(PrW)
            elif Porienratio == 'nee':
                PrW = "onbekend"


            if HellingX == 'ja':
                HXW = ResulatatenMeting[13]
                HellingXWaarde.append(HXW)
            elif HellingX == 'nee':
                HXW = "onbekend"

            if HellingY == 'ja':
                HYW = ResulatatenMeting[14]
                HellingYWaarde.append(HYW)
            elif HellingY == 'nee':
                HYW = "onbekend"

            if ElektrischeGeleidbaarheid == 'ja':
                EGW = ResulatatenMeting[10]
                ElektrischeGeleidbaarheidWaarde.append(EGW)
            elif ElektrischeGeleidbaarheid == 'nee':
                EGW = "onbekend"

            if MagnetischeVeldsterkteX == 'ja':
                MVXW = ResulatatenMeting[6]
                MagnetischeVeldsterkteXWaarde.append(MVXW)
            elif MagnetischeVeldsterkteX == 'nee':
                MVXW = "onbekend"

            if MagnetischeVeldsterkteY == 'ja':
                MVYW = ResulatatenMeting[7]
                MagnetischeVeldsterkteYWaarde.append(MVYW)
            elif MagnetischeVeldsterkteY == 'nee':
                MVYW = "onbekend"

            if MagnetischeVeldsterkteZ == 'ja':
                MVZW = ResulatatenMeting[8]
                MagnetischeVeldsterkteZWaarde.append(MVZW)
            elif MagnetischeVeldsterkteZ == 'nee':
                MVZW = "onbekend"

            if MagnetischeVeldsterkteTotaal == 'ja':
                MVToW = ResulatatenMeting[9]
                MagnetischeVeldsterkteTotaalWaarde.append(MVToW)
            elif MagnetischeVeldsterkteTotaal == 'nee':
                MVToW = "onbekend"

            if MagnetischeInclinatie == 'ja':
                MIW = ResulatatenMeting[16]
                MagnetischeInclinatieWaarde.append(MIW)
            elif MagnetischeInclinatie == 'nee':
                MIW = "onbekend"

            if MagnetischeDeclinatie == 'ja':
                MDW = ResulatatenMeting[17]
                MagnetischeDeclinatieWaarde.append(MDW)
            elif MagnetischeDeclinatie == 'nee':
                MDW = "onbekend"

            if Temperatuur == 'ja':
                TmpW = ResulatatenMeting[20]
                TemperatuurWaarde.append(TmpW)
            elif Temperatuur == 'nee':
                TmpW = "onbekend"



        # Zet de lijsten met string waardes om naar een lijst met float waardes als de ja-nee variabel met ja is beantwoord, anders wordt deze stap overgeslagen
        if Sondeertrajectlengte == 'ja':
            try:
                STLW = [float(i) for i in SondeertrajectlengteWaarde]
            except ValueError:
                pass

        if Conusweerstand == 'ja':
            try:
                CWW = [float(i) for i in ConusweerstandWaarde]
            except ValueError:
                pass

        if PlaatselijkeWrijving == 'ja':
            try:
                PWW = [float(i) for i in PlaatselijkeWrijvingWaarde]
            except ValueError:
                pass

        if Wrijvingsgetal == 'ja':
            try:
                WgW = [float(i) for i in WrijvingsgetalWaarde]
            except ValueError:
                pass

        if WaterspanningU1 == 'ja':
            try:
                WsU1W = [float(i) for i in WaterspanningU1Waarde]
            except ValueError:
                pass

        if WaterspanningU2 == 'ja':
            try:
                WsU2W = [float(i) for i in WaterspanningU2Waarde]
            except ValueError:
                pass

        if WaterspanningU3 == 'ja':
            try:
                WsU3W = [float(i) for i in WaterspanningU3Waarde]
            except ValueError:
                pass

        if Hellingresultante == 'ja':
            try:
                HrW = [float(i) for i in HellingresultanteWaarde]
            except ValueError:
                pass

        if HellingNoordZuid == 'ja':
            try:
                HNZW = [float(i) for i in HellingNoordZuidWaarde]
            except ValueError:
                pass

        if HellingOostWest == 'ja':
            try:
                HOWW = [float(i) for i in HellingOostWestWaarde]
            except ValueError:
                pass

        if Diepte == 'ja':
            try:
                DptW = [float(i) for i in DiepteWaarde]
            except ValueError:
                pass

        if VerlopenTijd == 'ja':
            try:
                VTW = [float(i) for i in VerlopenTijdWaarde]
            except ValueError:
                pass

        if GecorrigeerdeConusweerstand == 'ja':
            try:
                GCwW = [float(i) for i in GecorrigeerdeConusweerstandWaarde]
            except ValueError:
                pass

        if NettoConusweerstand == 'ja':
            try:
                NCwW = [float(i) for i in NettoConusweerstandWaarde]
            except ValueError:
                pass

        if Porienratio == 'ja':
            try:
                PrW = [float(i) for i in PorienratioWaarde]
            except ValueError:
                pass
                print PrW

        if HellingX == 'ja':
            try:
                HXW = [float(i) for i in HellingXWaarde]
            except ValueError:
                pass

        if HellingY == 'ja':
            try:
                HYW = [float(i) for i in HellingYWaarde]
            except ValueError:
                pass

        if ElektrischeGeleidbaarheid == 'ja':
            try:
                EGW = [float(i) for i in ElektrischeGeleidbaarheidWaarde]
            except ValueError:
                pass

        if MagnetischeVeldsterkteX == 'ja':
            try:
                MVXW = [float(i) for i in MagnetischeVeldsterkteXWaarde]
            except ValueError:
                pass

        if MagnetischeVeldsterkteY == 'ja':
            try:
                MVYW = [float(i) for i in MagnetischeVeldsterkteYWaarde]
            except ValueError:
                pass

        if MagnetischeVeldsterkteZ == 'ja':
            try:
                MVZW = [float(i) for i in MagnetischeVeldsterkteZWaarde]
            except ValueError:
                pass

        if MagnetischeVeldsterkteTotaal == 'ja':
            try:
                MVToW = [float(i) for i in MagnetischeVeldsterkteTotaalWaarde]
            except ValueError:
                pass

        if MagnetischeInclinatie == 'ja':
            try:
                MIW = [float(i) for i in MagnetischeInclinatieWaarde]
            except ValueError:
                pass

        if MagnetischeDeclinatie == 'ja':
            try:
                MDW = [float(i) for i in MagnetischeDeclinatieWaarde]
            except ValueError:
                pass

        if Temperatuur == 'ja':
            try:
                TmpW = [float(i) for i in TemperatuurWaarde]
            except ValueError:
                pass



        # Voeg de waardes van de variabelen toe aan de lege features lijst
        features.append([BroID, UitvoerderOnderzoek, KwaliteitsRegime, Conustype, OmschrijvingConustype, Sondeernorm, Kwaliteitsklasse, LokaalVerticaalReferentiepunt, Omstandigheden, SignaalbewerkingUitgevoerd,
        BewerkingOnderbrekingenUitgevoerd, MethodeVerticalePositiebepaling, MethodeLocatiebepaling, Bronhouder, KaderAanlevering, KaderInwinning, UitvoerderLocatiebepaling, DatumLocatiebepaling, UitvoerderVerticalePositiebepaling,
        DatumVerticalePositiebepaling, HoedanigheidOppervlakte, DissipatietestUitgevoerd, ExpertcorrectieUitgevoerd, AanvullendOnderzoekUitgevoerd, RapportagedatumOnderzoek, DatumLaatsteBewerking, DatumOnderzoek,
        ObjectIDBronhouder, OppervlakteConuspunt, OppervlakteKleefmantel, OppervlaktequotientConuspunt, OppervlaktequotientKleefmantel, AfstandConusTotMiddenKleefmantel, Sondeermethode, VoorgeboordTot, Grondwaterstand,
        Waterdiepte, Einddiepte, Stopcriterium, ConusweerstandVooraf, ConusweerstandAchteraf, PlaatselijkeWrijvingVooraf, PlaatselijkeWrijvingAchteraf, WaterspanningU1Vooraf, WaterspanningU1Achteraf, WaterspanningU2Vooraf,
        WaterspanningU2Achteraf, WaterspanningU3Vooraf, WaterspanningU3Achteraf, HellingresultanteVooraf, HellingresultanteAchteraf, HellingNoordZuidVooraf, HellingNoordZuidAchteraf, HellingOostWestVooraf, HellingOostWestAchteraf,
        ElektrischeGeleidbaarheidVooraf, ElektrischeGeleidbaarheidAchteraf, SensorAzimuth, Conusdiameter, Sondeertrajectlengte, Conusweerstand, PlaatselijkeWrijving, Wrijvingsgetal, WaterspanningU1, WaterspanningU2, WaterspanningU3,
        Hellingresultante, HellingNoordZuid, HellingOostWest, Diepte, VerlopenTijd, GecorrigeerdeConusweerstand, NettoConusweerstand, Porienratio, HellingX, HellingY, ElektrischeGeleidbaarheid, MagnetischeVeldsterkteX,
        MagnetischeVeldsterkteY, MagnetischeVeldsterkteZ, MagnetischeVeldsterkteTotaal, MagnetischeInclinatie, MagnetischeDeclinatie, Temperatuur, Volgnummer, Bovengrens, Ondergrens, BeschrijvingVerwijderdeLaag, StarttijdMeten,
        Coordinaten, Referentiestelsel, Verschuiving, VerticaalReferentieVlak, STLW, CWW, PWW, WgW, WsU1W, WsU2W, WsU3W, HrW, HNZW, HOWW, DptW, VTW, GCwW, NCwW, PrW, HXW, HYW, EGW, MVXW, MVYW, MVZW, MVToW, MIW, MDW, TmpW])

        # Een lijst wordt gemaakt met de attribuut namen zoals ze uiteindelijk in het geojson bestand gaan staan
        attributeNames = ['BroID', 'UitvoerderOnderzoek', 'KwaliteitsRegime', 'Conustype', 'OmschrijvingConustype', 'Sondeernorm', 'Kwaliteitsklasse', 'LokaalVerticaalReferentiepunt', 'Omstandigheden', 'SignaalbewerkingUitgevoerd',
        'BewerkingOnderbrekingenUitgevoerd', 'MethodeVerticalePositiebepaling', 'MethodeLocatiebepaling', 'Bronhouder', 'KaderAanlevering', 'KaderInwinning', 'UitvoerderLocatiebepaling', 'DatumLocatiebepaling',
        'UitvoerderVerticalePositiebepaling', 'DatumVerticalePositiebepaling', 'HoedanigheidOppervlakte', 'DissipatietestUitgevoerd', 'ExpertcorrectieUitgevoerd', 'AanvullendOnderzoekUitgevoerd', 'RapportagedatumOnderzoek',
        'DatumLaatsteBewerking', 'DatumOnderzoek', 'ObjectIDBronhouder', 'OppervlakteConuspunt', 'OppervlakteKleefmantel', 'OppervlaktequotientConuspunt', 'OppervlaktequotientKleefmantel', 'AfstandConusTotMiddenKleefmantel',
        'Sondeermethode', 'VoorgeboordTot', 'Grondwaterstand', 'Waterdiepte', 'Einddiepte', 'Stopcriterium', 'ConusweerstandVooraf', 'ConusweerstandAchteraf', 'PlaatselijkeWrijvingVooraf', 'PlaatselijkeWrijvingAchteraf',
        'WaterspanningU1Vooraf', 'WaterspanningU1Achteraf', 'WaterspanningU2Vooraf', 'WaterspanningU2Achteraf', 'WaterspanningU3Vooraf', 'WaterspanningU3Achteraf', 'HellingresultanteVooraf', 'HellingresultanteAchteraf',
        'HellingNoordZuidVooraf', 'HellingNoordZuidAchteraf', 'HellingOostWestVooraf', 'HellingOostWestAchteraf', 'ElektrischeGeleidbaarheidVooraf', 'ElektrischeGeleidbaarheidAchteraf', 'SensorAzimuth', 'Conusdiameter',
        'Sondeertrajectlengte', 'Conusweerstand', 'PlaatselijkeWrijving', 'Wrijvingsgetal', 'WaterspanningU1', 'WaterspanningU2', 'WaterspanningU3', 'Hellingresultante', 'HellingNoordZuid', 'HellingOostWest', 'Diepte', 'VerlopenTijd',
        'GecorrigeerdeConusweerstand', 'NettoConusweerstand', 'Porienratio', 'HellingX', 'HellingY', 'ElektrischeGeleidbaarheid', 'MagnetischeVeldsterkteX', 'MagnetischeVeldsterkteY', 'MagnetischeVeldsterkteZ',
        'MagnetischeVeldsterkteTotaal', 'MagnetischeInclinatie', 'MagnetischeDeclinatie', 'Temperatuur', 'Volgnummer', 'Bovengrens', 'Ondergrens', 'BeschrijvingVerwijderdeLaag', 'StarttijdMeten', 'Coordinaten', 'Referentiestelsel',
        'Verschuiving', 'VerticaalReferentieVlak', 'SondeertrajectlengteWaarde', 'ConusweerstandWaarde', 'PlaatselijkeWrijvingWaarde', 'WrijvingsgetalWaarde', 'WaterspanningU1Waarde', 'WaterspanningU2Waarde', 'WaterspanningU3Waarde',
        'HellingresultanteWaarde', 'HellingNoordZuidWaarde', 'HellingOostWestWaarde', 'DiepteWaarde', 'VerlopenTijdWaarde', 'GecorrigeerdeConusweerstandWaarde', 'NettoConusweerstandWaarde', 'PorienratioWaarde', 'HellingXWaarde',
        'HellingYWaarde', 'ElektrischeGeleidbaarheidWaarde', 'MagnetischeVeldsterkteXWaarde', 'MagnetischeVeldsterkteYWaarde', 'MagnetischeVeldsterkteZWaarde', 'MagnetischeVeldsterkteTotaalWaarde', 'MagnetischeInclinatieWaarde',
        'MagnetischeDeclinatieWaarde', 'TemperatuurWaarde']

        # De attribuut namen en waardes worden aan elkaar gekoppeld, waarvoor de twee lijsten in dezelfde volgorde moeten staan
        newFeatures = features[number]
        new = map(lambda x,y:(x,y),attributeNames,newFeatures)
        #pprint.pprint(new)

        # De namen en waardes worden in een georderde dictionairy gestopt om een geldige json structuur te krijgen
        # https://stackoverflow.com/questions/1867861/dictionaries-how-to-keep-keys-values-in-same-order-as-declared
        alleBoringen = OrderedDict(new)

        # De georderde dictionary van de feature wordt toegevoegd aan de lijst voor alle features
        objects.append(alleBoringen)

        # Er wordt geschakeld naar de volgende feature door het nummer plus 1 te zetten elke loop
        print number
        number += 1



    # Alle data wordt in een nieuw geojson bestand gedumpt en is zo te gebruiken in andere software
    with open(outputPoints, 'w') as outfile:
        #json.dump([{"Naam": x[0], "Waarde": x[1]} for x in new], outfile, indent=2)
        json.dump(objects, outfile, indent=2)




"""
Een definitie waarmee de workspace die geojson geometrie aan het json bestand toevoegd wordt gerunned

def JSONtoGeoJSON():
"""



"""
De systeempaden naar de inputs en outputs voor het script worden gegeven en het script wordt uitgevoerd
"""
inputPoints = "C:/Users/NLsgro/Documents/Internship/InternshipData/brogeotechnischsondeeronderzoek/sample.geojson"
outputPoints = "C:/Users/NLsgro/Documents/Internship/InternshipData/brogeotechnischsondeeronderzoek/processed_IMBRO_sample.geojson"
outputJSON = "C:/Users/NLsgro/Documents/Internship/InternshipData/brogeotechnischsondeeronderzoek/bro_xml_json_test2.json"
RestructuringJSON(inputPoints, outputPoints)





#JsonToPandas(outputPoints, outputJSON)



def JsonToPandas(outputPoints, outputJSON):
    df = pandas.read_json(outputPoints, orient="records", typ="frame")
    print df
    df2 = pandas.DataFrame.to_json(df, orient="split", index=False)
    pprint.pprint(df2)
    with open(outputJSON, 'w') as outfile:
        json.dump(df2, outfile)