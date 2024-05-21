import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
def generate_wordcloud(df_column):
    comment_text = ' '.join(df_column)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(comment_text)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)