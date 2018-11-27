#DISCLAIMER:

	# <This program accesses Health Canada's API for Medical Devices>
	# Copyright (C) 2018  Yuting Chu

	# This program is free software: you can redistribute it and/or modify
	# it under the terms of the GNU General Public License as published by
	# the Free Software Foundation, either version 3 of the License, or
	# any later version.

	# This program is distributed in the hope that it will be useful,
	# but WITHOUT ANY WARRANTY; without even the implied warranty of
	# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	# GNU General Public License for more details.

	# You should have received a copy of the GNU General Public License
	# along with this program.  If not, see <https://www.gnu.org/licenses/>.



import requests
import sys
import os

from csv import writer

def get_data(url, headers, params):

	url = url
	headers = headers
	params = params

	try:
		response = requests.get(
			url,
			headers = headers,
			params = params,

			)
		
		if response.ok == False:  #btwn http error 400-600; source: http://docs.python-requests.org/en/master/api/#requests.Response.raise_for_status
			raise ConnectionError(f"Error: {response.status_code} {response.reason}. A Connection error has occurred!")
		
	except requests.ConnectionError:  #source: http://docs.python-requests.org/en/master/user/quickstart/#errors-and-exceptions
		print("Connection Error. Ending Program early")
		sys.exit() 

	#data is list
	data = response.json()

	return data 


def get_userOK(data, filename):

	numRows = len(data)

	cwd = os.getcwd()

	print("Data downloaded.")
	

	if sys.platform.startswith("dar"):   #current system is Mac OS
		print(f"Placing data into: {cwd}/{filename}")
	
	else:
		print(f"Placing data into: {cwd}"+"'/'" + f"{filename}")



	print(f"There are {numRows} rows of data.")
	answer = input(f"Press Q to quit. Press Any Key to continue: ")

	if answer.upper() == "Q":
		print("Program Ends")
		sys.exit()

def post_tofile(data, filename):


	counter = 0  #initialize

	#put in column headings; I only need the keys
	for item in data:
		clist=list(item.keys())
		
		#write keys to csv file; "a" to append to end of file if it exists
		with open(filename, "a") as file:
			csv_writer = writer(file)
			csv_writer.writerow(clist)
		break #no need to continue; Only  the keys are needed


	#put in values		
	for item in data:

		#put key values into list
		clist=list(item.values())
				
		#write to csv file; "a" to append to end of file if it exists
		with open(filename, "a") as file:
			csv_writer = writer(file)
			csv_writer.writerow(clist)

			if len(data) >= 10000:
				counter = counter + 1
				print(f"Writing {counter} row of {len(data)}")


class MedicalDevice:
	def __init__(self):
		pass	

	def getCompanies(self, filename, url="https://health-products.canada.ca/api/medical-devices/company/"):
		#Get list of all company ids and company names
		
		filename = filename

		url = url
		headers = {"Accept":"application/json"}
		params = {"status":"A"}

		print("Getting List of companies...")

		#get list of all active companies including company ids and company names
		#data is list type		
		
		data = get_data(url, headers, params)
		
		get_userOK(data, filename)

		post_tofile(data, filename)
		
		print(f"List of companies downloaded into: {filename}. {len(data)} companies downloaded")


	def getLicences(self,filename, url = "https://health-products.canada.ca/api/medical-devices/licence/"):

		#find all licences attached to each company id
		

		filename = filename

		url = url		
		headers = {"Accept":"application/json"}
		params = {"state":"active"}

		#get a list of all active licences	

		print("Getting Licences...")

		data = get_data(url, headers, params)

		get_userOK(data, filename)

		post_tofile(data, filename)

		print(f"List of Licences Downloaded! {len(data)} Licences downloaded")

	def getProductCodes(self, filename, url = "https://health-products.canada.ca/api/medical-devices/deviceidentifier/"):
		#now final all device identifiers (product codes)

		filename = filename
		
		url = url
		headers = {"Accept":"application/json"}
		params = {"state":"active"}


		#get a list of all active licences	

		print("Getting Product Codes...")

		data = get_data(url, headers, params)

		get_userOK(data, filename)

		post_tofile(data, filename)

		print(f"List of Product Codes Downloaded! {len(data)} Product Codes downloaded")



	def getDeviceNames(self, filename, url = "https://health-products.canada.ca/api/medical-devices/device/" ):
		#get Device names
		
		filename = filename
		
		url = url
		headers = {"Accept":"application/json"}
		params = {"state":"active"}

		#get a list of all active device names	

		print("Getting Device Names...")

		data = get_data(url, headers, params)

		get_userOK(data, filename)

		post_tofile(data, filename)

		print(f"List of Device Names Downloaded! {len(data)} Device Names downloaded.")


