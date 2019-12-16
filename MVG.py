from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal
import pandas as pd
import numpy as np
from scipy.stats import norm
import math
import pymc3 as pm
from matplotlib import pyplot as plt
import theano.tensor as tt
from statsmodels.sandbox.distributions.extras import mvnormcdf


cat = 'cat'
dog = 'dog'
random1_labels = [cat, dog, dog, dog, cat, dog, dog, dog, cat, dog, dog, cat, dog, cat, cat, dog, dog, dog, dog, dog, cat, dog, cat, cat, dog, dog, dog, dog, dog, cat, dog, dog, cat, dog, dog, cat, cat, cat, dog, dog, dog, cat, dog, cat, dog, dog, dog, dog, cat, cat]
random3_labels = [cat, cat, dog, dog, dog, dog, cat, dog, dog, cat, dog, dog, dog, cat, cat, cat, cat, dog, cat, cat, dog, dog, dog, dog, cat, dog, dog, cat, cat, dog, dog, dog, dog, dog, dog, cat, dog, dog, dog, dog, dog, cat, dog, cat, dog, dog, cat, cat, cat, dog]
random4_labels = [dog, dog, dog, dog, cat, dog, cat, dog, dog, dog, cat, dog, dog, dog, dog, cat, dog, dog, dog, dog, dog, cat, cat, dog, dog, cat, dog, cat, cat, dog, dog, dog, cat, cat, cat, cat, cat, cat, dog, dog, dog, dog, dog, cat, dog, cat, cat, dog, dog, dog]
random5_labels = [dog, cat, cat, dog, cat, cat, cat, dog, dog, cat, cat, cat, cat, cat, cat, dog, dog, dog, cat, dog, cat, cat, dog, dog, dog, dog, cat, cat, dog, dog, dog, dog, dog, dog, cat, cat, cat, dog, cat, dog, dog, dog, dog, dog, dog, cat, cat, cat, dog, cat]
random6_labels = [dog, cat, cat, dog, dog, dog, dog, dog, dog, cat, cat, cat, cat, cat, cat, cat, dog, dog, cat, cat, dog, dog, dog, dog, cat, cat, dog, dog, cat, cat, cat, dog, dog, dog, cat, cat, cat, cat, dog, dog, cat, cat, dog, cat, cat, dog, dog, cat, dog, cat]

#Read cat and dog data
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

df = pd.read_excel('images/random3/saved_params.xlsx')
num_rows = 50
for row in range(num_rows):
	row_data = []
	for col in range(1, df.shape[1]):
		row_data.append(df.iat[row, col])
	if random3_labels[row] == cat:
		cat_data.append(row_data)
	else:
		dog_data.append(row_data)

df = pd.read_excel('images/random4/saved_params.xlsx')
num_rows = 50
for row in range(num_rows):
	row_data = []
	for col in range(1, df.shape[1]):
		row_data.append(df.iat[row, col])
	if random4_labels[row] == cat:
		cat_data.append(row_data)
	else:
		dog_data.append(row_data)


df = pd.read_excel('images/random5/saved_params.xlsx')
num_rows = 50
for row in range(num_rows):
	row_data = []
	for col in range(1, df.shape[1]):
		row_data.append(df.iat[row, col])
	if random5_labels[row] == cat:
		cat_data.append(row_data)
	else:
		dog_data.append(row_data)

df = pd.read_excel('images/random6/saved_params.xlsx')
num_rows = 50
for row in range(num_rows):
	row_data = []
	for col in range(1, df.shape[1]):
		row_data.append(df.iat[row, col])
	if random6_labels[row] == cat:
		cat_data.append(row_data)
	else:
		dog_data.append(row_data)

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
	dog_data.append(row_data)
	print ("data: ", row_data)

for row in range(25, 50):
	row_data = []
	for col in range(1, 14):
		row_data.append(df.iat[row, col])
	dog_data.append(row_data)
	print ("data: ", row_data)

for row in range(52, 122):
	row_data = []
	for col in range(1, 14):
		row_data.append(df.iat[row, col])
	if not (math.isnan(row_data[0])):
		dog_data.append(row_data)
		print ("data: ", row_data)

total_data = cat_data.extend(dog_data)
total_data = np.array(total_data)
cat_data = np.array(cat_data)
dog_data = np.array(dog_data)


mean_dog = np.mean(dog_data, axis = 0)
mean_cat = np.mean(cat_data, axis = 0)


cov_dog = np.cov(dog_data, rowvar = 0)
cov_cat = np.cov(cat_data, rowvar = 0)


#Calculating correlation coefficient matrices

# corr_total = np.corrcoef(cat_data, rowvar = False)
# df = pd.DataFrame(corr_total)



# filepath = 'corr_cat.xlsx'

# df.to_excel(filepath, index=False)



samples_dog = np.random.multivariate_normal(mean_dog, cov_dog, 1000000)
samples_cat = np.random.multivariate_normal(mean_cat, cov_cat, 1000000)


#Probabiliy density function

# pdf_cat = multivariate_normal.pdf(samples_cat, mean=mean_cat, cov=cov_cat)
# #np.save("pdf_cat", pdf_cat)



with pm.Model() as model:
	u = pm.Normal('mu', mu=[0,0,0,0,0,0,0,0,0,0,0,0,0], shape = 13, testvals = samples_cat.mean(axis = 0))
	#sd_dist = pm.HalfCauchy.dist(beta=2.5, shape=13)
	#chol_packed = pm.LKJCholeskyCov('chol_packed', n=13, eta=2, sd_dist=sd_dist)
	#chol = pm.expand_packed_triangular(13, chol_packed)
	#cov = pm.Deterministic('cov', tt.dot(sigma_matrix, corr, sigma_matrix)) 
	#obs = pm.MvNormal('obs', u, chol = chol, observed=samples_cat)
	obs = pm.MvNormal('vals', mu = u, cov = cov_cat, shape = 13, observed = samples_cat)
	#step = pm.Metropolis()
	#startvals = pm.find_MAP(model=model)
	trace = pm.sample()
	print ("trace: ", trace['mu'].mean(axis = 0))
	print ("trace: ", trace['vals'])


