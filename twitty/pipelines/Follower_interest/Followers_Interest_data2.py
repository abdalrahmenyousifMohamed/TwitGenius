import pandas as pd
import re
import pyLDAvis as vis
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from contextualized_topic_models.models.ctm import CombinedTM
from contextualized_topic_models.utils.data_preparation import TopicModelDataPreparation
from contextualized_topic_models.utils.preprocessing import WhiteSpacePreprocessing
import os
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning, module="pkg_resources")


class TopTopics:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path, encoding='iso-8859-1')
        self.df_gender_filtered = self.preprocess_data()
        self.bow_size = 0
        self.contextual_size = 768
        self.n_components = 50
        self.num_epochs = 20
        self.ctm = None
        self.nltk_download_stopwords()

    def preprocess_data(self):
        self.df_gender_filtered = self.data[['name', 'text', 'description']]
        self.duplicate_count_txt = self.df_gender_filtered['text'].duplicated().sum()
        self.duplicate_count_dis = self.df_gender_filtered['description'].duplicated().sum()
        
        self.df_gender_filtered.drop_duplicates(subset='description', inplace=True)
        self.df_gender_filtered.drop_duplicates(subset='text', inplace=True)
        self.df_gender_filtered = self.df_gender_filtered.dropna().reset_index(drop=True)
        
        self.df_gender_filtered['description'] = self.df_gender_filtered['description'].apply(self.clean_text)
        self.df_gender_filtered['description'] = self.df_gender_filtered['description'].apply(self.remove_urls)
        self.df_gender_filtered['text'] = self.df_gender_filtered['text'].apply(self.clean_text)
        self.df_gender_filtered['text'] = self.df_gender_filtered['text'].apply(self.remove_urls)
        return self.df_gender_filtered

    def remove_urls(self, text):
        cleaned_text = re.sub(r'http[s]?\S+', '', text)
        return re.sub(r'https?://\S+|www\.\S+', '', cleaned_text)

    def clean_text(self, text):
        pattern = r'[^\w\s]'
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        cleaned_text = re.sub(pattern, '', text)
        return cleaned_text

    def nltk_download_stopwords(self):
        nltk.download('stopwords')

    def combine_text_columns(self):
        selected_columns = ['text', 'description']
        self.df_gender_filtered['combined_text'] = self.df_gender_filtered[selected_columns].apply(lambda row: ' '.join(row), axis=1)
        self.df_gender_filtered['combined_text'] = self.df_gender_filtered['combined_text'].apply(self.clean_text)
        self.df_gender_filtered['combined_text'] = self.df_gender_filtered['combined_text'].apply(self.remove_urls)
        self.df_gender_filtered.to_csv('cleaned_data_gender.csv' , index=False)

    def prepare_topic_model_data(self):
        sp = WhiteSpacePreprocessing(self.df_gender_filtered['combined_text'], stopwords_language='english')
        res = sp.preprocess()
        preprocessed_documents, unpreprocessed_corpus, vocab = res[0], res[1], res[2]
        tp = TopicModelDataPreparation("paraphrase-distilroberta-base-v1")
        training_dataset = tp.fit(text_for_contextual=unpreprocessed_corpus, text_for_bow=preprocessed_documents)
        return tp, training_dataset

    def train_topic_model(self, tp, training_dataset):
        os.environ["TOKENIZERS_PARALLELISM"] = "false"
        self.ctm = CombinedTM(bow_size=len(tp.vocab), contextual_size=768, n_components=50, num_epochs=20)
        self.ctm.fit(training_dataset)

    def visualize_topics(self):
        lda_vis_data = self.ctm.get_ldavis_data_format(tp.vocab, training_dataset, n_samples=10)
        ctm_pd = vis.prepare(**lda_vis_data)
        vis.display(ctm_pd)


if __name__ == "__main__":
    data_path = '../data/gender-classifier-DFE-791531.csv'
    analyzer = TopTopics(data_path)
    analyzer.combine_text_columns()
    # tp, training_dataset = analyzer.prepare_topic_model_data()
    # analyzer.train_topic_model(tp, training_dataset)
    # analyzer.visualize_topics()
