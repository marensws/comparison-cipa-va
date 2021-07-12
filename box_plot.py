from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import os

data_path='/Users/sofiestubo/Documents/CS/MSc/project/data_convertion/va_data-main'
print(data_path)
drugs=['bepridil', 'chlorpromazine', 'cisapride', 'diltiazem', 'dofetilide', 'mexiletine', 'ondansetron', 'quinidine',
       'ranolazine', 'sotalol', 'terfenadine', 'verapamil']
doses=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25]

# prepares data by producing by creating two dataframes with the same columns
va_population = '95-105%'
biomarker = 'qNet'

#load correct metrics file
if va_population == '50-150%':
    va_metrics = pd.read_csv(data_path+'/va_metrics-50-150.csv')
elif va_population == '70-130%':
    va_metrics = pd.read_csv(data_path+'/va_metrics-70-130.csv')
elif va_population == '95-105%':
    va_metrics = pd.read_csv(data_path+'/va_metrics-95-105.csv')

cipa_metrics = pd.read_csv(data_path+'/cipa_metrics.csv')

# rename va biomarkers to match cipa
va_metrics = va_metrics.rename(columns={'APD1':'APD90'})
# adjust qNet values to match
cipa_metrics['qNet'] = cipa_metrics['qNet']/1000

# go through each drug and make a boxplot
for drug in drugs:
    va_data=[]
    cipa_data=[]
    # for each dose, append biomarker data to a list
    for dose in doses:
        va_data.append(va_metrics[(va_metrics.dose == dose) & (va_metrics.drug == drug)][biomarker])
        cipa_data.append(cipa_metrics[(cipa_metrics.dose == dose) & (cipa_metrics.drug == drug)][biomarker])

    # create boxplot
    def set_box_color(bp, color):
        colors = [color]
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
        plt.setp(bp['boxes'], color=color)
        plt.setp(bp['whiskers'], color=color)
        plt.setp(bp['caps'], color=color)
        plt.setp(bp['medians'], color='black')


    plt.figure()
    bpl = plt.boxplot(va_data, positions=np.array(range(len(va_data))) * 2.0 - 0.38,sym='', widths=0.6, patch_artist=True)
    bpr = plt.boxplot(cipa_data, positions=np.array(range(len(cipa_data))) * 2.0 + 0.38, sym='', widths=0.6, patch_artist=True)
    set_box_color(bpl, '#D7191C') # colors are from http://colorbrewer2.org/
    set_box_color(bpr, '#2C7BB6')

    plt.plot([], c='#D7191C', label='Virtual Assay')
    plt.plot([], c='#2C7BB6', label='CiPA')
    plt.legend()
    plt.title(drug)

    plt.xticks(range(0, len(doses) * 2, 2), doses)
    plt.xlim(-2, len(doses)*2)

    plt.tight_layout()

    plt.savefig(os.getcwd()+'/'+va_population+'/'+biomarker+'/'+va_population+'_'+drug+'_'+biomarker)
