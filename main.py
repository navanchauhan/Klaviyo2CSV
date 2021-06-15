import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import klaviyo
import requests

st.title("Klaviyo2CSV")

url = "https://a.klaviyo.com/api/v1/metrics/timeline"
private_key = st.text_input("Enter your Klaviyo Private API Key")
headers = {"Accept": "application/json"}

good_test = False

if st.button("Test Connection"):
	try:
		res = requests.get("https://a.klaviyo.com/api/v2/lists?api_key={}".format(private_key))
	except:
		st.text("Your IP has been soft banned 💀")
	else:
		if res.status_code == 403:
			st.text("Whoops! Invalid API Key")
		elif res.status_code == 200:
			st.text("Connection Sucessful")
			good_test = True

if st.button("Get Last 50 Events"):
	if good_test:
		querystring = {"api_key":private_key,"count":"50","sort":"desc"}
		response = requests.request("GET", url, headers=headers, params=querystring)
		j_data = response.json()
		df = pd.normalize(j_data["data"])
		df # <-- Print DataFrame
	else:
		st.text("Please Test Connection")