#check to see if program is in Mac OS or Win OS; end program if other OS

if sys.platform.startswith("dar"):   #Mac OS
	pass
elif sys.platform.startswith("win"):  #Win OS
	pass
else:
	sys.exit("This program only runs on Mac OS or Windows. Program Ends")


dinfo = MedicalDevice()



print("Download the following data from Health Canada:")
print("(1) List of Device Names")
print("(2) List of Company Names")
print("(3) List of Licences")
print("(4) List of Products")
print("(Q) QUIT\n")

response = input("Enter Selection: ")

if response == 1:
	#ask user for filename to store device names list
	filename = input("Enter the filename to store device names list. Press Q to quit: ")
	if filename.upper() == "Q":
		sys.exit("Program Ends")

	#ask user for url to download device names list
	#need to add in http://!!
	device_url = input("Enter the url to download the device names list. Press Enter to use default. Press Q to quit: ")
	if device_url.upper() == "Q":
		sys.exit("Program Ends")

	elif device_url == "":  #user pressed enter
		#need to add extension
		dinfo.getDeviceNames(filename + ".csv")  #don't pass in company url, default already set
	else:
		#need to add extension
		dinfo.getDeviceNames(filename + ".csv", device_url)

elif response == 2:
	#ask user for filename to store list of companies
	filename = input("Enter the filename to store list of companies. Press Q to quit: ")

	if filename.upper() == "Q":
	 	sys.exit("Program Ends")

	#ask user for url to download list of companies
	#need to add in http://!!
	company_url = input("Enter the url to download the list of companies. Press Enter to use default. Press Q to quit: ")
	if company_url.upper() == "Q":
		sys.exit("Program Ends")

	elif company_url == "":  #user pressed enter
		#need to add extension
		dinfo.getCompanies(filename + ".csv")  #don't pass in company url, default already set
	else:
		#need to add extension
		dinfo.getCompanies(filename + ".csv", company_url)

elif response == 3:
	#ask user for filename to store Licence list
	filename = input("Enter the filename to store Licence list. Press Q to quit: ")
	if filename.upper() == "Q":
		sys.exit("Program Ends")

	#ask user for url to download Licence list
	#need to add in http://!!
	licence_url = input("Enter the url to download the Licence list. Press Enter to use default. Press Q to quit: ")
	if licence_url.upper() == "Q":
		sys.exit("Program Ends")

	elif licence_url == "":  #user pressed enter
		#need to add extension
		dinfo.getLicences(filename + ".csv")  #don't pass in licence url, default already set
	else:
		#need to add extension
		dinfo.getLicences(filename + ".csv", licence_url)

elif response == 4:
	#ask user for filename to store Product list
	filename = input("Enter the filename to store Product list. Press Q to quit: ")
	if filename.upper() == "Q":
		sys.exit("Program Ends")

	#ask user for url to download Product Codes list
	#need to add in http://!!
	product_url = input("Enter the url to download the Product Codes list. Press Enter to use default. Press Q to quit: ")
	if product_url.upper() == "Q":
		sys.exit("Program Ends")

	elif product_url == "":  #user pressed enter
		#need to add extension
		dinfo.getProductCodes(filename + ".csv")  #don't pass in product url, default already set
	else:
		#need to add extension
		dinfo.getProductCodes(filename + ".csv", product_url)

else:
	pass


print("Program Ends")

