# # models.py
#
# from django.db import models
#
# class NewsArticle(models.Model):
#     text = models.TextField()
#     label = models.CharField(max_length=4, blank=True, null=True)
#
#
# # forms.py
#
# from django import forms
# from .models import NewsArticle
#
# class NewsArticleForm(forms.ModelForm):
#     class Meta:
#         model = NewsArticle
#         fields = ['text']
#
#
# # template.html
#
# <form method="post">
#     {% csrf_token %}
#     {{ form.as_p }}
#     <button type="submit">Predict</button>
# </form>
#
# # views.py
#
# from django.shortcuts import render
# from .forms import NewsArticleForm
# import joblib
#
#
# def predict_label(text):
#     # Load the trained model
#     model = joblib.load('path/to/trained/model.pkl')
#
#     # Preprocess the text
#     # ...
#
#     # Predict the label
#     label = model.predict([text])[0]
#
#     return label
#
#
# def predict(request):
#     if request.method == 'POST':
#         form = NewsArticleForm(request.POST)
#         if form.is_valid():
#             text = form.cleaned_data['text']
#             label = predict_label(text)
#
#             # Save the predicted label to the database
#             article = form.save(commit=False)
#             article.label = label
#             article.save()
#
#             return render(request, 'result.html', {'label': label})
#     else:
#         form = NewsArticleForm()
#
#     return render(request, 'predict.html', {'form': form})
#
#
#  # result.html
#
# <p>The predicted label is: {{ label }}</p>
#
# # views.py
#
# from django.shortcuts import render
# from .forms import NewsArticleForm
# import joblib
# import pandas as pd
# import numpy as np
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.model_selection import train_test_split
# from sklearn.naive_bayes import MultinomialNB
#
# # Load the fake news dataset
# df = pd.read_csv('path/to/fake_news_dataset.csv')
#
# # Preprocess the dataset
# df = df.dropna()
# df = df.drop_duplicates()
# df['text'] = df['title'] + ' ' + df['text']
# df = df[['text', 'label']]
# df['label'] = df['label'].map({'FAKE': 1, 'REAL': 0})
#
# # Split the dataset into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(df['text'], df['label'], test_size=0.2, random_state=42)
#
# # Create a TfidfVectorizer
# tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
#
# # Fit and transform the training data
# X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
#
# # Train a Multinomial Naive Bayes classifier
# clf = MultinomialNB()
# clf.fit(X_train_tfidf, y_train)
#
#
# def predict_label(text):
#     # Preprocess the text
#     text = text.lower()
#     text = ''.join([c for c in text if c.isalpha() or c.isspace()])
#
#     # Transform the text using the TfidfVectorizer
#     text_tfidf = tfidf_vectorizer.transform([text])
#
#     # Predict the label
#     label = clf.predict(text_tfidf)[0]
#
#     return label
#
#
# def predict(request):
#     if request.method == 'POST':
#         form = NewsArticleForm(request.POST)
#         if form.is_valid():
#             text = form.cleaned_data['text']
#             label = predict_label(text)
#
#             # Save the predicted label to the database
#             article = form.save(commit=False)
#             article.label = 'FAKE' if label == 1 else 'REAL'
#             article.save()
#
#             return render(request, 'result.html', {'label': article.label})
#     else:
#         form = NewsArticleForm()
#
#     return render(request, 'predict.html', {'form': form})
#
#
