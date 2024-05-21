import streamlit as st
import pandas as pd
import plotly.express as px
from fetch import fetch_comments
from trans import translate_comments
from vader import analyze_sentiment
from wordcld import generate_wordcloud

def input_page():
    st.title("ECHO INSIGHTS")

    # Get YouTube video link from user
    youtube_link = st.text_input("Enter YouTube video link:")
    if st.button("Analyze") and youtube_link:
        # Extract video ID from the link
        video_id = youtube_link.split("=")[-1]
        # Set query parameters to navigate to the next page
        st.session_state["query_params"] = {"youtube_link": youtube_link, "video_id": video_id}



def result_page():
    st.title("ECHO INSIGHTS !!")

    if st.button("Home"):
        # Clear session state
        st.session_state.clear()
        # Redirect to input page
        input_page()

    # Get video ID from query parameters
    query_params = st.session_state.get("query_params", {})
    youtube_link = query_params.get("youtube_link", "")
    video_id = query_params.get("video_id", "")

    

    # Fetch comments
    df = fetch_comments(video_id)
    st.subheader("Fetched Comments")
    # Display selected columns' heads in Streamlit
    st.write(df.head(15))

    # Translate comments
    translated_comments = translate_comments(df)
    selected_columns = ['text', 'translated_text']
    selected_df = df[selected_columns]
    st.subheader("Translated Comments")
    st.write(selected_df.head(15))

    # Perform sentiment analysis
    sentiment_analysis = analyze_sentiment(translated_comments)
    selected_columns = ['author','text', 'translated_text','vader_sentiment']
    selected_df = df[selected_columns]
    
    
    # Combine sentiment analysis with original data
    df['vader_sentiment'] = sentiment_analysis['vader_sentiment']

    # Sort comments based on sentiment score
    top_comments = df.sort_values(by='vader_sentiment', ascending=False).head(10)

    # Display top 10 comments with sentiments
    st.subheader("Top 10 Comments based on Sentiment")
    st.write(top_comments[['author', 'text', 'vader_sentiment']])

    worst_comments = df.sort_values(by='vader_sentiment', ascending=True).head(10)

    # Display worst 10 comments with sentiments
    st.subheader("Worst 10 Comments based on Sentiment")
    st.write(worst_comments[['author', 'text', 'vader_sentiment']])

    # Display sentiment distribution plot
    st.subheader("Sentiment Distribution")
    fig = px.histogram(df, x='vader_sentiment', nbins=30, title="Sentiment Distribution")
    st.plotly_chart(fig)

    # Display overall sentiment
    overall_sentiment = sentiment_analysis['vader_sentiment'].mean()
    st.subheader("Overall Sentiment")
    st.write(f"Overall sentiment: {overall_sentiment}")

    st.subheader("Word Cloud")
    generate_wordcloud(translated_comments['text'])

    # st.subheader("Pandas Profiling Report")
    # profiling_report = generate_profiling_report(df)
    # st.write(profiling_report)

    # Comments over time
    df['comment_published'] = pd.to_datetime(df['published_at'])
    df['comment_date'] = df['comment_published'].dt.date
    comments_over_time = df.groupby('comment_date').size().reset_index(name='comment_count')
    st.subheader("Comments Over Time")
    fig_comments_over_time = px.line(comments_over_time, x='comment_date', y='comment_count', title='Comments Over Time')
    st.plotly_chart(fig_comments_over_time)
    


def main():

    if st.session_state.get("query_params"):
        result_page()
    else:
        input_page()


if __name__ == "__main__":
    main()