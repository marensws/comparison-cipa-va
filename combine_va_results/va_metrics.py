import os
# extracts the dose of a va output file based on title
def get_dose(file_name):
    doses=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25]
    file_number = int(file_name.split(sep='_')[7]) % 13
    return doses[file_number-1]

drugs = {
    'bepridil': '31.5',
    'chlorpromazine': '34.5',
    "cisapride": '2.6',
    'diltiazem': '127.5',
    'dofetilide': '2.1',
    'mexiletine': '2503.2',
    'ondansetron': '358.5',
    'quinidine': '842.9',
    'ranolazine': '1948.2',
    'sotalol': '2.1',
    'terfenadine': '9',
    'verapamil': '45'
}

dataset = 'with_CiPA_parameters' # can also be set to 'with_Crumb_parameters' to use data from Crumb et al
population = '+-30%' # level of variance in the population can be '+-5%', '+-30%' and '+-50%' with data provided

data_path = os.getcwd()+'/'+dataset+'/'+population # get the directory of the path where this file is stored.
metrics_path = os.getcwd()+'/../metrics/va/'+dataset # the directory where the metrics file is to be stored

with open(metrics_path+'/'+'va'+population+'_population_'+dataset+'.csv', 'w') as metrics:
    metrics.write("Param#,Peak Voltage,RMP,Max Upstroke Velocity,APD1,APD2,APD3,Tri90-40,CTD90,CTD50,CaTamp,CaTmax,CaiD,EMw,qNet,EAD,Depolarization,Index,GNa,GNaL,Gto,GKr,GKs,GK1,Gncx,Pnak,PCa,drug,cnet,dose")
    metrics.write('\n')
    for drug in drugs.keys():
        for file in os.listdir(data_path+'/'+drug):
            if file != (".DS_Store" or ".git"):
                with open(data_path+'/'+drug+'/'+file) as f:
                    lis = [line.split() for line in f]
                    dose = str(get_dose(f.name))
                    cnet = drugs.get(drug)
                    for i in range(42, len(lis)):
                        line = str(lis[i][0])
                        metrics.writelines(line+','+drug+','+cnet+','+ dose + '\n')
                f.close()
    metrics.close()




