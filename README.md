# python4CityGovtProcessImprovement
Repo for the PY 4 CG Python for City Government Process Improvement Meet Up

## To work with the CSV files in Python:

### Option 1: Read the CSV directly from Github: 
1. From https://github.com/brl1906/python4CityGovtProcessImprovement, click on the file that you want to read into python
2. Click on the Raw button, which should take you to a new page that looks like a csv (comma separated values) document
3. Copy the URL (should start with https://raw...)
4. Write the following code to read in the csv file (using example of the Bitcoin CSV)

```
url = "https://raw.githubusercontent.com/brl1906/python4CityGovtProcessImprovement/master/BITFINEX-BTCUSD.csv"
df=pd.read_csv(url)
```

### Option 2: Download the document to your workstation
1. Click the "Clone and Download" green button in the top right corner and donwnload ZIP
2. All of the files in the python4CityGovtProcessImprovement file will appear in the new download
3. Copy the file path name for the csv that you want to work with
   Windows: Hold Shift + Right click mouse on file, click on "Copy as path"
   Mac: Hold Control + Click mouse on file, hold Option, and "Copy "filename" as pathname" should show up as a selection option, click this
4. Write the following code to read in the csv file (using example of the Bitcoin CSV)

```
df = pd.read_csv('pathname for ECB_Citations.csv')
```
