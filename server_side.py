from flask import Flask
import time
import json 

app = Flask(__name__)

inc_id = 0
users = {}
info = {}
high = 10**5
default_time = 5

def get_last_id():
	global inc_id
	inc_id+=1
	return inc_id

@app.route("/register/<public_hash>")
def register(public_hash):
	# create id
	id_ = get_last_id()
	global users
	users[str(id_)]=public_hash 
	return str(id_)

# get block from the network and store it in 'block' variable 
block = {    
	"Version" : "0x20000000",
    "timestamp" : time.time(),
    "difficulty" : 4022059196164.95,
    "hash_prev" : "0000000000013212312356373731124",
    "Nonce" : None,
    "hash" : None
    }

@app.route("/get_block")
def get_block():
	global block
	return str(block)


@app.route("/get_bin_dynamic/<id_>/<public_hash>")
def get_bin_dynamic(id_, public_hash):
	# match public hash with the public hash in the db for the given 
	current_timestamp = time.time()
	global high,info
	print(info)
	id_ = int(id_)
	if id_ in info:
		bin_size = (info[id_][1][-1]/(current_timestamp-info[id_][0][-1]))*(default_time)
		info[id_][0].append(current_timestamp)
		info[id_][1].append(bin_size)
		high = high + bin_size
		return str([high - bin_size,high ])
	else:
		bin_size = 10**5
		info[id_] = [[],[]]
		print("came here")
		info[id_][0].append(current_timestamp)
		info[id_][1].append(bin_size)
		high = high+bin_size
	f=open('dynamic_bin_timestamps_binsize.txt','w+')
	f.write(str(info))
	f.close()
	return str([high - bin_size,high])

@app.route("/get_bin_static/<id_>/<public_hash>")
def get_bin_static(id_, public_hash):
	# match public hash with the public hash in the db for the given 
	current_timestamp = time.time()
	global high,info
	print(info)
	id_ = int(id_)
	bin_size = 10**5
	if id_ not in info:
		info[id_] = [[],[]]
	info[id_][0].append(current_timestamp)
	info[id_][1].append(bin_size)
	high = high+bin_size
	with open('static_bin_timestamps.txt','w') as f:
		f.write(str(info[id_][0]))
	with open('static_bin_binsize.txt','w') as f:
		f.write(str(info[id_][1]))
	return str([high - bin_size,high])

# print(get_bin('0','akfbldnas'))
# print(get_bin('0','akfbldnas'))
# time.sleep(3)
# print(get_bin('0','akfbldnas'))
# time.sleep(4)
# print(get_bin('0','akfbldnas'))
# time.sleep(2)
# print(get_bin('0','akfbldnas'))