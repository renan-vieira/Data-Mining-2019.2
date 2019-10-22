import pandas as pd

# TODO: clean all prints and auxiliary variables after group consolidation of numbers

file = pd.ExcelFile('data/raw_data.xlsx')
patient_sheet = file.parse(0)
internees_sheet = file.parse(1)
ambulatory_sheet = file.parse(2)

registered_ids = list(patient_sheet['Cod Integração'].unique())
assert (len(registered_ids) == 6265)
ambulatory_ids = list(ambulatory_sheet['Cod Integração'].unique())
print(f'len(ambulatory_ids)= {len(ambulatory_ids)}')
internee_ids = list(internees_sheet['Cod Integração'].unique())
print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
print(f'len(internee_ids)= {len(internee_ids)}')

aux_df = internees_sheet[internees_sheet['UTI=1'] == 1]
print('@@@@@@@@@@@@@@@@@@@@@@@@')
print(len(aux_df['Cod Integração'].unique()))
aux_df = aux_df[aux_df['Cod Integração'].isin(ambulatory_ids)]
aux_list = list(aux_df['Cod Integração'].unique())
print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
print(f'len(aux_list)= {len(aux_list)}')
internees_sheet = internees_sheet[internees_sheet['Cod Integração'].isin(ambulatory_ids)]
internees_were_on_ambulatory_ids = list(internees_sheet["Cod Integração"].unique())
print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
print(f'len(internees_were_on_ambulatory_ids)= {len(internees_were_on_ambulatory_ids)}')

ambulatory_sheet = ambulatory_sheet[ambulatory_sheet['Cod Integração'].isin(internee_ids)]
ambulatory_and_internee_ids = list(ambulatory_sheet['Cod Integração'].unique())
print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
print(f'len(ambulatory_and_internee_ids)= {len(ambulatory_and_internee_ids)}')
patient_sheet = patient_sheet[patient_sheet['Cod Integração'].isin(ambulatory_and_internee_ids)]
print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
patient_sheet.info()

with pd.ExcelWriter('data/filtered_data.xlsx') as wrt:
    patient_sheet.to_excel(wrt, 'Cadastro')
    ambulatory_sheet.to_excel(wrt, 'Ambulatorio')
    internees_sheet.to_excel(wrt, 'Internacao')

    wrt.save()
