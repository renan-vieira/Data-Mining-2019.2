#=========================================
# PROJETO MINERACAO DE DADOS
# feature engineering
#
# @claudioalvesmonteiro
#=========================================

# import packages
import pandas as pd
from utils_functions import count_porcent, createFaixa, findUTI, categoryToDummyThreshold
import numpy as np

# importar dados
arq = pd.ExcelFile('data/raw_data_v0.xlsx')
cadastro = arq.parse(0)
internacao = arq.parse(1)
amb = arq.parse(2)

#==================================
# TRATAMENTO E FEATURE ENGINEERING
#==================================

#================ CADASTRO ===============#

#------------ passar codigo para string
amb['Cod Integração'] = [str(x) for x in amb['Cod Integração']]
cadastro['Cod Integração'] = [str(x) for x in cadastro['Cod Integração']]

internacao.dropna(subset=['Cod Integração'], inplace=True)
internacao['Cod Integração'] = [str(int(x)) for x in internacao['Cod Integração']]

#------------ cidade salvador
cadastro['bairro_centro'] = [1 if x == 'CENTRO' or x == 'CENTRO\r\n' else 0 for x in cadastro['Bairro']] 
cadastro['bairro_zona_rural'] = [1 if x == 'ZONA RURAL' or x == 'ZONA RURAL\r\n' else 0 for x in cadastro['Bairro']] 

#------------ bairro [centro e zona rural]
cadastro['cidade_salvador'] = [1 if x == 'SALVADOR' else 0 for x in cadastro['Cidade']] 

#------------ sexo
cadastro['sexo_feminino'] = [1 if x == 'F' else 0 for x in cadastro['Sexo']] 

#------------ idade
cadastro['faixa_etaria'] = createFaixa(cadastro['Idade'])

#------------ altura [faltante]
cadastro['altura_faltante'] = [1 if pd.isnull(x) else 0 for x in cadastro['Altura']] 

#------------ peso

# capturar peso por faixa etaria X sexo
media_peso = cadastro[['Peso', 'faixa_etaria', 'Sexo']].groupby(['Sexo', 'faixa_etaria']).median()
media_peso.columns = ['peso_faixa']
media_peso.reset_index(inplace=True)

# combinar com base de cadastro
cadastro = cadastro.merge(media_peso, on =['Sexo', 'faixa_etaria'])

# inputacao nos pesos faltantes
cadastro['peso'] = [cadastro['peso_faixa'][i] if pd.isnull(cadastro['Peso'][i]) else cadastro['Peso'][i] for i in range(len(cadastro))]

#================ AMBULATORIO ===============#

#------------ filtrar casos repetidos de procedimentos no ambulatorio
amb = amb.drop_duplicates(['Cod Integração', 'PROCEDIMENTO_COD'])

#------------ numero procedimentos por paciente

# contabilizar procedimentos e renomear colunas
qpro = count_porcent(amb[['Cod Integração', 'PROCEDIMENTO_COD']], 'Cod Integração').drop('porcent', axis=1)
qpro.columns = ['Cod Integração', 'numero_procedimentos']

# combinar com dados de cadastro [FILTRA CASOS QUE FORAM PARA AMBULATORIO]
cadastro = cadastro.merge(qpro, on='Cod Integração')

#------------ diagnosticos do ambulatorio

# aplicar funcao para gerar dummies > 1% de representatividade na base
cadastro = categoryToDummyThreshold(cadastro, amb, 'CID', 1)

#------------ procedimentos do ambulatorio

# aplicar funcao para gerar dummies > 1% de representatividade na base
cadastro = categoryToDummyThreshold(cadastro, amb, 'PROCEDIMENTO_COD', 1)

# remover pacientes duplicados [gerado em casos de multiplos valores de procedimentos para o mesmo paciente]
cadastro = cadastro.drop_duplicates('Cod Integração')

#================ INTERNACAO ===============#

#------------ alvo [1 se internado na UTI, 0 caso contrario] [tabela internacao]

# capturar unidades pela qual o paciente passou
internacao_uti = pd.DataFrame(internacao[['Cod Integração', 'Unidade']].groupby(['Cod Integração', 'Unidade']).size())            
internacao_uti.reset_index(inplace=True)

# fitrar unidade de UTI
internacao_uti['UTI'] = findUTI(internacao_uti['Unidade'])
internacao_uti = internacao_uti[internacao_uti['UTI'] == 1]

# remover duplicados e selecionar colunas
internacao_uti.drop_duplicates('Cod Integração', inplace=True)
internacao_uti.drop(['Unidade', 0], axis=1, inplace=True)

# combinar com base de cadastro
dataset = cadastro.merge(internacao_uti, on='Cod Integração', how='left')

# atribuir 0 a nulos no ALVO
dataset['UTI'] = [0 if pd.isnull(x) else x for x in dataset['UTI'] ]

#===========================
# EXPORTAR DADOS
#===========================

#------------ selecionar colunas
dataset = dataset[['UTI','Cod Integração', 'Idade', 
       'bairro_centro', 'bairro_zona_rural',
       'cidade_salvador', 'sexo_feminino', 'faixa_etaria', 'altura_faltante',
       'peso_faixa', 'peso', 'numero_procedimentos', 'SIG_CID', 'CID_C64',
       'CID_C710', 'CID_C830', 'CID_C910', 'CID_C920', 'CID_D613', 'CID_G409',
       'CID_I500', 'CID_J158', 'CID_J159', 'CID_J189', 'CID_N00', 'CID_N048',
       'CID_OUTROS', 'CID_Q210', 'CID_Q211', 'CID_Q213', 'CID_Z001',
       'SIG_PROCEDIMENTO_COD', 'PROCEDIMENTO_COD_11112050',
       'PROCEDIMENTO_COD_11112190', 'PROCEDIMENTO_COD_13051032',
       'PROCEDIMENTO_COD_13051040', 'PROCEDIMENTO_COD_1358',
       'PROCEDIMENTO_COD_1701001S', 'PROCEDIMENTO_COD_17011043',
       'PROCEDIMENTO_COD_17016045', 'PROCEDIMENTO_COD_17018030',
       'PROCEDIMENTO_COD_17023041', 'PROCEDIMENTO_COD_17034035',
       'PROCEDIMENTO_COD_17039045', 'PROCEDIMENTO_COD_17049040',
       'PROCEDIMENTO_COD_17055040', 'PROCEDIMENTO_COD_17056047',
       'PROCEDIMENTO_COD_17059046', 'PROCEDIMENTO_COD_17064040',
       'PROCEDIMENTO_COD_20202014', 'PROCEDIMENTO_COD_20203008',
       'PROCEDIMENTO_COD_28011376', 'PROCEDIMENTO_COD_6067',
       'PROCEDIMENTO_COD_CONMAERE', 'PROCEDIMENTO_COD_OUTROS',
       'PROCEDIMENTO_COD_S255', 'PROCEDIMENTO_COD_S571',
       'PROCEDIMENTO_COD_SADT', 'PROCEDIMENTO_COD_SH', 'PROCEDIMENTO_COD_SP']]

#------------ salvar base
dataset.to_csv('data/preprocessed_data.csv', index=False)

print('\nDados salvos com as seguintes features:', dataset.columns)