import warnings
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from sklearn.model_selection import train_test_split
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report
    )
from tensorflow.keras.layers import (
    Embedding,
    LSTM,
    Dense,
    Dropout,
    Bidirectional,
    GRU,
    BatchNormalization,
)
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from nltk.stem import WordNetLemmatizer
import plotly.express as px
import string
from tensorflow.keras.preprocessing.text import Tokenizer

warnings.filterwarnings("ignore")
nltk.download("stopwords", quiet=True)

"""KAREN2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1owU5eRMD6hN6pk5tQAom2NWc3R6LUQC6

Aleksandra Krasicka 148254

# NLP - final project

## About

Everyone sometimes has a hard time telling how the other person is feeling.
There are already many applications that help with that by assessing which
emotion seems something to be giving.

Example:

In this project I will try to perform sentimental analisys and
assesment of short texts like the one above.

There will be 6 cathegories:
- sadness (0)
- joy (1)
- love (2)
- anger (3)
- fear (4)
- surprise (5)

## Getting data
"""

df = pd.read_csv("text/text.csv", index_col=0)

"""## The Dataset

The dataset for this task is provided by Nidula Elgiriyewithana on kaggle.

link to the datase:
https://www.kaggle.com/datasets/nelgiriyewithana/emotions/data

"""

df.head(10)

fig = px.histogram(df, x="label", width=600, height=400)
fig.update_xaxes(
    type="category", categoryorder="array",
    categoryarray=["0", "1", "2", "3", "4", "5"]
)
fig.show()

df.isna().sum()

"""### Wordcloud"""

stopwordss = set(STOPWORDS)

"""#### Sadness (0)"""

wordcloud = WordCloud(
    width=800,
    height=800,
    background_color="white",
    stopwords=stopwordss,
    min_font_size=10,
    colormap="Blues",
)
wordcloud.generate(str(df[df["label"] == 0]["text"].values))
plt.figure(figsize=(8, 5), facecolor=None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)

plt.show()

"""#### Joy (1)"""

wordcloud = WordCloud(
    width=800,
    height=800,
    background_color="white",
    stopwords=stopwordss,
    min_font_size=10,
    colormap="YlGn_r",
)
wordcloud.generate(str(df[df["label"] == 1]["text"].values))
plt.figure(figsize=(8, 5), facecolor=None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)

plt.show()

"""#### Love (2)"""

wordcloud = WordCloud(
    width=800,
    height=800,
    background_color="white",
    stopwords=stopwordss,
    min_font_size=10,
    colormap="PuRd_r",
)
wordcloud.generate(str(df[df["label"] == 2]["text"].values))
plt.figure(figsize=(8, 5), facecolor=None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)

plt.show()

"""#### Anger (3)"""

wordcloud = WordCloud(
    width=800,
    height=800,
    background_color="white",
    stopwords=stopwordss,
    min_font_size=10,
    colormap="Reds_r",
)
wordcloud.generate(str(df[df["label"] == 3]["text"].values))
plt.figure(figsize=(8, 5), facecolor=None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)

plt.show()

"""#### Fear (4)"""

wordcloud = WordCloud(
    width=800,
    height=800,
    background_color="white",
    stopwords=stopwordss,
    min_font_size=10,
    colormap="gray",
)
wordcloud.generate(str(df[df["label"] == 4]["text"].values))
plt.figure(figsize=(8, 5), facecolor=None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)

plt.show()

"""#### Surprise (5)"""

wordcloud = WordCloud(
    width=800,
    height=800,
    background_color="white",
    stopwords=stopwordss,
    min_font_size=10,
    colormap="Wistia_r",
)
wordcloud.generate(str(df[df["label"] == 5]["text"].values))
plt.figure(figsize=(8, 5), facecolor=None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)

plt.show()

""""
## Preprocessing

What we don't want:
- stop words
- quotes
- punctuation
- parts of html
- emojis
- URLs
"""

