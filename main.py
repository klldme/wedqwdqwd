import sanic
import json
import aiohttp
import os
from jinja2 import Environment, FileSystemLoader

app = sanic.Sanic("D")
env = Environment(loader=FileSystemLoader('', encoding='utf8'))

def render_template(file_, **kwargs) -> str:
  template = env.get_template(file_)
  return sanic.response.html(template.render(**kwargs))

@app.route('/', methods=['GET', 'POST'])
async def index(request):
  if request.method == "GET":
    return render_template("index.html")
  elif request.method == "POST":
    code = request.form.get('CODE')
    async with aiohttp.ClientSession() as session:
      async with session.request(
        method="POST",
        url=os.environ['url'],
        data=f"grant_type=authorization_code&code={code}",
        headers={
          "Content-Type": "application/x-www-form-urlencoded",
          "Authorization": "basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE=",
        }
      ) as r:
        data_ = await r.text()
        data = json.loads(data_)
        print(data)
        if data != {'errorCode': 'errors.com.epicgames.account.oauth.authorization_code_not_found', 'errorMessage': 'Sorry the authorization code you supplied was not found. It is possible that it was no longer valid', 'messageVars': [], 'numericErrorCode': 18059, 'originatingService': 'com.epicgames.account.public', 'intent': 'prod', 'error_description': 'Sorry the authorization code you supplied was not found. It is possible that it was no longer valid', 'error': 'invalid_grant'}:
          pass
        else:
          return render_template("index.html", text2="Invalid Code!")
    async with aiohttp.ClientSession() as session:
      async with session.request(
        method="POST",            
        url=f"https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{data['account_id']}/deviceAuth",
        headers={
          "Authorization": f"Bearer {data['access_token']}",
          "Content-Type": "application/json"
        }
      ) as r:
        data2 = await r.text()
    async with aiohttp.ClientSession() as session:
      async with session.request(
        method="GET",            
        url=f"https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{data['account_id']}",
        headers={
          "Authorization": f"Bearer {data['access_token']}"
        }
      ) as Email_:
        Email = await Email_.text()
        email = json.loads(Email)
        print(email)
        base = {email['email']: {}}
        auths = json.loads(data2)
        auths['created'].pop('ipAddress')
        auths['created'].update({'ipAddress':request.headers.get('x-real-ip')})
        auths.update({'displayName': data['displayName']})  
        base[email['email']].update(auths)
        return sanic.response.json(base)

@app.route('/plain', methods=['GET', 'POST'])
async def index(request):
  if request.method == "GET":
    return render_template("cousin.html")
  elif request.method == "POST":
    code = request.form.get('CODE')
    async with aiohttp.ClientSession() as session:
      async with session.request(
        method="POST",
        url=os.environ['url'],
        data=f"grant_type=authorization_code&code={code}",
        headers={
          "Content-Type": "application/x-www-form-urlencoded",
          "Authorization": "basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE=",
        }
      ) as r:
        data_ = await r.text()
        data = json.loads(data_)
        print(data)
        if data != {'errorCode': 'errors.com.epicgames.account.oauth.authorization_code_not_found', 'errorMessage': 'Sorry the authorization code you supplied was not found. It is possible that it was no longer valid', 'messageVars': [], 'numericErrorCode': 18059, 'originatingService': 'com.epicgames.account.public', 'intent': 'prod', 'error_description': 'Sorry the authorization code you supplied was not found. It is possible that it was no longer valid', 'error': 'invalid_grant'}:
          pass
        else:
          return render_template("cousin.html", text2="Invalid Code!")
    async with aiohttp.ClientSession() as session:
      async with session.request(
        method="POST",            
        url=f"https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{data['account_id']}/deviceAuth",
        headers={
          "Authorization": f"Bearer {data['access_token']}",
          "Content-Type": "application/json"
        }
      ) as r:
        data2 = await r.text()
    async with aiohttp.ClientSession() as session:
      async with session.request(
        method="GET",            
        url=f"https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{data['account_id']}",
        headers={
          "Authorization": f"Bearer {data['access_token']}"
        }
      ) as Email2:
        Email = await Email2.text()
        email = json.loads(Email)
        auths = json.loads(data2)
        return sanic.response.text(f'''DEVICE_ID="{auths['deviceId']}"
ACCOUNT_ID="{auths['accountId']}"
SECRET="{auths['secret']}"''')
      
      
app.run(
  host="0.0.0.0",
  port=8080
)