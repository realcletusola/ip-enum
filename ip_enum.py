import json 
import time  
import asyncio
import argparse 
import sys 
import os 

import html2text
import requests
import aiohttp
import regex



# defining the argument parsers 
parser = argparse.ArgumentParser()
parser.add_argument('-a', '--address', type=str, required=True, help="provide at least one address")
parser.add_argument('-o', '--output', type=str, required=False, help="save result to as file name (optional)")
args = parser.parse_args()


# asinging names to our arguments
address = args.address
output_file = args.output 
address_list = []

# verify address is not none 
if not address:
	print(" ")
	print("\033[91m [+][+] you must provide at least one address [+][+] \033[00m")
	print("\033[91m [+][+] use -h argument for help (i.e python3 ip_goe.py -h) [+][+] \033[00m")
	print(" ")
	sys.exit()
else:
	address_list.append(address)
	pass

ip_score_url = "https://scamalytics.com/ip"
ip = address_list[0]
ip_locate_url = 'http://ip-api.com/batch'


pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}')

# async function to get ip fraud score  
async def get_ip_score(url: str, ip: str) -> str:

	try:
		async with aiohttp.ClientSession() as session:
			api_request = await session.post(f"{url}/{ip}")
			api_response = await api_request.text()
			response_text = html2text.html2text(api_response)
			clean_text = pattern.findall(response_text)
			result = clean_text[0]
			print("\033[92m [+][+][+] IP FRAUD SCORE [+][+][+] \033[00m \n")
			print(f"\033[92m {result} \033[00m")
			print(" ")

			return result 
	except:
		print("\033[91m [+][+] unable to get ip fraud score, server unavailable [+][+] \033[00m")
		print(" ")

# async function to get ip information 
async def get_ip_info(url: str, address_list: str) -> list:

	try:
		async with aiohttp.ClientSession() as session:
			api_request = await session.post(url, json=address_list)
			api_response = await api_request.json()
			api_data = json.dumps(api_response[0])
			api_json_data = json.loads(api_data)
			print(api_json_data)
			print(" ")

			query = api_json_data["query"]

			print(" ")
			print("\033[92m [+][+][+] IP INFO [+][+][+] \033[00m \n")
			print(f"\033[92m ********{query}******** \033[00m")
			time.sleep(0.2)
			print("\033[92m [+][+][+] Status : ", api_json_data["status"],"\033[00m")
			time.sleep(0.2)
			print("\033[92m [+][+][+] Country : ", api_json_data["country"],"\033[00m")
			time.sleep(0.2)
			print("\033[92m [+][+][+] Country Code : ", api_json_data["countryCode"],"\033[00m")
			time.sleep(0.2)
			print("\033[92m [+][+][+] Region : ", api_json_data["region"],"\033[00m")
			time.sleep(0.2)
			print("\033[92m [+][+][+] Region Name : ", api_json_data["regionName"],"\033[00m")
			time.sleep(0.2)
			print("\033[92m [+][+][+] City : ", api_json_data["city"],"\033[00m")
			time.sleep(0.2)
			print("\033[92m [+][+][+] Zip : ", api_json_data["zip"],"\033[00m")
			time.sleep(0.2)
			print("\033[92m [+][+][+] Latitude : ",api_json_data["lat"],"\033[00m")
			time.sleep(0.2)
			print("\033[92m [+][+][+] Longitude : ", api_json_data["lon"],"\033[00m")
			time.sleep(0.2)
			print("\033[92m [+][+][+] Timezone : ", api_json_data["timezone"],"\033[00m")
			time.sleep(0.2)
			print("\033[92m [+][+][+] ISP : ", api_json_data["isp"],"\033[00m")
			time.sleep(0.2)
			print("\033[92m [+][+][+] ISP Organization : ", api_json_data["org"],"\033[00m")
			time.sleep(0.2)
			print("\033[92m [+][+][+] ISP Association : ", api_json_data["as"],"\033[00m")
			print(" ")

			return api_json_data
	except:
		print("\033[91m [+][+] unable to get ip information, server unavailable [+][+] \033[00m")
		print(" ")


# main function 		
async def main() -> None:

	ip_score = asyncio.create_task(get_ip_score(ip_score_url,ip))
	ip_info = asyncio.create_task(get_ip_info(ip_locate_url,address_list))

	value1 = await ip_score
	value2 = await ip_info

	# print(value2)

	query = value2["query"]

	# check if filename is provided 
	if output_file is not None:


		# remove the file extention 
		file = os.path.splitext(output_file)
		filename = file[0]
		file_name = f"{filename}.txt" 

		# open and write to file  
		with open(file_name, "a") as f:
			try:
				f.write(f"""
				******** IP INFORMATION FOR {query}******** 
				[+][+][+] Status :  {value2["status"]}
				[+][+][+] Country :  {value2["country"]}
				[+][+][+] Country Code : {value2["countryCode"]}
				[+][+][+] Region :  {value2["region"]}
				[+][+][+] Region Name :  {value2["regionName"]}
				[+][+][+] City :  {value2["city"]}
				[+][+][+] Zip :  {value2["zip"]}
				[+][+][+] Latitude : {value2["lat"]}
				[+][+][+] Longitude :  {value2["lon"]}
				[+][+][+] Timezone :  {value2["timezone"]}
				[+][+][+] ISP :  {value2["isp"]}
				[+][+][+] ISP Organization :  {value2["org"]}
				[+][+][+] ISP Association : {value2["as"]} 
				\n\n
				******** IP FRAUD SCORE FOR {query} ********
				{value1}
				\n
				""")
				f.close()
			except:
				print(f"\033[91m [+][+] Error creating or writing to file '{file_name}' [+][+] \033[00m")	
	else:
		pass

	print("")
	print("\033[92m [+][+][+] TASK COMPLETED [+][+][+] \033[00m")


asyncio.run(main())
