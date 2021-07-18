from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import os




drugs=['bepridil', 'chlorpromazine', 'cisapride', 'diltiazem', 'dofetilide', 'mexiletine', 'ondansetron', 'quinidine',
       'ranolazine', 'sotalol', 'terfenadine', 'verapamil'] # list of drugs to be iterated through
doses=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25]

# if true, output from the normal CiPA model including the model for dynamic hERG is used. If false, output from cipa
# model without the dynamic hERG model is used
with_dynhERG = True

# to use data from Crumb et al use 'with_Crumb_parameters', to use data outputs that match the default CiPA input,
# use 'with_CiPA_parameters'
dataset='with_Crumb_parameters'

# denotes the variance of the population of the Virtual ASsay output to be plotted. Can be '+-50%', '+-30%' or '+-5%'
va_population = '+-50%'

# Relevant biomarkers: 'APD90' or 'qNet'
biomarker = 'qNet'

plot_path = os.getcwd()+'/../plots' # datapath for plots
metrics_path = os.getcwd()+'/../metrics' # datapath for metrics

#load correct  metrics file
va_metrics = pd.read_csv(metrics_path+'/va/'+dataset+'/va'+va_population+'_population_'+dataset+'.csv')
cipa_metrics = pd.read_csv(metrics_path+'/cipa/cipa_metrics.csv')

# rename va biomarkers to match cipa
va_metrics = va_metrics.rename(columns={'APD1':'APD90'})
# adjust qNet values to match
cipa_metrics['qNet'] = cipa_metrics['qNet']/1000
# remove empty values (NA) from cipa
cipa_metrics.dropna(subset = [biomarker], inplace=True)

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
    plt.title(va_population+' population, '+ biomarker+', '+drug)

    plt.xticks(range(0, len(doses) * 2, 2), doses)
    plt.xlim(-2, len(doses)*2)

    plt.tight_layout()

    if with_dynhERG:
        plt.savefig(plot_path+'/cipa_dynHerg/'+dataset+'/'+va_population+'/'+biomarker+'/'+va_population+'_'+drug+'_'+biomarker)
    else:
        plt.savefig(plot_path+'/cipa_no_dynHerg/'+dataset+'/'+va_population+'/'+biomarker+'/'+va_population+'_'+drug+'_'+biomarker)

