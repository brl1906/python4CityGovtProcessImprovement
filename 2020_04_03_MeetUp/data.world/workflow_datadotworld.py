#!/usr/bin/env python
# coding: utf-8

# # Datadotworld example flow

# ## What's the problem?
# When BPIO is processing data in-house, the best option is going to be direct SQL queries with the `pyodbc` Python package. That provides faster access to the freshest possible data on facilities and fleet activity. But we aren't going to be handing out our database credentials to everyone who's involved in a data partnership with us, or who just wants to explore a bit of DGS data. 
# 
# For external partners, analysts, and collaborators, the `datadotworld` Software Development Kit for Python offers a clean alternative. We break off tables that can be saved as .csv or .xslx files, host them at our page on the [Data.World site](https://data.world/dgsbpio), and partners can gain access to them without us needing to pass them files. This has several advantages:
# 
# - The lack of data files enables cleaner GitHub repositories and workflows.
# - We can update the data in one place and all partners will have the update, without us needing to send files to each of them.
# - The data dictionary uploads along with the data, so we can be sure everybody has the same column definitions.
# 
# The code below demonstrates some of the features and flows we can expect from data served by data.world.
# 
# ## Setup

# In[1]:


import datadotworld as dw  # here's the Python SDK
import pandas as pd  # at DGS, we typically pair datadotworld with Pandas
import pprint as pp
from pathlib import Path


# ### Configure the SDK if needed
# This library requires a data.world API authentication token to work.
# 
# Your authentication token can be obtained on data.world once you enable Python under Integrations > Python
# 
# To configure the library, run the following command. You will be prompted to provide your API key. 

# In[2]:


# dw configure


# ## Basic data import
# ### Load dataset
# The `dw.load_dataset()` function is probably the one that partners would use the most, if they simply want to use Data.World to obtain data. 
# 
# Take a look at the structure of the dictionary returned by the `describe()` method on a datadotworld dataset. 

# In[3]:


facilities = dw.load_dataset(dataset_key='dgsbpio/facilities-sandbox')
pp.pprint(facilities.describe())


# ### Import a specific table for analysis
# #### ... as a QueryResults object
# We can use the SDK's `query()` function to grab whole tables ... or selections or combination of tables based on a SQL query. This returns a QueryResults object.

# In[4]:


wr = dw.query(dataset_key='dgsbpio/facilities-sandbox', 
              query='SELECT * FROM work_requests')

type(wr)


# The main advantage of keeping the data as a `QueryResults` object is that the column descriptions are all accessible through its `describe()` method:

# In[5]:


pp.pprint(wr.describe(), depth=3)


# #### ... as a Pandas DataFrame
# But what if we want to just analyze the data in Pandas?
# 
# A `QueryResults` object returned by `query()` has a `.dataframe` attribute that causes the return value to be a Pandas DataFrame. 

# In[6]:


wr_df = wr.dataframe


# In[7]:


wr_df.head()


# Notice that the numerical ID columns, which we saved, correctly, as _strings_ in the Data.World browser-based UI, are still strings when we import them into a Pandas DataFrame here. **That is awesome!** Similarly, the datetime columns remain in the correct format, and the user of the Python SDK does not need to coerce them into the correct data type.

# In[8]:


wr_df.dtypes


# ## Use the API client to upload data
# The idea of using an API to push data up to Data.World originally got the Baltimore DGS team pretty excited because we hoped to be able to use GitHub as a familiar space to store all the data descriptions, labels, column descriptions, and so on. Then, if we were interested in applying version control to this information, that would just work out of the box.  
# 
# It turns out, though, that Data.World's API is still a bit limited. Only file labels (e.g. "clean data", "raw data", "documentation") and a file-level description can be created in this way. The following cells demonstrate this functionality. 

# In[9]:


# fire up a client object
client = dw.api_client()
path = Path.cwd() / 'data' / 'buildings.csv'


# In[10]:


# create an empty dictionary
metadata = {}
# put some labels and a description into the dictionary
metadata['buildings.csv'] =  { 'labels': ['raw data'], 
                              'description': 'the file description for this file'}

# upload the data to the DGS sandbox!
client.upload_files(dataset_key='dgsbpio/facilities-sandbox',
                    files=[path], 
                    files_metadata=metadata)


# Taking a look at the methods and attributions of the client object shows us that the API can do lots of things, most of which we haven't tried yet. Options include:
# 
# - appending rows to an existing table
# - adding or deleting datasets, insights, and projects
# - syncing files

# In[11]:


dir(client)

