import json
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
import tensorflow as tf

with open('carrier_enhancement.json', 'r') as f:
    data = json.load(f)


resumes = []
careers = []

for entry in data:
    resume_text = " ".join([entry['name']] + [degree['degree_name'] for degree in entry['degrees']] + \
                          [cert['certification_name'] for cert in entry['certifications']] + \
                          entry['skills'] + \
                          [project['description'] for project in entry['projects']])
    resumes.append(resume_text)
    careers.append(entry['career'])


label_encoder = LabelEncoder()
careers_encoded = label_encoder.fit_transform(careers)

tfidf_vectorizer = TfidfVectorizer(max_features=10000)
resumes_tfidf = tfidf_vectorizer.fit_transform(resumes)

resumes_dense = resumes_tfidf.toarray()


resumes_dense_sorted_indices = np.argsort(resumes_dense)
resumes_dense_reordered = resumes_dense[:, resumes_dense_sorted_indices]

X_train, X_test, y_train, y_test = train_test_split(resumes_dense_reordered, careers_encoded, test_size=0.2, random_state=42)


model = Sequential()
model.add(Flatten(input_shape=X_train.shape[1:]))  
model.add(Dropout(0.5))
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(label_encoder.classes_), activation='softmax'))

model.compile(loss='sparse_categorical_crossentropy', optimizer=Adam(learning_rate=0.001), metrics=['accuracy'])

early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

history = model.fit(X_train, y_train, batch_size=32, epochs=20, validation_data=(X_test, y_test), callbacks=[early_stopping])


model.save('trained_model.h5')

loss, accuracy = model.evaluate(X_test, y_test)
print("Test Loss:", loss)
print("Test Accuracy:", accuracy)

