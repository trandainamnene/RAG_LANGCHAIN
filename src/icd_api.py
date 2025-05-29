import requests

token_endpoint = 'https://icdaccessmanagement.who.int/connect/token'
client_id = 'ca5f34fb-5e3c-4e97-9daa-4717fc69d49c_7a98800e-a4dd-471e-b21a-c9ee4b56e9bc'
client_secret = 'rBls3UD3VljjjB5fYzruj1fdYiISeOTcSHsjY49HllI='
scope = 'icdapi_access'
grant_type = 'client_credentials'

# get the OAUTH2 token

# set data to post
payload = {'client_id': client_id,
           'client_secret': client_secret,
           'scope': scope,
           'grant_type': grant_type}

# make request
r = requests.post(token_endpoint, data=payload, verify=False).json()
token = r['access_token']

# access ICD API

uri = 'https://id.who.int/icd/entity'

# HTTP header fields to set
headers = {'Authorization': 'Bearer ' + token,
           'Accept': 'application/json',
           'Accept-Language': 'en',
           'API-Version': 'v2'}

# make request
r = requests.get(uri, headers=headers, verify=False)

# print the result
print(r.text)