import os
import pandas as pd
from sklearn.model_selection import train_test_split

files = os.listdir('archive')
data = pd.DataFrame()
for file in files:
    df = pd.read_csv('archive/' + file, sep='\t', header=None, on_bad_lines='skip')
    df.columns = ['marketplace','customer_id', 'review_id', 'product_id', 'product_parent', 'product_title','product_category', 'star_rating', 'helpful_votes',' total_votes', 'vine', 'verified_purchase', 'review_headline', 'review_body', 'review_date']
    df.drop(0, axis=0, inplace=True)
    df['review_date'] = pd.to_datetime(df['review_date'], errors='coerce')
    df.dropna(inplace=True)
    df['review_quarter'] = df['review_date'].dt.to_period('Q')
    class_counts = df['review_quarter'].value_counts()
    classes_to_keep = class_counts[class_counts > 1].index
    df = df[df['review_quarter'].isin(classes_to_keep)]
    small_df, _ = train_test_split(df, train_size=0.05, stratify=df['review_quarter'])
    data = pd.concat([data, small_df], axis=0)

data.drop('review_date', axis=1, inpace=True)
data.sort_values(by='review_quarter', ascending=True, inplace=True)
data.reset_index(drop=True, inplace=True)
data.to_csv('amazon_reviews.csv', index=False)