nltk.download("punkt")
lemma = WordNetLemmatizer()
stemmer = nltk.PorterStemmer()
stop_words = stopwords.words("english")

df.duplicated().sum()

df = df.drop_duplicates()

"""### Remove parts of the text"""

# This parts of the code was also used in the first version of KAREN


def remove_URL(text):
    url = re.compile(r"https?://\S+|www\.\S+")
    return url.sub(r"", text)


def remove_emoji(text):
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE,
    )
    return emoji_pattern.sub(r"", text)


def remove_html(text):
    html_pattern = r"<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});"
    return re.sub(html_pattern, "", text)


def remove_punct(text):
    table = str.maketrans("", "", string.punctuation)
    return text.translate(table)


def remove_quotes(text):
    quotes = re.compile(r"[^A-Za-z0-9\s]+")
    return re.sub(quotes, "", text)


df["mod_text"] = df["text"].apply(lambda x: remove_URL(x))
df["mod_text"] = df["mod_text"].apply(lambda x: remove_emoji(x))
df["mod_text"] = df["mod_text"].apply(lambda x: remove_html(x))
df["mod_text"] = df["mod_text"].apply(lambda x: remove_punct(x))
df["mod_text"] = df["mod_text"].apply(lambda x: remove_quotes(x))
df["mod_text"] = df["mod_text"].str.lower()

"""### Stemming"""


def listToString(s):
    str1 = ""
    for ele in s:
        str1 += ele
    return str1


# Stemming
ps = PorterStemmer()
corpus = []
words = []

for i in range(0, len(df)):
    # Removing characters other than letters
    review = df["mod_text"].iloc[[i]].values
    review = listToString(review)
    # Splitting into words
    review = review.split()
    # Applying Stemming
    stemmed = [
        ps.stem(word) for word in review if
        word not in stopwords.words("english")]
    # Joining words
    review = " ".join(stemmed)
    # Appending all tweets to a list after preprocessing
    corpus.append(review)
    # Appending all words for word embeddings
    words.append(stemmed)

# Corpus sample
corpus[1:10]

print("Legth of Corpus:", len(corpus))

df["clean_text"] = corpus

df_stemmed = df.drop(["text"], axis=1)
df_stemmed = df_stemmed.drop(["mod_text"], axis=1)

df_stemmed.to_csv("steemed.csv")

df_stemmed = pd.read_csv("/content/steemed.csv")

corpus = list(df_stemmed["clean_text"])

corpus

"""### Applying TFIDF Vectorization"""

X = df_stemmed["clean_text"].astype("str")

y = df_stemmed["label"].astype("str")

X

y

y = y.replace(
    ["0", "1", "2", "3", "4", "5"],
    ["sadness", "joy", "love", "anger", "fear", "surprise"],
)

y_dummies = pd.get_dummies(y)

y_dummies = y_dummies.replace([True, False], [1.0, 0.0])

y_dummies

"""## Models"""

X_train, X_test, y_train, y_test = train_test_split(
    X, y_dummies, test_size=0.2, random_state=42, stratify=y
)

tokenizer = Tokenizer(num_words=50000)
tokenizer.fit_on_texts(X_train)
tokenizer.fit_on_texts(X_test)
X_train_sequences = tokenizer.texts_to_sequences(X_train)
X_test_sequences = tokenizer.texts_to_sequences(X_test)

maxlen = max(len(tokens) for tokens in X_train_sequences)
X_train_padded = pad_sequences(
    X_train_sequences,
    maxlen=maxlen,
    padding="post",
)
X_test_padded = pad_sequences(X_test_sequences, maxlen=maxlen, padding="post")

np.max(X_train_padded) + 1

X_train_padded

print(f"X_train_padded shape: {X_train_padded.shape}")
print(f"y_train shape: {y_train.shape}")

pd.DataFrame(X_train_padded)

"""### GRU"""

