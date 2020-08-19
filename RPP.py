import sys
import os.path as path
import os
import pandas as pd
import shutil as s
from time import sleep




## BUG on cc mode answer no == yes Done
## в pricedf не распознается index Done
## delta считается Неправильно Done


## cc- Create Config Done
## cd - Create Database Done
## n -  Normal Done

CONFIG_FILENAME = "conf.ini"
Downloads_DIR = None
Working_DIR = None
DB_name = None

## Настройки Done
# Папка загрузок Done
# Рабочая папка Done
# название базы данных Done

def h_DataComparator(curprice,db):
	delta = list()
	print('\n\n\n\n\n\n\n')
	curprice.set_index("артикул")
	db.set_index("артикул")
	tmpdf = curprice.merge(db)
	for i in range(0,len(tmpdf.index-1)):
		price_now = tmpdf.values[i][1]
		price_history = tmpdf.values[i][2]
		if price_now >= price_history:
			delta_ = (price_now - price_history) / (price_history / 100)
			delta.append(delta_)
		else:
			delta_ = (price_history - price_now) / (price_now / 100) * -1
			delta.append(delta_)
	tmpdf.insert(3,"delta",delta)
	print(tmpdf.sort_values(by=['delta']))
	tmpdf.to_excel("out.xlsx")



def UpdateDB():
	global DB_name
	os.remove(DB_name + ".xlsx")
	new_db = pd.read_excel("out.xlsx")
	print(new_db.head())
	new_db = new_db.drop(columns=["hist_цена","delta"],axis=1)
	new_db = new_db.rename(columns={"артикул":"артикул","цена":"hist_цена"})
	new_db.set_index("артикул",inplace=True)
	new_db = new_db.drop(columns="Unnamed: 0")
	new_db.to_excel(DB_name + ".xlsx")



def h_del_garbage():
	garbadge = []
	print("создайте заголовок по шаблону [артикул,наименование,цена,гарантия]")
	print("Пример на странице проекта на github")
	os.system("pause")
	print("Процесс может занять некоторое время")
	file = pd.read_excel('regard_priceList.xlsx',index_col=0)
	file = file.drop(columns=["наименование","гарантия","Unnamed: 2"],axis=1)
	data_len = len(file.index)
	for i in range(0,data_len):
		if isinstance(file.index[i],int):
			continue
		else:
			garbadge.append(file.index[i])
	file = file.drop(index=garbadge)
	return file

def h_Downloadprice():
	global Downloads_DIR
	global Working_DIR
	Working_DIR =Working_DIR[:-1]
	Downloads_DIR = Downloads_DIR[:-1]
	try:
		import webbrowser as web
		link = "https://www.regard.ru/price/regard_priceList.xlsx"
		web.open(link)
		filename = link.split('/')[-1]
		sleep(2)
		s.move(Downloads_DIR +"\\" + filename, Working_DIR + '\\' + filename)
		return True
	except Exception:
		print("Что-то пошло не так, посмотрите описание ошибки в файле error_fix.txt")
		os.system("pause")
		return False

def h_ReadConfig():
	try:
		with open(CONFIG_FILENAME) as config:
			txt = config.readlines()
			for line in txt:
				tmp = line.split("::")
				if tmp[0] == "Downloads":
					global Downloads_DIR
					Downloads_DIR = tmp[1]
				elif tmp[0] == "CWD":
					global Working_DIR
					Working_DIR = tmp[1]
				elif tmp[0] == "DB":
					global DB_name
					DB_name = tmp[1]
	except FileNotFoundError:
		print("Не могу найти файл конфигурации создайте новый запустив программу с флагом -cc (Create Config)")
		os.system("pause")

def CreateDatabase():
	global DB_name
	h_ReadConfig()
	h_Downloadprice()
	df = h_del_garbage()
	df = df.rename(columns={"артикул":"артикул","цена":"hist_цена"})
	df.to_excel(DB_name +".xlsx")
	#Пропарсить настройки Done
	## Скачать прайс Done
	 #избавится от лишнего +- Done
	 #сохранить Done

def CreateConfig():
	## Создать файл conf.ini Done

	if path.exists(CONFIG_FILENAME):
		print("Найден файл конфигурации,перезаписать?[y/n]")
		if input() == 'y' or 'Y' or "yes":
			os.remove(CONFIG_FILENAME)
		elif input() == 'n' or 'N' or 'no':
			exit(1)
	print("Укажите полный путь к папке с загрузками")
	Downloads_DIR = input()
	Working_DIR = os.getcwd()
	print("Укажите название базы данных или оставьте пустым для стандартного имени [стандартное='RPPDB']")
	DB_name =input()
	if DB_name == "":
		DB_name = "RPPDB"
	print("Создание конфигурации")
	with open(CONFIG_FILENAME,"w") as config:
		config.write("Downloads::" + Downloads_DIR +'\n')
		config.write("CWD::"+ Working_DIR +'\n')
		config.write("DB::" +DB_name)
		print("conf.ini Created")
		os.system("pause")




def NormalMode():
	global DB_name
	h_ReadConfig()
	h_Downloadprice()
	pricedf = h_del_garbage()
	db = pd.read_excel(DB_name + ".xlsx")
	pricedf.reset_index()
	pricedf.to_excel("tmp.xlsx")
	pricedf = pd.read_excel("tmp.xlsx")
	deltas = h_DataComparator(pricedf,db)
	print("\n\n\n")
	print("Обновить базу данных? [y/n]")
	if input() == ("y" or "Y" or "yes"):
		UpdateDB()
	else:
		pass



	#Пропарсить настройки Done
	## Скачать прайс Done
	 #избавится от лишнего +- Done
	  #сравнить с бд основываясь на артикулах Done
	## вычеслить изменения  Done
	#вывести Done
	 #свести в таблицу Done
	  #выгрузить Done
	## запросить сохранение в бд Done
	## Отправить увед
def main():
	if (len(sys.argv) == 2 and sys.argv[1] =="-cc"):
		print("Режим создания конфигурации")
		CreateConfig()
	elif (len(sys.argv) == 2 and sys.argv[1] == "-cd"):
		print("Режим создания базы данных")
		CreateDatabase()
	elif (len(sys.argv) == 2 and sys.argv[1] == "-n"):
		print("Штатный режим ")
		NormalMode()
		os.remove("tmp.xlsx")
	else:
		print("Ошибка. Неизвестный режим")

if __name__ == "__main__":
	main()
## ToDo исправить обновление таблицы Done 
## CODDED BY : @Fallenhacker29
