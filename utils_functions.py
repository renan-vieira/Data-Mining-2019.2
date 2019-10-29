#===============================================
# PROJETO MINERACAO DE DADOS
# funcoes para preprocessamento e visualizacao
#
# @claudioalvesmonteiro
#===============================================

# funcao para gerar dummies com base em threshold
def categoryToDummyThreshold(dataframe, data, column, threshold):
    import pandas as pd
    # capturar distribuicao da CID
    cont = count_porcent(data, column)
    # combinar com base de ambulatorio
    data = data.merge(cont, on=column)
    # criar coluna CID > 1%
    data[('SIG_'+column)] = [data[column][x] if data['porcent'][x] >= threshold else 'OUTROS' for x in range(len(data))]
    # selecionar casos unicos do cod integracao e cid
    uni = data[['Cod Integração', ('SIG_'+column)]].drop_duplicates()
    # combinar com base alvo
    dataframe = dataframe.merge(uni, on='Cod Integração', how='left')
    # criar variaveis dummy para CID > %1 e combinar com a base
    dummies = pd.get_dummies(dataframe[('SIG_'+column)], prefix=column)
    dataframe = pd.concat([dataframe, dummies], axis=1)
    return dataframe

# funcao para identificar casos de unidade UTI
def findUTI(coluna):
    internado_uti = []
    utis = ['UTI PED A', 'UTI PED B', 'UTI NEONATAL', 'UTD']
    for unidade in coluna:
            if unidade in utis:
                internado_uti.append(1)
            else:
                internado_uti.append(0)
    return internado_uti


# criar faixa etaria [1: 0-1, 2:2-10, 3:11-15, 4:15>]
def createFaixa(coluna):
    import numpy as np
    faixa=[]
    for x in coluna:
        if x <= 1:
            faixa.append(1)
        elif x > 1 and x <= 10:
            faixa.append(2)
        elif x > 10 and x <= 15:
            faixa.append(3)
        elif x > 15:
            faixa.append(4)
        else:
            faixa.append(np.nan)
            print('FOUND NULL IDADE') 
    return faixa

# funcao para visualizar distribuicao de colunas categoricas
def count_porcent(data, colnome, save=False):
    import pandas as pd
    # agrupar por contagem (tamanho)
    agg = data[[colnome]].groupby(colnome).size()
    # transformar em dataframe
    agg = pd.DataFrame(agg)
    # tranformar index em coluna 
    agg.reset_index(inplace=True)
    # renomear colunas
    agg.columns = [colnome, 'contagem']
    # calcular porcentagem do total pra cada categoria
    agg['porcent'] = agg['contagem'] / sum(agg['contagem'])*100 
    # ordenar
    agg.sort_values('porcent', inplace=True)
    if save == True:
        agg.to_csv('data/tables/'+colnome+'_TABLE.csv', index=False)
    # retornar base final
    return agg


def contaAlvoPorcent(data, colnome, save=False):
    import pandas as pd
    # agrupar por contagem (tamanho)
    agg = data[[colnome, 'ALVO']].groupby([colnome,'ALVO']).size()
    # transformar em dataframe
    agg = pd.DataFrame(agg)
    # tranformar index em coluna 
    agg.reset_index(inplace=True)
    # renomear colunas
    agg.columns = [colnome, 'Alvo', 'contagem']
    # calcular porcentagem do total pra cada categoria
    agg['porcent'] = round( agg['contagem'] / sum(agg['contagem'])*100,2 )
    if save == True:
        agg.to_csv('data/tables/alvo_'+colnome+'_TABLE.csv', index=False)
    # retornar base final
    return agg