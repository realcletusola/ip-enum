import requests  
import argparse 
import sys 
import json 
import os 
import time


# defining the argument parsers 
parser = argparse.ArgumentParser()
parser.add_argument('-a', '--address', type=str, nargs='+', help="provide at least one address")
parser.add_argument('-o', '--output', type=str, required=False, help="save result to as file name (optional)")
args = parser.parse_args()


# asinging names to our arguments
address = args.address
output_file = args.output 
address_list = []

url = 'http://ip-api.com/batch'

# verify address is not none 
if not address:
    print(" ")
    print("\033[91m [+][+] you must provide at least one address [+][+] \033[00m")
    print("\033[91m [+][+] use -h argument for help (i.e python3 ip_goe.py -h) [+][+] \033[00m")
    print(" ")
    sys.exit()

# add each address to address list 
for a in address:
    address_list.append(a)

# make a post request to the ip_geo api
res = requests.post(url, json=address_list)
res_data = json.dumps(res.json())
json_data = json.loads(res_data)

# iterate the results to get results from each ip address 
for i in range(len(json_data)):
    print(" ")
    query = json_data[i]["query"]
    # check if the request returned success or fail  
    if json_data[i]["status"].casefold() == "success":
        print(" ")
        print(f"\033[92m ********{query}******** \033[00m")
        time.sleep(0.2)
        print("\033[92m [+][+][+] Status : ", json_data[i]["status"],"\033[00m")
        time.sleep(0.2)
        print("\033[92m [+][+][+] Country : ", json_data[i]["country"],"\033[00m")
        time.sleep(0.2)
        print("\033[92m [+][+][+] Country Code : ", json_data[i]["countryCode"],"\033[00m")
        time.sleep(0.2)
        print("\033[92m [+][+][+] Region : ", json_data[i]["region"],"\033[00m")
        time.sleep(0.2)
        print("\033[92m [+][+][+] Region Name : ", json_data[i]["regionName"],"\033[00m")
        time.sleep(0.2)
        print("\033[92m [+][+][+] City : ", json_data[i]["city"],"\033[00m")
        time.sleep(0.2)
        print("\033[92m [+][+][+] Zip : ", json_data[i]["zip"],"\033[00m")
        time.sleep(0.2)
        print("\033[92m [+][+][+] Latitude : ",json_data[i]["lat"],"\033[00m")
        time.sleep(0.2)
        print("\033[92m [+][+][+] Longitude : ", json_data[i]["lon"],"\033[00m")
        time.sleep(0.2)
        print("\033[92m [+][+][+] Timezone : ", json_data[i]["timezone"],"\033[00m")
        time.sleep(0.2)
        print("\033[92m [+][+][+] ISP : ", json_data[i]["isp"],"\033[00m")
        time.sleep(0.2)
        print("\033[92m [+][+][+] ISP Organization : ", json_data[i]["org"],"\033[00m")
        time.sleep(0.2)
        print("\033[92m [+][+][+] ISP Association : ", json_data[i]["as"],"\033[00m")
        print(" ")

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
                        ********{query}******** 
                        [+][+][+] Status :  {json_data[i]["status"]}
                        [+][+][+] Country :  {json_data[i]["country"]}
                        [+][+][+] Country Code : {json_data[i]["countryCode"]}
                        [+][+][+] Region :  {json_data[i]["region"]}
                        [+][+][+] Region Name :  {json_data[i]["regionName"]}
                        [+][+][+] City :  {json_data[i]["city"]}
                        [+][+][+] Zip :  {json_data[i]["zip"]}
                        [+][+][+] Latitude : {json_data[i]["lat"]}
                        [+][+][+] Longitude :  {json_data[i]["lon"]}
                        [+][+][+] Timezone :  {json_data[i]["timezone"]}
                        [+][+][+] ISP :  {json_data[i]["isp"]}
                        [+][+][+] ISP Organization :  {json_data[i]["org"]}
                        [+][+][+] ISP Association : {json_data[i]["as"]}
                    """)
                    f.close()
                except:
                    print(f"\033[91m [+][+] Error creating or writing to file '{file_name}' [+][+] \033[00m")
        else:
            pass 
    
    # if request is not successful 
    else:
        print(f"\033[91m [+][+] Unable to find info about the address {query} [+][+] \033[00m")






        







