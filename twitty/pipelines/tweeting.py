import os , pandas as pd
import tweepy , time
# Set environment variables
os.environ['TWITTER_API_KEY'] = ''
os.environ['TWITTER_API_KEY_SECRET'] = ''
os.environ['TWITTER_CONSUMER_ID'] = ''
os.environ['TWITTER_CLIENT_SECRET'] = ''
os.environ['TWITTER_BEAR_TOKEN'] = ''
os.environ['TWITTER_ACCESS_TOKEN'] = ''
os.environ['TWITTER_ACCESS_TOKEN_SECRET'] = ''
os.environ['OPENAI_API_KEY'] = ''
os.environ['PERSONA_TOKEN_AIRTABLE'] = ''
os.environ['TOKEN2'] = '.'
os.environ['TABLE'] = 'twisty'

twitter_api_key = os.environ.get('TWITTER_API_KEY')
twitter_api_key_secret = os.environ.get('TWITTER_API_KEY_SECRET')
twitter_consumer_id = os.environ.get('TWITTER_CONSUMER_ID')
twitter_client_secret = os.environ.get('TWITTER_CLIENT_SECRET')
twitter_bear_token = os.environ.get('TWITTER_BEAR_TOKEN')
twitter_access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
twitter_access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
openai_api_key = os.environ.get('OPENAI_API_KEY')
persona_token_airtable = os.environ.get('PERSONA_TOKEN_AIRTABLE')
token2 = os.environ.get('TOKEN2')
table = os.environ.get('TABLE')


client = tweepy.Client(twitter_bear_token , twitter_api_key ,twitter_api_key_secret,twitter_access_token,twitter_access_token_secret)

auth = tweepy.OAuth1UserHandler(twitter_api_key ,twitter_api_key_secret,twitter_access_token,twitter_access_token_secret)

api = tweepy.API(auth)


file_path = 'trend_with_interest.csv'
df = pd.read_csv(file_path).drop(['Unnamed: 0'], axis=1)

def post_tweet(username, content):
    try:
            tweet = f'{content} @{username}' 
            client.create_tweet(text=tweet)
            print(f"Tweet posted: {tweet}")

    except tweepy.errors.TweepyException as e:
        print(f"Error posting tweet: {e}")

for index, row in df.iterrows():
    username = row['name']
    content = row['content_strategy']
    post_tweet(username, content)
    
    time.sleep(5)  
