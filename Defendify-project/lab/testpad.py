import pandas as pd
import sklearn 
#as scikit_learn
import scipy
import altair as alt
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.multioutput import MultiOutputClassifier
from sklearn.linear_model import SGDClassifier
from sklearn import preprocessing
from sklearn.metrics import f1_score
#from jupyter_datatables import init_datatables_mode
#init_datatables_mode()

fileName = '20210313b_GraphSAGE_embed_features'

d = pd.read_csv(fileName+'.csv')
nd = d['features'].str.strip('[]').str.split(',').apply(pd.Series)
X=nd

#TSNE
X_embedded = TSNE(n_components=2, random_state=6).fit_transform(X)
#X_embedded = TSNE(n_components=2, random_state=6).fit_transform(list(X.embedding))
TSNE_components = pd.DataFrame(X_embedded, columns=['X_red_X', 'X_red_Y'])
#TSNE_components = TSNE_components.assign(X_red_X=X_embedded[:,0], X_red_Y=X_embedded[:,1])
TSNE_components['btc_id']=d['name']
TSNE_components['risk_rating']=d['exp']
TSNE_components['pageRank']=d['pr']
TSNE_components['out_deg']=d['outdeg']
TSNE_components['in_deg']=d['indeg']
TSNE_components['total_amount']=d['ta']

#Reduce the components to 2
pca = PCA(n_components=2)
X_red = pca.fit_transform(X)
# Save components to a DataFrame
PCA_components = pd.DataFrame(X_red, columns=['X_red_X', 'X_red_Y'])
PCA_components['btc_id']=d['name']
PCA_components['risk_rating']=d['exp']
PCA_components['pageRank']=d['pr']
PCA_components['out_deg']=d['outdeg']
PCA_components['in_deg']=d['indeg']
PCA_components['total_amount']=d['ta']

def elbow_fn(X_red):
    ks = range(1, 10)
    inertias = []
    for k in ks:
        # Create a KMeans instance with k clusters: model
        model = KMeans(n_clusters=k)

        # Fit model to samples
        model.fit(X_red)

        # Append the inertia to the list of inertias
        inertias.append(model.inertia_)

#Run Elbow function to determine the number of clusters (K) for analysis
#using the PCA fit
elbow_fn(X_red)
#using the TSNE fit
#elbow_fn(X_embedded)

#Determine Kmeans clustering
K=3
#X_red - PCA
#X_embedded - TSNE
kmeans = KMeans(n_clusters=K, random_state=0).fit(X_red)
#Cluster labels
lab = kmeans.labels_

#print("*****Cluster Centers*****")
#print(kmeans.cluster_centers_)
centers = kmeans.cluster_centers_

d2 = d.assign(X_red_X=X_red[:,0], X_red_Y=X_red[:,1], cluster_label=lab)
print(d2.head())

#df = pd.DataFrame(np.random.randn(100, 2))
msk = np.random.rand(len(d2)) < 0.8
train = d2[msk]
test = d2[~msk]
print(len(test))
print(len(train))
print(test.head(3))

le = preprocessing.LabelEncoder()
train['features'] = le.fit_transform(train['features'])
train['cluster_label'] = le.fit_transform(train['cluster_label'])

test['features'] = le.fit_transform(test['features'])
test['cluster_label'] = le.fit_transform(test['cluster_label'])

log = MultiOutputClassifier(SGDClassifier(loss="log_loss"), n_jobs=10)
log.fit(train[['features']], train[['cluster_label']])

print(f1_score(test[['cluster_label']],
               log.predict(test[['features']]), average="micro"))
print("****Predicted Labels****")
#print(log.predict(test[['features']]))
#df_total["pred_lin_regr"] = clf.predict(Xtest)
test['predicted_cluster_label'] = log.predict(test[['features']])
print(test[['name', 'exp', 'cluster_label','predicted_cluster_label']].head(20))
dx = test[['name', 'exp', 'cluster_label','predicted_cluster_label']]
dx.to_csv(fileName+"_output_predictor_3.csv")
