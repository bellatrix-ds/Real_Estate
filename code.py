#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("https://raw.githubusercontent.com/bellatrix-ds/Real_Estate/refs/heads/main/Anthill.csv",header=1)  
st.write("ستون‌ها:", data.columns.tolist())

data["قیمت"] = data["قیمت"].astype(str).str.replace(",", "").astype(float)

data["طبقه"] = data["طبقه - واحد"].astype(str).str.extract(r"(\d+)").astype(float)

# ---------------- Sidebar Filters ----------------
st.sidebar.title("فیلترها")

# فیلتر املاکی
agency_options = data["املاکی؟"].dropna().unique()
selected_agency = st.sidebar.multiselect("انتخاب املاکی", agency_options, default=agency_options)

# فیلتر اتاق
room_options = data["اتاق"].dropna().unique()
selected_rooms = st.sidebar.multiselect("تعداد اتاق", room_options, default=room_options)

# ---------------- Filtered Data ----------------
filtered_data = data[
    data["املاکی"].isin(selected_agency) &
    data["اتاق"].isin(selected_rooms)
]

# ---------------- Price by Floor Group Chart ----------------
def categorize_floor(floor):
    if pd.isna(floor):
        return "نامشخص"
    if floor < 10:
        return "زیر ۱۰"
    elif floor > 19:
        return "بالای ۱۹"
    else:
        return "بین ۱۰ تا ۱۹"

filtered_data["گروه طبقه"] = filtered_data["طبقه"].apply(categorize_floor)

price_by_floor_group = filtered_data.groupby("گروه طبقه")["قیمت"].mean().reset_index()

# رسم نمودار
st.subheader("میانگین قیمت بر اساس گروه طبقات")
fig, ax = plt.subplots()
ax.bar(price_by_floor_group["گروه طبقه"], price_by_floor_group["قیمت"])
ax.set_ylabel("میانگین قیمت")
ax.set_xlabel("گروه طبقه")
st.pyplot(fig)

# ---------------- Display Filtered Table ----------------
st.subheader("لیست خانه‌ها")
st.dataframe(filtered_data)


# In[ ]:




