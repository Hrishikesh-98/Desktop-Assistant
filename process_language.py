#Natural Language Processing

#importing Essential Libraries
import pandas as pd

#importing the dataset
class Process():
    def fit_model(self):
        dataset = pd.read_csv("C:\\Users\\Satrangi\\Desktop\\orders.csv")
        #cleaning the text
        import re
        from nltk.stem.porter import PorterStemmer
        from nltk.corpus import stopwords
        corpus = []
        for i in range(0,117):
            review = re.sub('[^a-zA-Z]', ' ', dataset['Order'][i])
            review = review.lower()
            review = review.split()
            ps = PorterStemmer()
            review = [word for word in review if not word in set(stopwords.words('english'))]
            review = ' '.join(review)
            corpus.append(review)

        #creating bag of words model
        from sklearn.feature_extraction.text import CountVectorizer
        cv = CountVectorizer(max_features = 1500)
        X = cv.fit_transform(corpus).toarray()
        y = dataset.iloc[:, 1].values

        #fitting the classifier to the training set
        from sklearn.naive_bayes import GaussianNB
        classifier = GaussianNB()
        classifier.fit(X, y)
        print("fitting done")
        returns = list()
        returns.append(classifier)
        returns.append(cv)
        return returns

    def predict(self, query, classifier, cv):
        statement = query
        statements = list()
        statements.append(statement)
        statement = cv.transform(statements).toarray()
        y_pred = classifier.predict(statement)
        statements.clear()
        return y_pred[0]


