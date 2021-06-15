import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import klaviyo
import requests
import base64
import io
import datetime
from time import mktime


st.title("Klaviyo2CSV")

url = "https://a.klaviyo.com/api/v1/metrics/timeline"
headers = {"Accept": "application/json"}

since_date = st.date_input("Data to be fetched since",value=datetime.datetime.today())

private_key = st.text_input("Enter your Klaviyo Private API Key")

def get_data_klaviyo(since,api_key=private_key,count="100",sort="desc"):
  querystring = {
      "api_key": private_key,
      "count": count,
      "sort": sort,
      "since": since
  }
  response = requests.request("GET",url,headers=headers,params=querystring)
  return response.json()

def get_list_json(since):
	list_of_json = []
	next_v = since
	with st.spinner('Fetching Data...'):
		while since != None:
			json_data = get_data_klaviyo(since=since,sort="asc")
			list_of_json.append(json_data["data"])
			next_v = json_data["next"]

def get_combined_df(list_of_json):
	df = pd.json_normalize(list_of_json[0])
	with st.spinner('Combining DataFrames...'):
		for f in list_of_json[::-1][:-1][::-1]:
			df.append(pd.json_normalize(f))
	return df


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

if st.button("Get Last 100 Events"):
	#querystring = {"api_key":private_key,"count":"100","sort":"desc","since":int(mktime(since_date.timetuple()))}
	#response = requests.request("GET", url, headers=headers, params=querystring)
	#j_data = response.json()
	#df = pd.json_normalize(j_data["data"])
	df = get_combined_df(get_list_json(int(mktime(since_date.timetuple()))))
	df # <-- Print DataFrame
	towrite = io.BytesIO()
	downloaded_file = df.to_excel(towrite, encoding='utf-8', index=False, header=True)
	towrite.seek(0)
	b64 = base64.b64encode(towrite.read()).decode()  # some strings
	linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="output.xlsx">Download Excel File</a>'
	st.markdown(linko, unsafe_allow_html=True)