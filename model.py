import pandas as pd
from sklearn.model_selection import train_test_split
import urlexpander
from urllib.parse import urlparse
from sklearn import metrics
from sklearn.feature_selection import RFE
from sklearn.ensemble import RandomForestClassifier
import pickle
data=pd.read_csv('E:/1notes/attack/dataset_full1.csv')
data=data.dropna()
X=data.drop(['phishing'],axis=1)
y=data['phishing']
# print(X.columns.values.tolist())
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=0)
print('********start*********')
for i in range(88,89):
    print('iteration',i)
    rfc=RandomForestClassifier()
    rfe=RFE(estimator=rfc,n_features_to_select=i)
    rfe.fit(X_train,y_train)
    pickle.dump(rfe, open('model1.pkl','wb'))
    
model=pickle.load(open('model1.pkl', 'rb'))
acc=metrics.accuracy_score(y_test,model.predict(X_test))
print('i',' = ',acc)
print(rfe.support_)

