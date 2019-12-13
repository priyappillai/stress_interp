from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal
import pandas as pd
import numpy as np
from scipy.stats import norm
import math


cat = 'cat'
dog = 'dog'
random1_labels = [cat, dog, dog, dog, cat, dog, dog, dog, cat, dog, dog, cat, dog, cat, cat, dog, dog, dog, dog, dog, cat, dog, cat, cat, dog, dog, dog, dog, dog, cat, dog, dog, cat, dog, dog, cat, cat, cat, dog, dog, dog, cat, dog, cat, dog, dog, dog, dog, cat, cat]
random3_labels = [cat, cat, dog, dog, dog, dog, cat, dog, dog, cat, dog, dog, dog, cat, cat, cat, cat, dog, cat, cat, dog, dog, dog, dog, cat, dog, dog, cat, cat, dog, dog, dog, dog, dog, dog, cat, dog, dog, dog, dog, dog, cat, dog, cat, dog, dog, cat, cat, cat, dog]
random4_labels = [dog, dog, dog, dog, cat, dog, cat, dog, dog, dog, cat, dog, dog, dog, dog, cat, dog, dog, dog, dog, dog, cat, cat, dog, dog, cat, dog, cat, cat, dog, dog, dog, cat, cat, cat, cat, cat, cat, dog, dog, dog, dog, dog, cat, dog, cat, cat, dog, dog, dog]
random5_labels = [dog, cat, cat, dog, cat, cat, cat, dog, dog, cat, cat, cat, cat, cat, cat, dog, dog, dog, cat, dog, cat, cat, dog, dog, dog, dog, cat, cat, dog, dog, dog, dog, dog, dog, cat, cat, cat, dog, cat, dog, dog, dog, dog, dog, dog, cat, cat, cat, dog, cat]
random6_labels = [dog, cat, cat, dog, dog, dog, dog, dog, dog, cat, cat, cat, cat, cat, cat, cat, dog, dog, cat, cat, dog, dog, dog, dog, cat, cat, dog, dog, cat, cat, cat, dog, dog, dog, cat, cat, cat, cat, dog, dog, cat, cat, dog, cat, cat, dog, dog, cat, dog, cat]

#Read data
df = pd.read_excel('images/random1/saved_params.xlsx')
num_rows = 50
cat_data = []
dog_data = []
for row in range(num_rows):
	row_data = []
	for col in range(1, df.shape[1]):
		row_data.append(df.iat[row, col])
	if random1_labels[row] == cat:
		cat_data.append(row_data)
	else:
		dog_data.append(row_data)
#cat_data = np.array(cat_data)
#dog_data = np.array(dog_data)
#print (cat_data.shape)
#print (dog_data.shape)

df = pd.read_excel('images/random3/saved_params.xlsx')
num_rows = 50
cat_data = []
dog_data = []
for row in range(num_rows):
	row_data = []
	for col in range(1, df.shape[1]):
		row_data.append(df.iat[row, col])
	if random3_labels[row] == cat:
		cat_data.append(row_data)
	else:
		dog_data.append(row_data)
#cat_data = np.array(cat_data)
#dog_data = np.array(dog_data)

df = pd.read_excel('images/random4/saved_params.xlsx')
num_rows = 50
cat_data = []
dog_data = []
for row in range(num_rows):
	row_data = []
	for col in range(1, df.shape[1]):
		row_data.append(df.iat[row, col])
	if random4_labels[row] == cat:
		cat_data.append(row_data)
	else:
		dog_data.append(row_data)
#cat_data = np.array(cat_data)
#dog_data = np.array(dog_data)

df = pd.read_excel('images/random5/saved_params.xlsx')
num_rows = 50
cat_data = []
dog_data = []
for row in range(num_rows):
	row_data = []
	for col in range(1, df.shape[1]):
		row_data.append(df.iat[row, col])
	if random5_labels[row] == cat:
		cat_data.append(row_data)
	else:
		dog_data.append(row_data)
#cat_data = np.array(cat_data)
#dog_data = np.array(dog_data)

df = pd.read_excel('images/random6/saved_params.xlsx')
num_rows = 50
cat_data = []
dog_data = []
for row in range(num_rows):
	row_data = []
	for col in range(1, df.shape[1]):
		row_data.append(df.iat[row, col])
	if random6_labels[row] == cat:
		cat_data.append(row_data)
	else:
		dog_data.append(row_data)
#cat_data = np.array(cat_data)
#dog_data = np.array(dog_data)

df = pd.read_excel('More_data.xlsx', sheet_name = "CAT")
for row in range(27):
	row_data = []
	for col in range(1, 14):
		row_data.append(df.iat[row, col])
	cat_data.append(row_data)

for row in range(29, 54):
	row_data = []
	for col in range(1, 14):
		row_data.append(df.iat[row, col])
	cat_data.append(row_data)

for row in range(56, 140):
	row_data = []
	for col in range(1, 14):
		row_data.append(df.iat[row, col])
	if not (math.isnan(row_data[0])):
		cat_data.append(row_data)
		#print ("data: ", row_data)

df = pd.read_excel('More_data.xlsx', sheet_name = "DOG")
for row in range(23):
	row_data = []
	for col in range(1, 14):
		row_data.append(df.iat[row, col])
	cat_data.append(row_data)
	#print ("data: ", row_data)

for row in range(25, 50):
	row_data = []
	for col in range(1, 14):
		row_data.append(df.iat[row, col])
	cat_data.append(row_data)
	#print ("data: ", row_data)

for row in range(52, 122):
	row_data = []
	for col in range(1, 14):
		row_data.append(df.iat[row, col])
	if not (math.isnan(row_data[0])):
		cat_data.append(row_data)
		#print ("data: ", row_data)

cat_data = np.array(cat_data)
dog_data = np.array(dog_data)

#assuming mu is 0

#Fit cat data
mean_cat = np.mean(cat_data, axis = 0)
cov_cat = np.cov(cat_data, rowvar = 0)
samples_cat = np.random.multivariate_normal(mean_cat, cov_cat, 50000)
pdf_cat = multivariate_normal.pdf(samples_cat, mean=mean_cat, cov=cov_cat)
np.save("pdf_cat", pdf_cat)

# print ("mean_cat: ", mean_cat)
# print ("cov_cat: ", cov_cat.shape)
# print (samples_cat)
#print (pdf_cat)
# plt.plot(samples_cat, pdf_cat)
# plt.show()
# print ("samples_cat: ", samples_cat[:, 0])
# print ("pdf_cat: ", pdf_cat)
# plt.ylim(min(pdf_cat), max(pdf_cat))
# plt.scatter(samples_cat[:, 0], pdf_cat)
# plt.show()
#Fit dog data
mean_dog = np.mean(dog_data, axis = 0)
cov_dog = np.cov(dog_data, rowvar = 0)
samples_dog = np.random.multivariate_normal(mean_dog, cov_dog, dog_data.shape[0])
pdf_dog = multivariate_normal.pdf(samples_dog, mean=mean_dog, cov=cov_dog)
np.save("pdf_dog", pdf_dog)
#print ("pdf_dog: ", pdf_dog)

#plt.plot(pdf_dog)
#plt.show()

