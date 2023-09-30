import sqlite3
import pandas as pd
import random
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import logging

# Initialize the logger
logging.basicConfig(filename='twitter_analysis.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Create a class to handle database operations
class TweetDatabase:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

        # Create the table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tweets (
                tweet_id INTEGER PRIMARY KEY,
                tweet_text TEXT,
                likes INTEGER,
                user_name VARCHAR(255),
                retweets INTEGER
            )
        ''')

    def insert_data(self, data):
        # Insert data into the SQLite table using executemany
        self.cursor.executemany('INSERT INTO tweets (tweet_id, tweet_text, likes, user_name, retweets) VALUES (?, ?, ?, ?, ?)', data)
        self.conn.commit()

    def fetch_data(self):
        self.cursor.execute('SELECT * FROM tweets')
        rows = self.cursor.fetchall()
        return rows

    def close_connection(self):
        self.conn.close()

# Create a class to handle tweet analysis
class TweetAnalysis:
    def __init__(self, tweet_data):
        self.tweet_data = tweet_data

    def tokenize_text(self, text):
        # nltk.download('stopwords')
        # nltk.download('punkt')
        stop_words = set(stopwords.words('english'))
        words = word_tokenize(text)
        filtered_text = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]
        return filtered_text

    def perform_ab_test(self, metric_test, metric_control):
        t_stat, p_value = ttest_ind(metric_test, metric_control)
        return t_stat, p_value

    def calculate_engagement_metrics(self, test_group_results, control_group_results):
        likes_test = [result['likes'] for result in test_group_results]
        likes_control = [result['likes'] for result in control_group_results]
        
        total_likes_test = sum(likes_test)
        total_likes_control = sum(likes_control)

        ctr_test = total_likes_test / len(self.tweet_data)
        ctr_control = total_likes_control / len(self.tweet_data)

        incremental_lift = ctr_test - ctr_control

        return ctr_test, ctr_control, incremental_lift ,total_likes_test , total_likes_control

# Create a class for A/B testing suggestions
class ABSuggestions:
    def ai_suggest_ab_tests(self, historical_data):
        suggestions = [
            "Try using emojis in the tweet content.",
            "Test different call-to-action phrases.",
            "Experiment with video content in tweets.",
            "Explore using user-generated content (UGC) in tweets.",
            "Adjust the posting times for tweets to target different time zones.",
        ]
        return suggestions

# Main code
if __name__ == "__main__":
    df_gender = pd.read_csv('../data/gender-classifier-DFE-791531.csv', encoding='iso-8859-1')
    db = df_gender[['_unit_id', 'text', 'fav_number', 'retweet_count', 'name']]

    # Initialize and populate the database
    db_name = 'twitty.db'
    db_conn = TweetDatabase(db_name)
    columns = ['_unit_id', 'text', 'fav_number', 'name', 'retweet_count']
    filtered_data = db[columns]
    data_tuples = [tuple(row) for row in filtered_data.values]
    db_conn.insert_data(data_tuples)

    # Fetch tweet data from the database
    tweet_data = db_conn.fetch_data()
    db_conn.close_connection()

    # Create instances of classes
    tweet_analysis = TweetAnalysis(tweet_data)
    ab_suggestions = ABSuggestions()

    # Tokenize text and analyze engagement
    for row in tweet_data:
        tweet_id, tweet_text, likes, user_name, retweets = row
        filtered_text = tweet_analysis.tokenize_text(tweet_text)
        logger.info(f"Filtered Text for Tweet ID {tweet_id}: {filtered_text}")

    # Perform A/B testing and calculate engagement metrics
    test_group_results = []
    control_group_results = []
    random.shuffle(tweet_data)
    test_group = tweet_data[:len(tweet_data)//2]
    control_group = tweet_data[len(tweet_data)//2:]

    for tweet in test_group:
        test_group_results.append({'likes': random.randint(1, 10), 'retweets': random.randint(1, 5)})

    for tweet in control_group:
        control_group_results.append({'likes': random.randint(1, 30), 'retweets': random.randint(1, 15)})

    ctr_test, ctr_control, incremental_lift ,total_likes_test , total_likes_control= tweet_analysis.calculate_engagement_metrics(test_group_results, control_group_results)
    logger.info(f"CTR Test: {ctr_test}")
    logger.info(f"CTR Control: {ctr_control}")
    logger.info(f"Incremental Lift: {incremental_lift}")

    # Get A/B testing suggestions
    ai_suggestions = ab_suggestions.ai_suggest_ab_tests(tweet_data)
    logger.info("AI-Driven A/B Test Suggestions:")
    for suggestion in ai_suggestions:
        logger.info("- " + suggestion)

    # Create a bar chart to visualize engagement metrics
    labels = ['Test Group', 'Control Group']
    likes = [total_likes_test, total_likes_control]

    plt.bar(labels, likes)
    plt.xlabel('Group')
    plt.ylabel('Total Likes')
    plt.title('Engagement Metrics - Likes')
    plt.show()
