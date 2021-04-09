import pandas as pd
import numpy as np
import pickle
import nltk
import keras

from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import preprocessing

nltk.download('stopwords')
nltk.download('punkt')

stop_words = stopwords.words('english')
porter_stemmer = PorterStemmer()

df = pd.read_csv('./imdb-dataset.csv', delimiter=',')
df = df.head(30000)


def identify_tokens(row):
    source = row[0]
    tokens = word_tokenize(source)
    token_words = [w for w in tokens if w.isalpha()]
    return token_words


def remove_stops(row):
    source_tokenization = row[2]
    stop = [w for w in source_tokenization if not w in stop_words]
    return (stop)


def stem_porter(row):
    my_list = row[2]
    stemmed_list = [porter_stemmer.stem(word) for word in my_list]
    return (stemmed_list)


def rejoin_words(row):
    my_list = row[2]
    joined_words = (" ".join(my_list))
    return joined_words


def pre_processing(df):
    print('Tokenization')
    df['text1'] = df.apply(identify_tokens, axis=1)
    print('Remove stop words')
    df['text1'] = df.apply(remove_stops, axis=1)
    print('Stemming')
    df['text1'] = df.apply(stem_porter, axis=1)
    print('Rejoin words')
    df['tidy_text'] = df.apply(rejoin_words, axis=1)

    return df


df = pre_processing(df)
df['tidy_text'] = df['tidy_text'].str.lower()

X = df['tidy_text']
Y = df['sentiment']

X_train, X_test, Y_train, Y_test = train_test_split(X,
                                                    Y,
                                                    test_size=0.1,
                                                    random_state=48,
                                                    stratify=Y)

tfidf = TfidfVectorizer(ngram_range=(2, 3),
                        sublinear_tf=True,
                        max_features=10000)

X_train_tf = tfidf.fit_transform(X_train)
X_test_tf = tfidf.transform(X_test)

le = preprocessing.LabelEncoder()

le.fit(list(Y_train))
Y_train_le = le.transform(list(Y_train))
Y_test_le = le.transform(list(Y_test))

num_class = Y.value_counts().shape
input_shape = X_train_tf.shape

from keras.utils import to_categorical

Y_train_label_keras = to_categorical(Y_train_le)
Y_test_label_keras = to_categorical(Y_test_le)

from keras import models
from keras import layers

network = models.Sequential()

network.add(layers.Dense(2, activation='relu', input_shape=(input_shape[1], )))
network.add(layers.Dropout(0.4))

network.add(layers.Dense(5, activation='relu'))
network.add(keras.layers.Dropout(0.4))

network.add(layers.Dense(5, activation='sigmoid'))
network.add(layers.Dropout(0.4))

network.add(layers.Dense(num_class[0], activation='softmax'))

network.compile(optimizer='adamax',
                loss="binary_crossentropy",
                metrics=['accuracy'])

network.summary()

network.fit(X_train_tf.toarray(),
            Y_train_label_keras,
            verbose=1,
            epochs=50,
            validation_split=0.3)

network.save('./network_model.h5')
pickle.dump(tfidf, open('./vectorizer.pkl', 'wb'))
