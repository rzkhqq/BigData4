# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 14:49:37 2016

@author: Yudha #114
"""

import sqlite3 as lite
import sys
#import csv
#import locale
import copy

#DATA_PATH kontrakan :
#Remember \U traps on python, use this :
#Untuk di kontarkan
#DATA_PATH=r"E:\Yudha#114\Dropbox\[PENTING TIDAK URGENT]\[ARSIP KULIAH]\SEMESTER 8\Kuliah\Big Data\Tugas KElompok 1\world-development-indicators\database.sqlite"
#Untuk di TC
DATA_PATH=r"E:\UserTA\5112100086\Dropbox\[PENTING TIDAK URGENT]\[ARSIP KULIAH]\SEMESTER 8\Kuliah\Big Data\Tugas Kelompok 1\world-development-indicators\database.sqlite"
#or this:
#DATA_PATH="E:\\Yudha#114\\Dropbox\\[PENTING TIDAK URGENT]\\[ARSIP KULIAH]\\SEMESTER 8\\Kuliah\\Big Data\\Tugas KElompok 1\\world-development-indicators\\database.sqlite"

def fetch_db(query, data_path):
    con = None
    
    try:
        con = lite.connect(data_path)
        
        cur = con.cursor()    
        cur.execute(query)
        data = cur.fetchall()
        return data
                        
        
    except lite.Error as e:
        
        print("Error %s:" % e.args[0])
        sys.exit(1)
        
    finally:
        
        if con:
            con.close()
            
def save_txt(dataToSave,fileName):
    #python 3
    #csvfile = open(fileName, 'w', newline='')
    #python 2
    #csvfile = open(fileName, 'wb')
    #Writer = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_ALL)
    #Writer.writerow([ str("CountryName"), str("CountryCode"), str("Year"), str("Value") ])    
    with open(fileName, 'w') as txtfile:   
        for i in range(len(dataToSave)):
            #print(locale.format('%.2f', float(dataToSave[i][3]), True))
            #Writer.writerow([ str(dataToSave[i][0]), str(dataToSave[i][1]), int(dataToSave[i][2]), locale.format('%.2f', float(dataToSave[i][3]), True) ])
            #Writer.writerow([ dataToSave[i][0], dataToSave[i][1], dataToSave[i][2], locale.format('%.2f', dataToSave[i][3], True) ])
            try :
                line=str(dataToSave[i][0])+";"+str(dataToSave[i][1])+";"+str(dataToSave[i][2])+";"+str(dataToSave[i][3])+"\n"
            except IndexError as detail:
                    print(detail)
                    print(i)
            
            txtfile.write(line)  
    txtfile.close()
        
if __name__=="__main__":
    #1 Ambil data indikator %populasi terakses listrik     
    query_1="SELECT CountryName,CountryCode,Year,Value FROM Indicators WHERE IndicatorCode = 'EG.ELC.ACCS.ZS' ORDER BY CountryName"
    akses_listrik=fetch_db(query_1,DATA_PATH)
    save_txt(akses_listrik, "akses_listrik.txt")
    
    #2 Ambil data indikator %populasi terakses bbm non padat     
    query_2="SELECT CountryName,CountryCode,Year,Value FROM Indicators WHERE IndicatorCode = 'EG.NSF.ACCS.ZS' ORDER BY CountryName"
    akses_bbm=fetch_db(query_2,DATA_PATH)
    save_txt(akses_bbm, "akses_bbm.txt")
    
    #3 Indikator energi terbarukan 
    #a Ambil data indikator hydro electricity     
    query_3a="SELECT CountryName,CountryCode,Year,Value FROM Indicators WHERE IndicatorCode = 'EG.ELC.HYRO.ZS' ORDER BY CountryName"
    hydro=fetch_db(query_3a,DATA_PATH)
    save_txt(hydro, "hydro.txt")
     
    #b Ambil data natural gas electricity
    query_3b="SELECT CountryName,CountryCode,Year,Value FROM Indicators WHERE IndicatorCode = 'EG.ELC.NGAS.ZS' ORDER BY CountryName"
    gas=fetch_db(query_3b,DATA_PATH)
    save_txt(gas, "gas.txt")
    
    energi_terbarukan = copy.deepcopy(gas)
    for i in range(len(gas)):
        value=((energi_terbarukan[i][3]+hydro[i][3])/2)
        lst = list(energi_terbarukan[i])
        lst[3]=value
        tup=tuple(lst)
        energi_terbarukan[i]=tup
    save_txt(energi_terbarukan, "energi_terbarukan.txt")
        
    #c Ambil data  coal electricity
    query_3c="SELECT CountryName,CountryCode,Year,Value FROM Indicators WHERE IndicatorCode = 'EG.ELC.COAL.ZS' ORDER BY CountryName"
    coal=fetch_db(query_3c,DATA_PATH)
    save_txt(coal, "coal.txt")
    
    #d Ambil data  oil electricity
    query_3d="SELECT CountryName,CountryCode,Year,Value FROM Indicators WHERE IndicatorCode = 'EG.ELC.PETR.ZS' ORDER BY CountryName"
    oil=fetch_db(query_3d,DATA_PATH)
    save_txt(oil, "oil.txt")
    
    energi_habis = copy.deepcopy(oil)
    for i in range(len(oil)):
        value=((energi_habis[i][3]+coal[i][3])/2)
        lst = list(energi_habis[i])
        lst[3]=value
        tup=tuple(lst)
        energi_habis[i]=tup
    save_txt(energi_habis, "energi_habis.txt")
    
    #e Ambil data nuclear electricity
    query_3e="SELECT CountryName,CountryCode,Year,Value FROM Indicators WHERE IndicatorCode = 'EG.ELC.NUCL.ZS' ORDER BY CountryName"
    nuclear=fetch_db(query_3e,DATA_PATH)
    save_txt(nuclear, "energi_nuklir.txt")
    
    #chekc \r\n
    """file = open('fetched_data/akses_listrik.txt', 'r')
    for tulisan in file.readlines():
        a=tulisan.strip().split(";")
        print(type(str(a[0])))
        print(type(str(a[1])))
        print(type(int(a[2])))
        print(a[2])
        print(type(float(a[3])))
        print(a[3])"""
    