# -*- coding: utf-8 -*-
"""consumercomplaint.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UQBwaz-v9phmZn9NDfelKH4RPLRkHwVO

#IMPORTING LIBRARIES
"""

#1.Pandas for dataframe
import pandas as pd

    #2. NumPy to peform Calculations
import numpy as np

    #3. Seaborn to Visualize data
#import seaborn as sns

    #4. To split data
from sklearn.model_selection import train_test_split

    #5. For Logistic Regression
from sklearn.linear_model import LogisticRegression

    #6. For Plotting Graph
import matplotlib.pyplot as plt

    #7. For Natural Language Processing
import nltk
from nltk.corpus import stopwords

    #8. For Classification
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier

    #9. For Analysing Text
import regex as re
import string

    #10. For Deployment
import streamlit as st

# **DATA PREPROCESSING**"""

#Importing Data:
data_complaint= pd.read_excel('Complaints.xlsx')

  #Creating Copy:
data=data_complaint.copy()

  #Printing top 5 entries
print(data.head())

#Taking only columns required for prediction
data = data[["Product", "Issue", "Consumer complaint narrative"]]

#Printing total NULL values of each column
print(data.isnull().sum())

#Dropping NaN(Not a Number) values
data = data.dropna(axis=0)
print(data.isnull().sum())

#Checking objects data type
print(data.info())

#Typecasting Data
data['Product'] = data['Product'].astype('string')
data['Issue'] = data['Issue'].astype('string')
data['Consumer complaint narrative'] = data['Consumer complaint narrative'].astype('string')

  #Again checking objects data type
print(data.info())

#Count of Various Issues
print(data["Issue"].value_counts())

#Using NLP to pre-process text data
nltk.download('stopwords')
stemmer = nltk.SnowballStemmer("english")
stopword=set(stopwords.words('english'))

#Defining function to clean text
def clean(text):
    text = str(text).lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = [word for word in text.split(' ') if word not in stopword]
    text=" ".join(text)
    text = [stemmer.stem(word) for word in text.split(' ')]
    text=" ".join(text)
    return text

  #Calling clean(text) function
data["Consumer complaint narrative"] = data["Consumer complaint narrative"].apply(clean)

#Spliting data into train and test sets
x = np.array(data["Consumer complaint narrative"])
y = np.array(data["Product"])

#Training Model
cv = CountVectorizer()
X = cv.fit_transform(x)
X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    test_size=0.33,
                                                    random_state=42)

# **VISUALIZATION**"""

#Frequency distribution of Complaint Type
#SalStat=sns.countplot(data['Product'])

#Pie Chart representation of Consumer Complaint Type
#data.Product.value_counts().plot(kind='pie',autopct='%1.0f%%',figsize=(12, 8))
#plt.title("Complaint Type")
#plt.axis("equal")  # Equal aspect ratio ensures a circular pie chart
#plt.show()"""

# **APPLYING CLASSIFICATION ALGORITHM**"""

#Stochastic Gradient Descent (SGD) Classifier Algorithm
sgdmodel = SGDClassifier()
sgdmodel.fit(X_train,y_train)

# **ACCURACY**"""

print("Accuracy of SGD model:",sgdmodel.score(X_test,y_test)*100,"%")

# **PREDICTION OF COMPLAINT**"""

#Taking User Input
st.header("Consumer Complaint Classification")
user =st.text_input("Enter Complaint Narrative: ")
b1=st.button("Submit")
if b1:
    data = cv.transform([user]).toarray()
    output = sgdmodel.predict(data)
    
    #Printing the type of complaint
    st.write("Type of Complaint:\n")
    st.write(output[0])
