import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
data = pd.read_csv('../data/cleaned_data.csv',index_col=0)

data['timestampy'] = pd.to_datetime(data.index)
data['hour'] = data['timestampy'].dt.hour
data['day_of_week'] = data['timestampy'].dt.day_name()
data['engagement_rate'] = data['likeCount'] + data['retweetCount'] + data['quoteCount']

hourly_engagement = data.groupby('hour')['engagement_rate'].mean()
logger.info(f"Hourly Engagement Rate:\n{hourly_engagement}")

daily_engagement = data.groupby('day_of_week')['engagement_rate'].mean()
logger.info(f"Daily Engagement Rate:\n{daily_engagement}")

optimal_tweeting_time = hourly_engagement.idxmax()
logger.info(f"Optimal Tweeting Time: {optimal_tweeting_time} o'clock")

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

plt.figure(figsize=(10, 6))
sns.lineplot(x=hourly_engagement.index, y=hourly_engagement.values)
plt.title('Hourly Engagement Rate')
plt.xlabel('Hour of the Day')
plt.ylabel('Average Engagement Rate')
plt.xticks(np.arange(0, 24, step=1))
plt.grid(True)
# plt.show()
plt.savefig('Deploy/images/h_of_day.png')
plt.figure(figsize=(10, 6))
sns.barplot(x=daily_engagement.index, y=daily_engagement.values, order=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
plt.title('Daily Engagement Rate')
plt.xlabel('Day of the Week')
plt.ylabel('Average Engagement Rate')
plt.xticks(rotation=45)
plt.savefig('Deploy/images/day_of_week.png')
# plt.show()

top_content_types = data.groupby('content')['engagement_rate'].mean().nlargest(5).index.tolist()
logger.info(f"Top Content Types:\n{',   '.join(top_content_types)}")

best_day = daily_engagement.idxmax()
best_hour = hourly_engagement.idxmax()

logger.info(f"Best Day for Tweeting: {best_day}")
logger.info(f"Best Hour for Tweeting: {best_hour}")

heatmap_data = data.groupby(['hour', 'day_of_week'])['engagement_rate'].mean().unstack()
plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_data, cmap='YlGnBu', annot=True, fmt='.2f', linewidths=.5)
plt.title('Engagement Heatmap by Hour and Day of the Week')
plt.xlabel('Day of the Week')
plt.ylabel('Hour of the Day')
# plt.show()
plt.savefig('Deploy/images/Hour_and_Day_of_the_Week.png')
best_day = daily_engagement.idxmax()
best_hour = hourly_engagement.idxmax()


print(f"Best Day for Tweeting: {best_day}")
print(f"Best Hour for Tweeting: {best_hour}")