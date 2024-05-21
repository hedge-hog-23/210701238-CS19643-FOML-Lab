def translate_comments(df):
    # Your code to translate comments here
    from googletrans import Translator
    def translate_text(text, src='auto', dest='en'):
      translator = Translator()
      translated_text = translator.translate(text, src=src, dest=dest)
      return translated_text.text
    # Apply translation to the 'text' column
    df['translated_text'] = df['text'].apply(lambda x: translate_text(x))
    return df