TFIDFclassifier = Sequential()
TFIDFclassifier.add(Embedding(
    input_dim=332898,
    output_dim=50,
    input_length=79))
TFIDFclassifier.add(Dropout(rate=0.5))

TFIDFclassifier.add(Bidirectional(GRU(120, return_sequences=True)))
TFIDFclassifier.add(Bidirectional(GRU(64, return_sequences=True)))

TFIDFclassifier.add(Dense(units=32, activation="relu"))
TFIDFclassifier.add(BatchNormalization())
TFIDFclassifier.add(Bidirectional(GRU(64)))
TFIDFclassifier.add(Dropout(rate=0.1))
TFIDFclassifier.add(Dense(units=6, activation="softmax"))

TFIDFclassifier.compile(
    optimizer="adam", loss="mean_squared_error", metrics=["accuracy"]
)

TFIDFclassifier.summary()

"""Dzielniki	1, 2, 3, 6, 113, 226, 339, 491, 678, 982,
1473, 2946, 55483, 110966, 166449, 332898"""

history_GRU = TFIDFclassifier.fit(
    X_train_padded,
    y_train,
    batch_size=1473,
    epochs=10,
    verbose=1,
    validation_data=(X_test_padded, y_test),
)

final_preds_GRU = TFIDFclassifier.predict(X_test_padded)

final_preds_GRU

max_pred_GRU = np.argmax(final_preds_GRU, axis=1)

max_pred_GRU

y_test_max = np.argmax(y_test, axis=1)

y_test_max

"""#### Classification report"""

target_names = ["Sadness", "Joy", "Love", "Anger", "Fear", "Surprise"]
acc_log_tfidf_GRU = accuracy_score(y_test_max, max_pred_GRU)
classification_log_tfidf_GRU = classification_report(
    y_test_max, max_pred_GRU, target_names=target_names
)
confusion_matrix_log_tfidf_GRU = confusion_matrix(y_test_max, max_pred_GRU)

print(
    " \n Accuracy : ",
    acc_log_tfidf_GRU,
    "\n",
    "Classification report \n",
    classification_log_tfidf_GRU,
    "\n",
    "Confusion matrix \n",
    confusion_matrix_log_tfidf_GRU,
)

"""#### Confusion matrix"""

cm = confusion_matrix(y_test_max, max_pred_GRU)
sns.heatmap(cm, annot=True, fmt="d", cmap="Reds")

"""#### Training and validation loss and accuracy"""

train_loss = history_GRU.history["loss"]
val_loss = history_GRU.history["val_loss"]
train_acc = history_GRU.history["accuracy"]
val_acc = history_GRU.history["val_accuracy"]

epochs = range(1, len(train_acc) + 1)

plt.plot(epochs, train_loss, "r", label="Training loss")
plt.plot(epochs, val_loss, "b", label="Validation loss")
plt.title("Training and validation loss")
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.legend()
plt.show()

plt.figure()
plt.plot(epochs, train_acc, "r", label="Training acc")
plt.plot(epochs, val_acc, "b", label="Validation acc")
plt.title("Training and validation accuracy")
plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.legend()
plt.show()

"""### LSTM"""

LSTMclassifier = Sequential()
LSTMclassifier.add(Embedding(input_dim=332898, output_dim=50, input_length=79))
LSTMclassifier.add(Dropout(rate=0.5))

LSTMclassifier.add(Bidirectional(LSTM(120, return_sequences=True)))
LSTMclassifier.add(Bidirectional(LSTM(64, return_sequences=True)))

LSTMclassifier.add(Dense(units=32, activation="relu"))
LSTMclassifier.add(BatchNormalization())
LSTMclassifier.add(Bidirectional(LSTM(64)))
LSTMclassifier.add(Dropout(rate=0.1))
LSTMclassifier.add(Dense(units=6, activation="softmax"))

LSTMclassifier.compile(
    optimizer="adam", loss="mean_squared_error", metrics=["accuracy"]
)

