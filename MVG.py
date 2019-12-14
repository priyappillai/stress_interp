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
	dog_data.append(row_data)
	#print ("data: ", row_data)

for row in range(25, 50):
	row_data = []
	for col in range(1, 14):
		row_data.append(df.iat[row, col])
	dog_data.append(row_data)
	#print ("data: ", row_data)

for row in range(52, 122):
	row_data = []
	for col in range(1, 14):
		row_data.append(df.iat[row, col])
	if not (math.isnan(row_data[0])):
		dog_data.append(row_data)
		#print ("data: ", row_data)

cat_data = np.array(cat_data)
dog_data = np.array(dog_data)

#assuming mu is 0

#Fit cat data
mean_cat = np.mean(cat_data, axis = 0)
print ("mean_cat: ", mean_cat)
cov_cat = np.cov(cat_data, rowvar = 0)
var_cat = np.var(cat_data, axis = 0)
print ("var_cat: ", var_cat)
#print ("cov_cat: ", cov_cat)
samples_cat = np.random.multivariate_normal(mean_cat, cov_cat, 1000000)
#print (np.mean(samples_cat, axis = 0))
# pdf_cat = multivariate_normal(mean=mean_cat, cov=cov_cat)
# print (pdf_cat.pdf([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]))
#np.save("pdf_cat", pdf_cat)

ndim = 13
with pm.Model() as model:
	u = pm.Normal('mu', mu=[0,0,0,0,0,0,0,0,0,0,0,0,0], shape = 13, testval = samples_cat.mean(axis = 0))
	#sd_dist = pm.HalfCauchy.dist(beta=2.5, shape=13)
	#chol_packed = pm.LKJCholeskyCov('chol_packed', n=13, eta=2, sd_dist=sd_dist)
	#chol = pm.expand_packed_triangular(13, chol_packed)
	#cov = pm.Deterministic('cov', tt.dot(sigma_matrix, corr, sigma_matrix)) 
	#obs = pm.MvNormal('obs', u, chol = chol, observed=samples_cat)
	obs = pm.MvNormal('vals', mu = u, cov = np.cov(samples_cat), shape = 13, observed = samples_cat)
	#step = pm.Metropolis()
	#startvals = pm.find_MAP(model=model)
	trace = pm.sample()
	print ("trace: ", trace['mu'].mean(axis = 0))
	print ("trace: ", trace['vals'])

#print (pdf_cat)


# var, U = np.linalg.eig(cov_cat)
# print ("var: ", var)
# print ("U: ", U)
# SEED = 3264602
# np.random.seed(SEED)



# with pm.Model() as model:
#     packed_L = pm.LKJCholeskyCov('packed_L', n=13, eta=1, sd_dist=pm.HalfCauchy.dist(2.5))

# print ("packed_L: ", packed_L.tag.test_value.shape)
# print ("packed_L: ", packed_L.tag.test_value)

# with model:
#     L = pm.expand_packed_triangular(13, packed_L)
#     cov = pm.Deterministic('cov', L.dot(L.T))

# print ("L: ", L.tag.test_value.shape)
# print ("L: ", L.tag.test_value)
# print ("cov: ", cov.tag.test_value)
# #independent, vague normal priors
# #test vals = initial values for random variables, helps when pymc3 automatically tries to initialize models
# with pm.Model() as model:
#     #u = pm.Normal('u', 0., 1., shape=13, testval=samples_cat.mean(axis=0))
#     u = pm.Normal('u', 0, 1, shape=13)
#     cov_final = np.outer(cov_cat, cov_cat)
#     #cov = pm.Deterministic('cov', cov_final)
#     obs = pm.MvNormal('obs', mu=u, cov = cov_cat.dot(cov_cat.T))#, observed=samples_cat)
#     #u = pm.Normal('u', 0, 1)
#     #sigma = pm.Exponential('sigma', lam=0.01)
#     #obs = pm.Uniform('obs', lower = 0, upper = 100, observed = samples_cat)

# # with model:
# #     u = pm.Normal('u', 0., 10., shape=13, testval = mean_cat)
# #     obs = pm.MvNormal('obs', u, chol=L, observed=samples_cat)
# # print ('u: ', u.tag.test_value)
# # print ('u: ', u.ravel())
# # #u.ravel()[5] = 0
# with model:
#     trace = pm.sample()
# # with model:
# #     #trace = pm.sample()
# # with model:
# #     trace = pm.sample(random_seed=SEED, cores=4)
# # # pm.traceplot(trace);


# u_post = trace['u'].mean(axis=0)
# cov_post = trace['cov'].mean(axis=0)
# var_post, U_post = np.linalg.eig(cov_post)

# print ("mean post: ", u_post)
# print ("cov_post: ", cov_post)
# print ("var_post: ", var_post)
# print ("U_post: ", U_post)


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
# mean_dog = np.mean(dog_data, axis = 0)
# cov_dog = np.cov(dog_data, rowvar = 0)
# samples_dog = np.random.multivariate_normal(mean_dog, cov_dog, dog_data.shape[0])
# pdf_dog = multivariate_normal.pdf(samples_dog, mean=mean_dog, cov=cov_dog)
# np.save("pdf_dog", pdf_dog)
#print ("pdf_dog: ", pdf_dog)

#plt.plot(pdf_dog)
#plt.show()

