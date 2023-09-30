# 
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import re , openai

class ContentAnalyzer:
    def __init__(self, data):
        self.df = data
        openai.api_key =  ''

    def calculate_engagement_score(self):
        self.df['EngagementScore'] = self.df['likeCount'] + self.df['retweetCount'] + self.df['replyCount'] + self.df['quoteCount']

    def remove_urls(self, text):
        url_pattern = r'https?://\S+|www\.\S+'
        return re.sub(url_pattern, '', text)

    def preprocess_content(self):
        self.df['content'] = self.df['content'].apply(self.remove_urls)

    def analyze_topics(self, num_topics=3):
        vectorizer = CountVectorizer(max_features=10, stop_words='english')
        tf_matrix = vectorizer.fit_transform(self.df['content'])
        
        lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
        lda.fit(tf_matrix)
        
        topic_words = []
        for topic_idx, topic in enumerate(lda.components_):
            top_words_idx = topic.argsort()[-5:][::-1]
            top_words = [vectorizer.get_feature_names_out()[i] for i in top_words_idx]
            topic_words.append(top_words)
        
        for topic_idx, words in enumerate(topic_words):
            print(f"Topic {topic_idx + 1}: {', '.join(words)}")
        
        return topic_words

    def analyze_top_tweets(self, num_top_tweets=2):
        top_tweets = self.df.nlargest(num_top_tweets, 'EngagementScore')
        
        i = 0
        for idx, row in top_tweets.iterrows():
            print(idx)
            print(f"Content Strategy for Top Tweet {str(idx)}:")
            print(f"Topic: {', '.join(self.topic_words[i])}")
            i += 1
            print(f"Engagement Score: {row['EngagementScore']}")
            print(f"Tweet Text: {row['content']}")
            print("\n")

        return top_tweets

    def export_content_to_file(self, output_file="new_content.txt"):
        with open(output_file, 'w', encoding='utf-8') as file:
            for content in self.df['content']:
                file.write(content + '\n')
        print(f"Contents from df['content'] have been written to {output_file}")

    def generate_content_strategies(self, topic_words):
        content_strategies = {}
        
        for topic_idx, words in enumerate(topic_words):
            prompt = f"Suggest content strategies to cater to those interests while expanding reach for {', '.join(words)}."
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=50,
                n=1
            )
            content_strategies[topic_idx] = response.choices[0].text.strip()
        
        return content_strategies

if __name__ == "__main__":
    data = pd.read_csv('../data/cleaned_data.csv')

    content_analyzer = ContentAnalyzer(data)

    # Perform content analysis
    content_analyzer.calculate_engagement_score()
    content_analyzer.preprocess_content()
    content_analyzer.topic_words = content_analyzer.analyze_topics()
    top_tweets = content_analyzer.analyze_top_tweets()
    content_analyzer.export_content_to_file()

    # Generate content strategies
    content_strategies = content_analyzer.generate_content_strategies(content_analyzer.topic_words)

    # Print the content strategies
    for topic, strategy in content_strategies.items():
        print(f"Content Strategy for Topic {topic + 1}:")
        print(strategy)
        print("\n")
