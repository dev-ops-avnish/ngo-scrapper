import json,sys
filename = sys.argv[1]
if "jsonl" not in filename:
    sys.exit(1)
output = filename.replace("jsonl","csv")
data = open(filename,"r").readlines()
newline="\n"
tab="\t"
firstline = f"S.no.\tID\tName\tEmail-id\tMobile no.\tAddress\tCity\tState\tSector\tWebsite\n"
open(output,"w").write(firstline+newline)
sr = 1
for i in data:
    i= json.loads(i)
    unique_id = i.get("infor")["0"]["UniqueID"] 
    ngo_name = i.get("infor")["0"]["ngo_name"]
    Email = i.get("infor")["0"]["Email"]
    Mobile = i.get("infor")["0"]["Mobile"]
    Address= i.get("registeration_info")[0]["nr_add"].strip().replace("\r"," ").replace("\n"," ")
#     print (Address)
    City = i.get("registeration_info")[0]["nr_city"]
    State = i.get("infor")["operational_states_db"]
    Sector =  i.get("infor")["issues_working_db"]
    Website =i.get("infor")["0"]["ngo_url"]
    linedata = f"{sr}{tab}{unique_id}{tab}{ngo_name}{tab}{Email}{tab}{Mobile}{tab}{Address}{tab}{City}{tab}{State}{tab}{Sector}{tab}{Website}{newline}"
    open(output,"a").write(linedata)
    sr = sr +1 