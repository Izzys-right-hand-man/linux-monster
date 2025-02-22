import base64
from flask import Flask, request
from main import onload_proxy

app = Flask(__name__)

@app.route("/", defaults = {"path": ""})
@app.route("/<path:path>", methods = ["GET", "POST"])

def proxy(path):
  proxy_now = onload_proxy()
  proxy_url = f"https://{proxy_now.split('@')[1]}"
  
  auth_encode = base64.b64encode(proxy_now.split('@')[0].split('//')[1].encode()).decode()
  
  headers = dict(request.headers)
  headers["Proxy-Authorization"] = f"Basic {auth_encode}"
  
  try:
    if request.method == "POST":
      response = request.post(path, proxies = {'https' : proxy_url, 'http' : proxy_url}, data = request.data)
      
    else:
      response = request.get(path, proxies = {'https' : proxy_url, 'http' : proxy_url}, parameters = request.arg)
    
    return response.status_code
  except Exception as error:
    return f"An error occured : {error}",500
    
if __name__ == "__main__":
  app.run(host='127.0.0.1', port = 8000)