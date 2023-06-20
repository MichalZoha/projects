import argparse
import os
import sys
import json
import shutil
from datetime import datetime
import matplotlib.pyplot as plt



#Získávání inputu uživatele
parser = argparse.ArgumentParser(description="Program, který setřídí data podle roku a týdne")
parser.add_argument("--input", help="Zadání cesty ze kterého chceme načítat soubory")
parser.add_argument("--output", help="Zadání cesty k adresáři do kterého chceme ukládat soubory")
parser.add_argument("--version", help="Vypsání aktuální verze programu", action="store_true")
parser.add_argument("--write", help="Program provede setřídění dat. Pokud tato možnost není zvolená, program udělá takzvaný dry run", action="store_true")
parser.add_argument("--graph", help="Zadejte rok ve formátu YYYY, u kterého Vás zájímá graf")
parser.add_argument("--compare", nargs=2, help="Zadejte roky ve formátu YYYY YYYY, které chcete porovnat")
user_input = parser.parse_args()

if user_input.input:
    filepath_in = user_input.input
else:
    if 'SOURCE_DIRECTORY' in os.environ:
        filepath_in = os.environ.get('SOURCE_DIRECTORY')
    else:
        filepath_in = '.'

if user_input.output:
    filepath_out = user_input.output
else:
    if 'TARGET_DIRECTORY' in os.environ:
        filepath_out = os.environ.get('TARGET_DIRECTORY')
    else:
        filepath_out = '.'

if user_input.version:
    sys.stderr.write("Current version: 1.0.0\n")



#Vytváření proměnných
files = os.listdir(filepath_in)
sys.stderr.write(f"Processing {len(files)} files..")

words_holder = [] 
files_holder = []
counter = 0
num_files = 0
num_words = 0
active_year = 0
active_week = 0
new_year = False
years = {}
data = {}
condition1 = None
condition2 = None



#Práce s daty
if user_input.input:
    for file in files:
        if file.endswith('.json'): #Kontrola jestli se jedná o .json file
            f = open(os.path.join(filepath_in, file))
            file_data = json.load(f)

            if(file_data['date'].split("-")==file.split("_")[0].split("-")): #Kontrola jestli se "date" shoduje v názvu i uvnitř souboru
                num_words+=len(file_data['text'].split())
                num_files+=1
                counter+=1
                date = datetime(*[int(x) for x in file_data['date'].split("-")])
                sys.stdout.write(f"source: {filepath_in+'/'+file}, target: {filepath_out+'/W'+str(date.isocalendar().week)+'/'+file[5:]}\n")
                

                if(active_year == 0 or active_year != date.isocalendar().year): #Kontrola jestli nepracujeme s daty z nového roku, nebo jestli žádný rok ještě není načtený
                    new_year = True

                    if new_year == True:
                        words_holder.append(num_words/num_files)
                        files_holder.append(num_files)

                    if active_week != 0:
                        data["words"] = words_holder
                        data["inputs"] = files_holder
                        years[active_year] = data
                        words_holder = []
                        files_holder = []
                        data = {}
                        num_files = 0
                        num_words = 0
                    active_year = date.isocalendar().year
                    year_dir = os.path.join(filepath_out, str(date.isocalendar().year)[2:])

                    if not(os.path.exists(year_dir)) and user_input.write: #Vytvoření adresáře pro nový rok
                        os.makedirs(year_dir)


                if(active_week == 0 or active_week != date.isocalendar().week or new_year == True): #Kontrola jestli nepracujeme s daty z nového týdne

                    if active_week != 0 and new_year == False:
                        words_holder.append(num_words/num_files)
                        files_holder.append(num_files)
                        num_words = 0
                        num_files = 0
                    active_week = date.isocalendar().week
                    week_dir = os.path.join(year_dir, "W"+str(active_week))

                    if not(os.path.exists(week_dir)) and user_input.write: #Vytvoření adresáře pro nový týden
                        os.makedirs(week_dir, 0o666)
                    new_year = False
                f.close()

                if user_input.write:
                    shutil.move(os.path.join(filepath_in, file), filepath_out+'/'+str(date.isocalendar().year)[2:]+'/W'+str(active_week)+'/'+file[5:])

    
    if counter == len(files): #Kontrola jestli jsme prošli všechny soubory na vstupu  
        sys.stdout.write("Success: "+str(counter)+'/'+str(len(files))+" were transfered\n")
    else:  
        sys.stdout.write("Failure: "+str(counter)+'/'+str(len(files))+" were transfered\n")
    if num_files != 0:
        words_holder.append(num_words/num_files)
        files_holder.append(num_files)
    if files_holder != []:
        data["words"] = words_holder
        data["inputs"] = files_holder
        years[active_year] = data


if user_input.write: #Pokud chce uživatel změny provést, nebo-li nedělat pouze "dry-run" 

    if user_input.graph != None and int(user_input.graph) in list(years.keys()): #Vytvoření grafu pro jeden rok
        plt.plot([int(x) for x in range(1,len(years[int(user_input.graph)]["inputs"])+1)], years[int(user_input.graph)]["inputs"], label = "Počet souborů")
        plt.plot([int(x) for x in range(1,len(years[int(user_input.graph)]["words"])+1)], years[int(user_input.graph)]["words"], label = "Průměrný počet slov")
        plt.xlabel('Počet')
        plt.ylabel('Týden')
        plt.title('Info o roce '+str(user_input.graph))
        plt.legend()
        plt.show()
    else:
        condition1 = False
        
    if not(user_input.compare == None):
        if (int(user_input.compare[0]) in list(years.keys()) and int(user_input.compare[1]) in list(years.keys())): #Vytvoření grafu pro porovnání dvou roků
            plt.plot([int(x) for x in range(1,len(years[int(user_input.compare[0])]["inputs"])+1)], years[int(user_input.compare[0])]["inputs"], label = "Počet souborů")
            plt.plot([int(x) for x in range(1,len(years[int(user_input.compare[0])]["words"])+1)], years[int(user_input.compare[0])]["words"], label = "Průměrný počet slov")
            plt.plot([int(x) for x in range(1,len(years[int(user_input.compare[1])]["inputs"])+1)], years[int(user_input.compare[1])]["inputs"], label = "Počet souborů")
            plt.plot([int(x) for x in range(1,len(years[int(user_input.compare[1])]["words"])+1)], years[int(user_input.compare[1])]["words"], label = "Průměrný počet slov")
            plt.xlabel('Počet')
            plt.ylabel('Týden')
            plt.title('Porovnání roků '+user_input.compare[0]+' a '+user_input.compare[1])
            plt.legend()
            plt.show()

        else:
            condition2 = False


#Input verification
if (not(user_input.write) and (not(user_input.graph == None and user_input.compare == None))):
    print("Pro možnost vytváření grafu musí být také zvolená možnost --write")

if (condition1 == False or condition2 == False):
    print("Zadané roky se nenachází mezi dostupnými ročníky, nebo byly zadané ve špatném formátu")  