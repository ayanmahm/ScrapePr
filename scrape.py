# PANDAS, NumPy, matplotLib and Seaborn are all data libraries.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams
import seaborn as sns
from urllib.request import urlopen
# BeautifulSoup cleans HTML tags from file
from bs4 import BeautifulSoup
import re

# %matplotlib inline

# IMPORT LXML AS A LIBRARY
# obtain the URL and create an object of the page
url = "http://hubertiming.com/results/2017GPTR10K"
html = urlopen(url)
soup = BeautifulSoup(html, 'lxml')
type(soup)

# Use BeautifulSoup to scrape the title
title = soup.title
print(title)

print()
# # Use BeautifulSoup to scrape the text of the webpage
# page = soup.get_text()
# print(page)

print()
# Ask BeautifulSoup to extract all hyperlinks from the page
soup.find_all('a')

# For loop to traverse through all links and return the href value
all_links = soup.find_all("a")
for link in all_links:
    print(link.get("href"))

print()
# Ask BeautifulSoup to print the first ten tables.
rows = soup.find_all('tr')
print(rows[:10])

# Iterate through the table rows and prints out each cell - includes HTML tags
print("---- The data is being printed in rows ----")
for row in rows:
    row_td = row.find_all('td')
print(row_td)
type(row_td)

# Use BeautifulSoup to clean the HTML tags from the data
print("---- The data is being cleansed ----")
str_cells = str(row_td)
cleantext = BeautifulSoup(str_cells, "lxml").get_text()
print(cleantext)

# Uses the RE (regular expressions library) to complete all of the above for each row
print("---- The data is being formatted using Regular Expressions ----")
list_rows = []
for row in rows:
    cells = row.find_all('td')
    str_cells = str(cells)
    clean = re.compile('<.*?>')
    clean2 = (re.sub(clean, '', str_cells))
    list_rows.append(clean2)
print(clean2)
type(clean2)

# Pandas - Use Pandas to put the rows into a dataframe
print("---- The data is being formatted using PANDAS ----")
dataframe = pd.DataFrame(list_rows)
dataframe.head(10)

# Cleaning the data
print("---- The data is being cleansed ----")
# Split the 0 column using the str.split method
df1 = dataframe[0].str.split(',', expand=True)
df1.head(10)

# Remove the square brackets from the data
df1[0] = df1[0].str.strip('[')
df1.head(10)

# Extract all of the tABLE hEADERS
print("---- The headers are being collected using BeautifulSoup ----")
collect_labels = soup.find_all('th')

# Use BeautifulSoup to clean the tags
print("---- The headers are being cleansed using BeautifulSoup ----")
cumulative_headers = []
collect_str = str(collect_labels)
cleansetext = BeautifulSoup(collect_str, 'lxml').get_text()
cumulative_headers.append(cleansetext)
print(cumulative_headers)

# Put all of the headers in a Pandas dataframe
print("---- The headers are being formatted using Pandas ----")
df2 = pd.DataFrame(cumulative_headers)
df2.head()

# Split all of the items in the above data frame at the comma to make headers.
print("---- The headers are being split using Pandas ----")
df3 = df2[0].str.split(',', expand=True)
df3.head()

# Combine all of the dataframes using the concat() method
print("---- The headers are being concatenated with the data items using Pandas ----")
frames = [df3, df1]
df4 = pd.concat(frames)
df4.head(10)

# Use Pandas ILOC method to select rows and columns by index.
# The first row is being made the header.
print("---- The headers are being created using Pandas ----")
df5 = df4.rename(columns=df4.iloc[0])
df5.head()

# Get an overview of the table
print("---- Pandas ----")
df5.info()
df5.shape

# Destroy rows with empty values
print("---- Pandas is dropping rows that have empty values ----")
df6 = df5.dropna(axis=0, how='any')

# Destroy the first row (it duplicates the header)
print("---- Pandas is dropping the first row ----")
df7 = df6.drop(df6.index[0])
df7.head()

# Look at the output - index 0 and 9 still have the square brackets.
# Refactor the end columns to have proper names
print("---- Pandas is refactoring the anomalous rows ----")
df7.rename(columns={'[Place': 'Place'}, inplace=True)
df7.rename(columns={' Team]': 'Team'}, inplace=True)
df7.head()
df7['Team'] = df7['Team'].str.strip(']')
df7.head()

df7.info()

# DATA VISUALISATION

# Convert the Chip Time list from hours, minutes and seconds to just minutes
time_list = df7[' Chip Time'].tolist()
# You can use a for loop to convert 'Chip Time' to minutes
time_mins = []
for i in time_list:
    # for each item in the list, split at the colon that divides the hrs, mins and secs
    print(i)
    if len(i) < 7:
        i = "00:" + i
    h, m, s = i.split(':')
    math = (int(h) * 3600 + int(m) * 60 + int(s)) // 60
    time_mins.append(math)
print(time_mins)

# Use PANDAS and add the minutes as an extra column
df7['Runner_mins'] = time_mins
df7.head()
# Generate the stats for the dataframe
df7.describe(include=[np.number])

# using pylab from matplotlib, create a boxplot.
rcParams['figure.figsize'] = 15, 5
df7.boxplot(column='Runner_mins')
plt.grid(True, axis='y')
plt.ylabel('Chip Time')
plt.xticks([1], ['Runners'])

# Use seaborn to generate a plot to measure the distribution of the "Runner mins" table.
x = df7['Runner_mins']
ax = sns.distplot(x, hist=True, kde=True, rug=False, color='m', bins=25, hist_kws={'edgecolor': 'black'})
plt.show()

# Use seaborn to make a distribution plot between men and women
women = df7.loc[df7[' Gender'] == ' F']['Runner_mins']
men = df7.loc[df7[' Gender'] == ' M']['Runner_mins']
sns.distplot(women, hist=True, kde=True, rug=False, hist_kws={'edgecolor': 'black'}, label='Female')
sns.distplot(men, hist=False, kde=True, rug=False, hist_kws={'edgecolor': 'black'}, label='Male')
plt.legend()
plt.show()

# Group all of the data by Gender, then generate values.
g_stats = df7.groupby(" Gender", as_index=True).describe()
print(g_stats)

# Using gender as a factor, create a set of boxplots
df7.boxplot(column='Runner_mins', by=' Gender')
plt.ylabel('Chip Time')
plt.suptitle("")
plt.show()
