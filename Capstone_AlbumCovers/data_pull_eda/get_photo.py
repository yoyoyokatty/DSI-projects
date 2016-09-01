import requests
import pickle


with open('finalish.pkl', 'r') as picklefile:
    df = pickle.load(picklefile)


count = 0
for image_link in df["artworkUrl100"]:
	try:
		count +=1
		r = requests.get(image_link)
		with open(str(count)+".jpg", "wb") as code:
			code.write(r.content)
	except:
		print image_link
		pass

