#===============================================
# PROJETO MINERACAO DE DADOS
# analise exploratoria e visualizacao de dados
#
# @claudioalvesmonteiro
#===============================================

# importar pacotes
import pandas as pd

# importar dados
data = pd.read_csv('data/preprocessed_data.csv')
arq = pd.ExcelFile('data/raw_data.xlsx')
amb = arq.parse(2)

#==================================
# gerar tabelas para visualizacao
#==================================

# funcao para visualizar distribuicao de colunas categoricas
def contaePorcent(data, colnome, save=False):
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


contaePorcent(data, 'CID_sig', save=True)
contaePorcent(data, 'Sexo',  save=True)
contaePorcent(data, 'Estado',  save=True)
contaePorcent(data, 'Bairro',  save=True)
contaePorcent(data, 'Cidade',  save=True)
contaePorcent(data, 'Idade',  save=True)

contaePorcent(amb, 'PROCEDIMENTO',  save=True)

def contaAlvoPorcent(data, colnome, save=False):
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


contaAlvoPorcent(data, 'Sexo',  save=True)

