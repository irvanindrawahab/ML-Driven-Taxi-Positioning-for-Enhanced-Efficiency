# Streaming Wars: A Subreddit Analysis

### Problem Statement

Disney+ Data Science Team is evaluating the current streaming wars with its competitor Netflix. Instead of using financial and content analysis, the Team will be assessing the Reddit posts and comments to gain understanding of public perception, user preferences, and emerging trends.

### Data Preparation
#### Data Collection
Public Perception assessment and evaluation from Reddit posts and comments

Why Reddit?
- Every day, millions of people around the world post, vote, and comment in communities organized around their interests
- Reddit has a user-created areas of interest where discussions on Reddit are organized, in this case we can look into r/DisneyPlus and r/netflix Subreddits

How to collect the posts data? 
- Webscraping of the posts content, such as
A) Title - post title
B) Selftext - the body of the post which elaborates the post further
C) Upvote Ratio - represents the ratio of upvotes to the total votes cast
D) Created Date - shows when the post is created

#### Data Cleaning

Remove duplicate entries based on the user id post to make sure that each of the post is unique.
Remove the field with empty input, e.g., some of the users only post the Title without any Selftext

#### Preprocessing

Combine Title and Selftext into one feature called “post” as our X variable
Add feature called “label” to classify post as Y variable

### Exploratory Data Analysis

A) Upvote Ratio
- Represents the ratio of upvotes to the total votes cast
- The average of upvote ratio for both DisneyPlus and Netflix datasets are above 0.50, indicating that the posts are well-received by the other Reddit users

B) Frequent Words
- Tokenize, lemmatize and remove stop words
- Use POS to collect the most frequent adjectives in the posts
- Disney+ has more “New” and “Original” but less of “Good”

C) Sentiment Analysis
- VADER Lexicon is a lexicon specifically designed for sentiment analysis of social media texts
- It does not only provide a sentiment score for each word but also considers context, punctuation, capitalization, degree modifiers, and emoticons
- VADER is widely used and performs well with informal texts like tweets and online reviews
- Both Disney+ and Netflix posts have 1.0 compound score using VADER lexicon, indicating that the overall sentiment is positive


### Modeling
#### Process
A) Split the data into train and test with equal proportion of Disney+ and Netflix on both sets (~50-50)
B) Fit the different combinations of vectorizer and classifier below
Vectorizer: Countvectorizer, TF-IDF
Classifier: Multinomial Naive Bayes, Logistic Regression, KNN, Random Forest, Bagging, and Gradient Boosting
C) Hyperparameter tuning on the best performing model combination

#### Metrics 
Accuracy. Why?
A) Easy to interpret
B) Good for balanced datasets
C) Treats all prediction errors equally

Before we build our model, we would want to set the baseline model to ensure that the model that we are building indeed brings value
1. Baseline Model
The baseline model is defined as the accuracy of simply predicting if the post contains keyword 'disney' or 'netflix'. The baseline accuracy is 5%.
   
2. Create and Build Model
Amongst all different combinations, TF-IDF classifier with Logistic Regression classifier performs the best on the test dataset as it gives the highest accuracy.

3. Hyperparameter Tuning
Further fine tune the model by running different combinations of parameters through pipeline and GridSearch. The accuracy with the most optimized hyperparameters is 87%

#### Modeling Conclusion
Why TF-IDF could perform better than CountVectorizer?
TF-IDF gives higher weights to terms that are frequent in a document but rare in the corpus, effectively reducing the importance of common words like and highlighting the importance of words that are more specific to the documents

Why LogisticRegression could perform better than the rest of the classifiers?
Text data is typically high-dimensional and sparse, meaning that most features (words or n-grams) have zero or very low frequency. Logistic regression can handle sparse data well, especially when using techniques like TF-IDF (Term Frequency-Inverse Document Frequency) to represent text features.
Logistic regression tends to be robust to noisy features because it estimates the probability of the class label based on the weighted sum of all features, effectively ignoring irrelevant features with low weigh n: Logistic regression calso an be regularized using techniques like L1 (Lasso) or L2 (Ridge) regularization, which penalize large parameter values.

### Recommendations
- Provide insights on public perception and preferences towards Disney+
- Predict public opinion or comments and perform classification
- Optimize marketing and content creation strategy towards a more targeted public
- Study the competitor dynamics, customer experience and preference

### Limitations
- Data scraped for this analysis are <2,000 - to scrape more data on further studies / analysis
- Reddit users come from diverse backgrounds and have different type of writing styles
- Potential biases amongst communities towards certain items