import hashlib
# importing the requests library
import requests
import json
import time

user_id = 0
public_hash = 'unique_public_hash'
hash_rate = 100000
STATIC = True
# api-endpoint
def request_for_bin_dynamic():
	# user_id = input('Enter id')
	global user_id,public_hash
	# public_hash = input('Enter public key/hash')	
	URL = "http://localhost:5000/get_bin_dynamic/"+str(user_id)+"/"+public_hash 
	r = requests.get(url = URL)
	data = r.content
	print(data)	
	return data

def request_for_bin_static():
	# user_id = input('Enter id')
	global user_id,public_hash
	# public_hash = input('Enter public key/hash')	
	URL = "http://localhost:5000/get_bin_static/"+str(user_id)+"/"+public_hash 
	r = requests.get(url = URL)
	data = r.content
	print(data)	
	return data

def register():
	global user_id
	URL = "http://localhost:5000/register/"+public_hash 
	r = requests.get(url = URL)
	user_id = int(r.content)

def request_block():
	URL = "http://localhost:5000/get_block" 
	r = requests.get(url = URL)
	# print(r)
	return r.content

def hash_rate_fn(bin_size):
	global hash_rate
	return bin_size/hash_rate

def calc_hash(nonce , block):
  sha = hashlib.sha256()
  sha.update(str(block.index).encode('utf-8') + 
             str(block.timestamp).encode('utf-8') + 
             str(block.data).encode('utf-8') + 
             str(block.previous_hash).encode('utf-8'))
  return sha.hexdigest()

register()
block = request_block()


if STATIC: 
	while(True):
		nonce = request_for_bin_static()
		print(type(nonce))
		nonce = nonce.decode()
		nonce =str(nonce)
		nonce = json.loads(nonce)

		time.sleep(hash_rate_fn(nonce[1]-nonce[0]) )
else:
	while(True):
		nonce = request_for_bin_dynamic()
		print(type(nonce))
		nonce = nonce.decode()
		nonce =str(nonce)
		nonce = json.loads(nonce)
		time.sleep(hash_rate_fn(nonce[1]-nonce[0]) )
