from sklearn.svm import SVC
from sklearn.pipeline import Pipeline



class Vectorizer(object):
	def __init__(self):

	def fit(self,X,y):
		return self

	def transform(self,X):
		return self


lsvc_tfidf = Pipeline([("ifidf_vectorizer", Vectorizer()), ("linear svc", SVC(kernel="linear",gamma='auto'))])
rsvc_tfidf = Pipeline([("ifidf_vectorizer", TfidfVectorizer()), ("linear svc", SVC(kernel="rbf",gamma='auto'))])
etree_tfidf = Pipeline([("word2vec vectorizer", TfidfVectorizer()), ("extra trees", ExtraTreesClassifier(n_estimators=200))])


all_models = [('lsvc_w2v', lsvc_w2v), ('rsvc_w2v', rsvc_w2v), ('etree_w2v', etree_w2v)]

for name, model in all_models:
	print(cross_val_score(model, X, y, cv= 5, scoring= accuracy).mean(),cross_val_score(model, X, y, cv= 5, scoring= precision).mean(),cross_val_score(model, X, y, cv= 5, scoring= f_score).mean())






