from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal
import pandas as pd
import numpy as np
from scipy.stats import norm


cat = 'cat'
dog = 'dog'
labels = [cat, dog, dog, dog, cat, dog, dog, dog, cat, dog, dog, cat, dog, cat, cat, dog, dog, dog, dog, dog, cat, dog, cat, cat, dog, dog, dog, dog, dog, cat, dog, dog, cat, dog, dog, cat, cat, cat, dog, dog, dog, cat, dog, cat, dog, dog, dog, dog, cat, cat]

#Read data
df = pd.read_excel('images/random1/saved_params.xlsx')
num_rows = 50
cat_data = []
dog_data = []
for row in range(num_rows):
	row_data = []
	for col in range(1, df.shape[1]):
		row_data.append(df.iat[row, col])
	if labels[row] == cat:
		cat_data.append(row_data)
	else:
		dog_data.append(row_data)
cat_data = np.array(cat_data)
dog_data = np.array(dog_data)
#print (cat_data.shape)
#print (dog_data.shape)

#assuming mu is 0

#Fit cat data
mean_cat = np.mean(cat_data, axis = 0)
cov_cat = np.cov(cat_data, rowvar = 0)
samples_cat = np.random.multivariate_normal(mean_cat, cov_cat, 50000)
pdf_cat = multivariate_normal.pdf(samples_cat, mean=mean_cat, cov=cov_cat)

# print ("mean_cat: ", mean_cat)
# print ("cov_cat: ", cov_cat.shape)
# print (samples_cat)
#print (pdf_cat)
# plt.plot(samples_cat, pdf_cat)
# plt.show()
print ("samples_cat: ", samples_cat[:, 0])
print ("pdf_cat: ", pdf_cat)
plt.ylim(min(pdf_cat), max(pdf_cat))
plt.scatter(samples_cat[:, 0], pdf_cat)
plt.show()
#Fit dog data
mean_dog = np.mean(dog_data, axis = 0)
cov_dog = np.cov(dog_data, rowvar = 0)
samples_dog = np.random.multivariate_normal(mean_dog, cov_dog, dog_data.shape[0])
pdf_dog = multivariate_normal.pdf(samples_dog, mean=mean_dog, cov=cov_dog)
#print ("pdf_dog: ", pdf_dog)

#plt.plot(pdf_dog)
#plt.show()

