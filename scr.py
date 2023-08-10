import sys
import os
import shutil
import datetime
import time
from schedule import * 
import schedule
#The format is : scriptName.py(in this case scr.py) [SourceFolder path] [replicaFolder path] [logFile path] [Number of minutes to resyncronize Folders] ^type this command in cmd^
# arg 1 = FOlder Destinatie 
# arg 2 = Folder replica 
# arg 3 = Locatie log file
# arg 4 = numarul de minute la care sa se repete scriptul
def DeletingDone():
    print('----------------Deleting Done----------------\n')
    file=open(fullPathLog,'a')
    file.write('\n--------------------------------------------------------------------------\n\n')
    file.close

def LogAppend(string):
    file=open(fullPathLog,'a')
    file.write(string)
    file.close
#functia LogAppend este facuta pentru a scrie in fisierul log

def logMake():
    path=sys.argv[3]
    logName='Log_'+os.path.basename(sys.argv[1])+'.txt'
    global fullPathLog
    fullPathLog=path+"\\"+ logName
    print("Name of the Log File : " + logName  + '\n')
    print("The path for the log file is : " + fullPathLog + '\n')
    global now
    now = datetime.datetime.now()
    file=open(fullPathLog,'w')
    file.write(f'File Created at : {now}\n\n'+'--------------------------------------------------------------------------\n\n')
    file.close
    file=open(fullPathLog,'a')
    file.write('The arguments you have entered are : \n'+'The source folder is : '+ x + '\nThe replica folder is : ' + y + '\nLog file path : ' + z + '\nInterval for synchronization of folders :' + str(q) + '\n\n--------------------------------------------------------------------------\n\n')
    file.close
#Functia logMake creeaza fisierul log in locatia specificata in argumentul 3 

def logDeleteFile(path):
    os.unlink(path)
    print('File '+ path + ' deleted')
    file=open(fullPathLog,'a')
    file.write('File ' + path + ' deleted.'+'\n')
    file.close
#Functia logDeleteFile sterge un fisier si  afiseaza in consola si scrie in log de fiecare data cand un fisier este sters 

def logDeleteDir(path):
    shutil.rmtree(path)
    print('Directory '+ path + ' deleted')
    file=open(fullPathLog,'a')
    file.write('Directory ' + path + ' deleted.'+'\n')
    file.close

#Functia logDeleteDir sterg un folder afiseaza in consola si scrie in log de fiecare data cand un folder este sters 

def recicle():
    print('Starting Deleting ....\n--------------------------------')
    LogAppend('Starting Deleting .... \n')
    folder = sys.argv[2]
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isdir(file_path): 
                logDeleteDir(file_path)
            elif os.path.isfile(file_path) :
                logDeleteFile(file_path)

        except Exception as e:
            #print('File ' + file_path + 'already exists\n')
            file=open(fullPathLog,'a')
            file.write('File ' + file_path + 'already exists\n')
            file.close

    LogAppend('------------Deleting Completed------------ \n')
#Functia recicle sterge tot din fisierul replica pentru a fi siguri ca folderele vor fi indentice dupa executie, pot exista fisiere cu acelasi nume dar continut diferit.

def copy(path_src,path_des):
    
    try:
        print("COPYING FROM: " + path_src + " TO: " + path_des)
        shutil.copy(path_src, path_des)
        file=open(fullPathLog,'a')
        file.write(path_src + ' succesfully copied to ' + path_des+'\n')
        file.close


    except:
        print("File Exists")
#Functia copy copiaza un fisier/folder si afiseaza in consola si scrie in log cand face acest lucru.


def each_file(path_src, path_des):
    for folderName, subfolders, filenames in os.walk(path_src):
        print('\nSource Folder: \n-------------------------------------------\nThe source folder is' + folderName+'\n\nStarting COPYING..........\n-------------------\n')
        LogAppend('\n Starting COPYING.... \n')
        for subfolder in subfolders:
            print('SUBFOLDER OF ' + folderName + ': ' + subfolder)
            try:
                new_path = folderName.replace(path_src,path_des)
                os.mkdir(new_path+"\\"+subfolder)
            except:
                print("Folder Exists:" + subfolder)
                file=open(fullPathLog,'a')
                file.write('Folder exists : ' + subfolder)
                file.close

        for filename in filenames:
            new_path = folderName.replace(path_src,path_des)
            file = folderName + '\\'+ filename
            copy(file, new_path)
        print('\n---------------COPYING Done ---------------\n')
        LogAppend('----------COPYING Done----------\n')

#Functia each_file parcurge toate fisierele si folderele din locatia sursa si le copiaza in locatia replica

#each_file(sys.argv[1],sys.argv[2])
x=sys.argv[1]
y=sys.argv[2]
z=sys.argv[3]
q=int(sys.argv[4])



def job():
    print('\n\n----------------------------------------------------------------------\n\n') 
    LogAppend('\n\n\n-------File Created at : '+ str(datetime.datetime.now()) + "\n" )
    recicle()
    each_file(x,y)
    print('\n\n\n')
 #Functia job este tot procesul ce se va repeta la perioada stabilita in argumentul 4   
logMake()
recicle()
each_file(x,y)
print('\n\n----------------------------------------------------------------------\n\n') 
schedule.every(q).minutes.do(job)
#Exista o varietate larga de optiuni in ceea ce priveste timpul la care se va repeta scriptul.(minute, secunde, ore, zilee, ora exacta zi exacta, etc..)
while True :
    schedule.run_pending()
    time.sleep(1)
