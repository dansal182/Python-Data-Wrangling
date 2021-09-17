import numpy as np
import pandas as pd


def getClvUni(row):
    states = ['AGS', 'BJN', 'BJS', 'CAM', 'CHP', 'CHI', 'CMX',
              'COA', 'COL', 'DUR', 'GUA', 'GUE', 'HID', 'JAL', 'EMX', 'MIC', 'MOR', 'NAY', 'NLN', 'OAX',
              'PUE', 'QUE', 'QRO', 'SLP', 'SIN', 'SON', 'TAB', 'TAM', 'TLX', 'VER',
              'YUC', 'ZAC']

    aux = diputados.iloc[row][1]
    if not type(aux) == int:
        aux = int(aux)
    tag = states[(aux - 1)]

    if aux < 10:
        ent = "0" + str(aux)
    else:
        ent = str(aux)

    aux = diputados.iloc[row][7]
    if not type(aux) == int:
        aux = int(aux)

    if aux < 10:
        sec = "00" + str(aux)
    elif aux < 100:
        sec = "0" + str(aux)
    else:
        sec = str(aux)

    return ent + sec + tag


def fillClvUni(clvD, size):
    for i in range(0, size):
        clvD.loc[i, 'ClvSecc'] = getClvUni(i)
        if i in [1000, 10000, 20000, 40000, 60000]:
            print('done: ' + str(i))
    print('ready fready')


def conClv(clvD, dipD):
    votBas = dipD.copy()
    votBas['ClvSecc'] = clvD['ClvSecc']
    return votBas


def sumVotos(clvD, dipD):
    votBas = conClv(clvD, dipD)
    votG = pd.DataFrame(votBas.groupby('ClvSecc')[['PAN', 'PRI', 'PRD', 'PC', 'PT', 'PVEM', 'PPS', 'PDM']].sum())
    votG['ClvSecc'] = votG.index
    votG['Ind'] = np.arange(len(votG))
    votG = votG.set_index('Ind')
    return votG


def wonSec(votG, row):
    aux = votG.loc[row, ['PAN', 'PRI', 'PRD', 'PC', 'PT', 'PVEM', 'PPS', 'PDM']].max()
    if aux == votG['PAN'].iloc[row]:
        return 'PAN'
    elif aux == votG['PRI'].iloc[row]:
        return 'PRI'
    elif aux == votG['PRD'].iloc[row]:
        return 'PRD'
    elif aux == votG['PC'].iloc[row]:
        return 'PC'
    elif aux == votG['PT'].iloc[row]:
        return 'PT'
    elif aux == votG['PVEM'].iloc[row]:
        return 'PVEM'
    elif aux == votG['PPS'].iloc[row]:
        return 'PPD'
    # elif aux == votG['MORENA_15'].iloc[row]:
    #    return 'MORENA'
    # elif aux == votG['PARTIDO_HUMANISTA_15'].iloc[row]:
    #    return 'PARTIDO_HUMANISTA'
    # elif aux == votG['ENCUENTRO_SOCIAL_15'].iloc[row]:
    #    return 'ENCUENTRO_SOCIAL_15'
    # elif aux == votG['PRI_PVEM_15'].iloc[row]:
    #    return 'PRI_PVEM'
    # elif aux == votG['PRD_PT_15'].iloc[row]:
    #    return 'PRD_PT'
    # elif aux == votG['CAND_IND_1_15'].iloc[row]:
    #    return 'CAND_IND_1'
    # elif aux ==votG['CAND_IND_2_15'].iloc[row]:
    #    return 'CAND_IND_2'
    # elif aux ==votG['NO_REGISTRADOS_15'].iloc[row]:
    #    return 'NO_REGISTRADOS'
    else:
        return 'PDM'


def fillwon(votG):
    votF = votG.copy()
    votF['Gano'] = str(np.arange(len(votG)))
    votF['Total'] = np.arange(len(votG))
    for i in range(0, len(votG)):
        votF.loc[i, 'Gano'] = wonSec(votG, i)
        votF.loc[i, 'Total'] = votG.loc[i, ['PAN', 'PRI', 'PRD', 'PC', 'PT', 'PVEM', 'PPS', 'PDM']].sum()
        if i in [1000, 10000, 20000, 30000, 40000, 50000, 60000]:
            print('done: ' + str(i))
    print('ready fready')
    return votF

def savefile(filetosave, name):
    path = '/Users/danielsalnikov/Documents/Ejidos/elecciones/bases_finales/' + name + ".csv"
    filetosave.to_csv(path, index=False)


path = '/Users/danielsalnikov/Documents/Ejidos/elecciones/elecciones_nacional/computos_elecciones/1997' \
       '/1997_SEE_DIP_FED_MR_NAL_CAS.csv'

diputados = pd.read_csv(path)

secc = pd.read_csv('/Users/danielsalnikov/Documents/Ejidos/elecciones/elecciones_nacional/computos_elecciones'
                   '/secc_ejidos.csv')
print(diputados.head(2))
#diputados = diputados[diputados['ID_ESTADO_15'] !='.']
#print(len(diputados))
#diputados = diputados.apply(pd.to_numeric)
clv = pd.DataFrame()
clv['ClvSecc'] = np.arange(len(diputados))
fillClvUni(clv, len(diputados))
basura = conClv(clv, diputados)
print(len(basura))
print(basura.head(10))

vot97 = sumVotos(clv, diputados)
print(vot97.head(5))
print(len(vot97))
vot97f = fillwon(vot97)
print(vot97f.head(5))
savefile(vot97f, 'vot97final')
secc97 = pd.merge(secc, vot97f, on='ClvSecc', how='left')
savefile(secc97, 'secciones97')