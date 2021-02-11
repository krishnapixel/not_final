import os
import urllib.parse
import urllib.request
import json
import csv

def loadData(filenameRoot, howMany) :
	csvFile = filenameRoot
	if not os.path.isfile(csvFile) :
		params = urllib.parse.urlencode({"$limit":howMany})
		uri = "https://data.buffalony.gov/resource/9p2d-f3yt.json?%s" % params
		response = urllib.request.urlopen(uri)
		content_string = response.read().decode()
		content = json.loads(content_string)
		writeDataToCSVFile(csvFile, content, ['apno', 'aptype', 'issued', 'value'], True)


def writeDataToCSVFile(filename, data, headers, header_flag) :
  with open(filename, 'w') as f:
    if header_flag:
      f.write(",".join(headers) + "\n")
      for chunk in data:
        raw = []
        for key in headers:
          raw.append(chunk[key])
        f.write(",".join(raw) + "\n")

def makeDictionary(k, v):
  result ={}
  for i in range(0, len(k)):
    result[k[i]] = v[i]
  return result


def readDataFromCSVFile(filename):
  f = open(filename, newline='', encoding="utf-8")
  h = f.readline().strip().split(",")
  result = []
  for line in f.readlines():
    data = line.strip().split(",")
    result.append(makeDictionary(h, data))
  f.close()
  return result

def dictionaryToListOfValues(k, dictionary):
    result = []
    for key in k:
        result.append(dictionary[key])
    return result

def filterIn(data, dictkey, dictval):
  result = []
  for i in data:
    for k,v in i.items():
      if k == dictkey and v == dictval: 
        result.append(i)
        break
  return result

#okay
def filterOut(data, dictkey, dictval):
 result = [] 
 for i in data:
      flag = False
      for k,v in i.items():
        if k == dictkey and v == dictval:
          flag = True
          break
      if not flag:
        result.append(i)
 return result

#okay
def filterInRange(data, dictkey, a, b):
  result = [] 
  for i in data:
    if int(float(i[dictkey])) >= a and int(float(i[dictkey])) < b:
      result.append(i)
  return result

def filterByMonth(data,month):
	result=[]
	for i in data:
		m = int(i['issued'][5:7])
		if month == m:
			result.append(i)
	return result

def filterByYear(data, year):
  result = []
  for i in data:
    y = int(i['issued'][0:4])
    if y == year:
      result.append(i)
  return result

def permitsByYear():
  loadData("permitData.csv", 5000)
  data = readDataFromCSVFile("permitData.csv")
  year = []
  yearCount = []
  for i in range(2008, 2020):
    year.append(i)
    yearCount.append(len(filterByYear(data, i)))
  result = {}
  result['div'] = 'graph2'
  result['x'] = year
  result['y'] = yearCount
  result['type'] = 'scatter'
  return result

def permitsByMonth():
  loadData("permitData.csv", 5000)
  data = readDataFromCSVFile("permitData.csv")
  monthCount = []
  for i in range(1, 13):
    monthCount.append(len(filterByMonth(data, i)))
  month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
  result = {}
  result['div'] = 'graph1'
  result['x'] = month
  result['y'] = monthCount
  result['type'] = 'bar'
  return result

def permitsScatter():
  loadData("permitData.csv", 5000)
  data = readDataFromCSVFile("permitData.csv")
  result = []
  for i in range(2019, 2020):
    filteredByYear = filterByYear(data, i)
    values = []
    smallValue = 0
    mediumValue = 0
    largeValue = 0
    for j in filteredByYear:
      small = filterInRange(filteredByYear, 'value', 0, 5000)
      medium = filterInRange(filteredByYear, 'value', 5000, 50000)
      large = filterInRange(filteredByYear, 'value', 50000, 500000)
      
      for k in small:
        smallValue += small['value']
      
      for k in medium:
        mediumValue += medium['value']
      
      for k in large:
        largeValue += large['value']
    values.append(smallValue)
    values.append(mediumValue)
    values.append(largeValue)
    sizes = ['small', 'medium', 'large']
    jsonData = {}
    jsonData['x'] = values
    jsonData['y'] = sizes
    jsonData['year'] = i
    result.append(jsonData)
  print(result)
  return result
    
