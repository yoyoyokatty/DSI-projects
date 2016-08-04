import requests
import pickle

with open('my_pickled_sample.pkl', 'r') as picklefile:
    url_list = pickle.load(picklefile)

count = 3191
for url in url_list[3191:]:
	try:
		count +=1
		r = requests.get(url)
		with open(str(count)+".txt", "wb") as code:
			code.write(r.content)
	except:
		print url
		pass

