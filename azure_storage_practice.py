from azure.storage.blob import (
    BlobServiceClient, ContainerClient, BlobClient

)
import json

config_source = "./infofab-sapforsales-config.json"
with open(config_source, encoding='utf-8') as f:
  config = json.load(f)

storage_name = config['storage_name']
storage_key = config['storage_key1']
storage_string = config['storage_connection_string1']
storage_url = f"https://{storage_name}.blob.core.windows.net/"

blob_service_client = BlobServiceClient(
    account_url=storage_url, 
    credential=storage_key
    )

account_info = blob_service_client.get_account_information()

container_name = config['container_name']
container_client = ContainerClient(
    account_url=storage_url,
    container_name=container_name,
    credential=storage_key
    )



print(dir(container_client))
#print(dir(blob_client))
blob_list = container_client.list_blobs()
for blob in blob_list:
    print("\t" + blob.name)

blob_client_positions = BlobClient(
    account_url=storage_url, 
    container_name=storage_name, 
    blob_name="104人力銀行_SAP_positions.csv", 
    credential=storage_key
    )

blob_client_companies = BlobClient(
    account_url=storage_url, 
    container_name=storage_name, 
    blob_name="104人力銀行_SAP_companies.csv", 
    credential=storage_key
    )
print(dir(blob_client_companies))


#print(account_info)
#print(dir(blob_service_client))

# for container in blob_service_client.list_containers():
#     print(container)
#     print(dir(container))
#     print(dir(container.items()[0]))
#     print(container.items()[0].__module__)

