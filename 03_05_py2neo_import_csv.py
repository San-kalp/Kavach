from py2neo import Graph
from py2neo.bulk import create_nodes, create_relationships
import pandas as pd
import json

#load csv as dataframe
im_data = pd.read_csv("sf_dataset.csv")
    

#im_data["deviceID"] = im_data["deviceID"].astype(str)

# create dataframes for node
df_business = im_data.filter(["business_id","business_name","business_address","latitude","longitude"])
# drop the duplicates so that we just try to insert the node once (multiple times will not work)
df_business = df_business.drop_duplicates('business_id', keep='last')
# turn the dataframe into json string
json_business = df_business.to_json(orient="records")
# trun json into dictionarie for the import
dict_business = json.loads(json_business)

# prepare Zip node data
df_zip = im_data.filter(["zip"])
df_zip = df_zip.drop_duplicates('zip', keep='last')
json_zip = df_zip.to_json(orient="records")
dict_zip = json.loads(json_zip)

# prepare person data
df_person = im_data.filter(["user_name","deviceID"])
df_person = df_person.drop_duplicates('deviceID', keep='last')
print(len(df_person))
json_person = df_person.to_json(orient="records")
dict_person = json.loads(json_person)

# create dataframes for relationships
df_relationship = im_data.filter(["business_id","deviceID","scan_timestamp"])
json_relationship = df_relationship.to_json(orient="records")
dict_relationship = json.loads(json_relationship)

df_relationship_zip = im_data.filter(["business_id","zip"])
df_relationship_zip = df_relationship_zip.drop_duplicates('business_id', keep='last')
json_relationship_zip = df_relationship_zip.to_json(orient="records")
dict_relationship_zip = json.loads(json_relationship_zip)


#print(dict_relationship_zip)
#print(dict_relationship)

#connect to neo4j
graph = Graph("neo4j+s://8360bf53.databases.neo4j.io", auth=("neo4j", "l4TgLWzCraMg8p88PDzH5HM0uQoymEAxSupssHDrcw8"))

# Create business nodes
create_nodes(graph.auto(), dict_business, labels={"Business"})
print(graph.nodes.match("Business").count())

# Create zip nodes
create_nodes(graph.auto(), dict_zip, labels={"Zip"})
print(graph.nodes.match("Zip").count())

# create person nodes
create_nodes(graph.auto(), dict_person, labels={"Person"})
print(graph.nodes.match("Person").count())


#create relationships people visiting businesses
ex_people = []

for p in dict_relationship:
    
    device= p["deviceID"]
    business = p["business_id"]

    p.pop("deviceID")
    p.pop("business_id")
    ex_people.append((device,p,business))

#print(ex_people)

#man_relationship = [("5403628525158",{"scan_timestamp":"2022-03-05 23:19:25"},"0311287-01-001")]
rel_pb = create_relationships(graph.auto(), ex_people, "VISITED", start_node_key=("Person", "deviceID"), end_node_key=("Business", "business_id"))
print(rel_pb)

#create zip and business
ex_zip = []

for p in dict_relationship_zip:

    zip= p["zip"]
    business = p["business_id"]
    ex_zip.append((business,{"active":1},zip))

#print(ex_zip)

rel_bz = create_relationships(graph.auto(), ex_zip, "ISLOCATED", start_node_key=("Business", "business_id"), end_node_key=("Zip", "zip"))
print(rel_bz)

