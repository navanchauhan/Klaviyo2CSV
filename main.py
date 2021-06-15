import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import klaviyo
import requests

st.title("Klaviyo2CSV")

private_key = st.text_input("Enter your Klaviyo Private API Key")

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