LSTMclassifier.summary()

history = LSTMclassifier.fit(
    X_train_padded,
    y_train,
    batch_size=113,
    epochs=10,
    verbose=1,
    validation_data=(X_test_padded, y_test),
)

final_preds = LSTMclassifier.predict(X_test_padded)

max_pred = np.argmax(final_preds, axis=1)

max_pred

y_test_max = np.argmax(y_test, axis=1)

y_test_max

"""#### Classification report"""

target_names = ["anger", "fear", "joy", "love", "sadness", "surprise"]
acc_log_tfidf = accuracy_score(y_test_max, max_pred)
classification_log_tfidf = classification_report(
    y_test_max, max_pred, target_names=target_names
)
confusion_matrix_log_tfidf = confusion_matrix(y_test_max, max_pred)

print(
    " \n Accuracy : ",
    acc_log_tfidf,
    "\n",
    "Classification report \n",
    classification_log_tfidf,
    "\n",
    "Confusion matrix \n",
    confusion_matrix_log_tfidf,
)

"""#### Confusion matrix"""

cm = confusion_matrix(y_test_max, max_pred)
sns.heatmap(cm, annot=True, fmt="d", cmap="Reds")

"""#### Training and validation loss and accuracy"""

train_loss = history.history["loss"]
val_loss = history.history["val_loss"]
train_acc = history.history["accuracy"]
val_acc = history.history["val_accuracy"]

epochs = range(1, len(train_acc) + 1)

plt.plot(epochs, train_loss, "r", label="Training loss")
plt.plot(epochs, val_loss, "b", label="Validation loss")
plt.title("Training and validation loss")
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.legend()
plt.show()

plt.figure()
plt.plot(epochs, train_acc, "r", label="Training acc")
plt.plot(epochs, val_acc, "b", label="Validation acc")
plt.title("Training and validation accuracy")
plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.legend()
plt.show()

"""### Mismatched

#### All predictions
"""

all_pred = pd.DataFrame(X_test)
all_pred["true"] = y_test_max
all_pred["GRU"] = max_pred_GRU
all_pred["LSTM"] = max_pred
df_no_dup = df.drop_duplicates(subset=["clean_text"], keep="first")
all_pred = pd.merge(
    all_pred, df_no_dup[["clean_text", "text"]], on="clean_text", how="left"
)

all_pred

"""#### GRU and LSTM both wrong"""

mismatched = all_pred[
    ((all_pred["true"] != all_pred["GRU"]) &
     (all_pred["true"] != all_pred["LSTM"]))
]

mismatched = mismatched.replace(
    [0, 1, 2, 3, 4, 5], ["anger", "fear", "joy", "love", "sadness", "surprise"]
)
mismatched

mismatched_same = mismatched[mismatched["GRU"] == mismatched["LSTM"]]
mismatched_diff = mismatched[mismatched["GRU"] != mismatched["LSTM"]]

mismatched_same

mismatched_diff

"""#### Which types are mismached the most"""

mismatched_grouped = (
    mismatched.groupby(["true", "GRU", "LSTM"])["text"]
    .count()
    .reset_index(name="count")
    .sort_values(by="count", ascending=False)
    .head(10)
)

mismatched_grouped

"""##### Examples"""

for _, row in mismatched_grouped.iterrows():
    true_value = row["true"]
    GRU_value = row["GRU"]
    LSTM_value = row["LSTM"]
    print(f"True: {true_value}, GRU: {GRU_value}, LSTM: {LSTM_value}")
    print(
        mismatched.loc[
            (mismatched["true"] == row["true"])
            & (mismatched["GRU"] == row["GRU"])
            & (mismatched["LSTM"] == row["LSTM"])
        ]
        .head(1)["text"]
        .values
    )

"""#### All instances where GRU and LSTM do not agree"""

notmatched = all_pred[((all_pred["LSTM"] != all_pred["GRU"]))]
print(notmatched)
