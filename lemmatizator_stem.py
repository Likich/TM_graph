
def lemmatize_all(text_file):
    import stop_words
    import pymystem3
    import pandas as pd
    print('Lemmatizing...')

    def getText(tex):
        with open(tex) as f:
            text = f.readlines()
            lines =  '\n'.join(text)
        return lines
    text = getText(text_file)
    paragraphs = text.split('\n')
    df = pd.DataFrame(paragraphs,
                    columns = ['paragraphs'],
                    index = range(1, len(paragraphs)+1))
    df['paragraphs'] = df['paragraphs'].str.lower()

    def delete_punctuation(text):
        clear_text = ""
        for symbol in text:
            if symbol.isalpha():
                clear_text += symbol
            else:
                clear_text += " "
        return clear_text
    def delete_double(text):
        while "  " in text:
            text = text.replace("  ", " ").strip()
        return text
    def delete_eng(text):
        text = text.split()
        clear_text = []
        for word in text:
            if ord(word[0]) > 1039:
                clear_text.append(word)
        return " ".join(clear_text)
    df['paragraphs'] = df['paragraphs'].apply(delete_punctuation)
    df['paragraphs'] = df['paragraphs'].apply(delete_double)

    mstem = pymystem3.Mystem()

    def lemmatize(text):
        return ''.join(mstem.lemmatize(text)).strip()
    df['paragraphs'] = df['paragraphs'].apply(lemmatize)
    rus = stop_words.get_stop_words('russian')
    en = stop_words.get_stop_words('english')
    all_sw = rus + en
    len(all_sw)
    additional = ['интервьюер', 'информант']
    all_sw += additional
    
    def delete_stop_words(text):
        text = text.split()
        clear_text = []
        for word in text:
            if word not in all_sw:
                clear_text.append(word)
        return ' '.join(clear_text)
    df['paragraphs'] = df['paragraphs'].apply(delete_stop_words)
    df['paragraphs'] = df['paragraphs'].apply(delete_eng)
    print('Your file is lemmatized. Please find enclosed interview_lemmatized.xlsx')
    return df.to_excel('interview_lemmatized.xlsx')


def lemmatize_all_eng(text_file):
    from nltk.stem import WordNetLemmatizer
    import nltk
  
    lemmatizer = WordNetLemmatizer()
    import stop_words
    import pymystem3
    import pandas as pd
    print('Lemmatizing...')
    def getText(tex):
        with open(tex) as f:
            text = f.readlines()
            lines =  '\n'.join(text)
        return lines
    text = getText(text_file)
    paragraphs = text.split('\n')
    df = pd.DataFrame(paragraphs,
                    columns = ['paragraphs'],
                    index = range(1, len(paragraphs)+1))
    df['paragraphs'] = df['paragraphs'].str.lower()
    def delete_punctuation(text):
        clear_text = ""
        for symbol in text:
            if symbol.isalpha():
                clear_text += symbol
            else:
                clear_text += " "
        return clear_text
    def delete_double(text):
        while "  " in text:
            text = text.replace("  ", " ").strip()
        return text

    df['paragraphs'] = df['paragraphs'].apply(delete_punctuation)
    df['paragraphs'] = df['paragraphs'].apply(delete_double)

    def lemmatize(text):
        word_list = nltk.word_tokenize(text)
        print(word_list)
        return ' '.join([lemmatizer.lemmatize(w) for w in word_list])
    df['paragraphs'] = df['paragraphs'].apply(lemmatize)
    en = stop_words.get_stop_words('english')
    all_sw = en
    len(all_sw)
    def delete_stop_words(text):
        text = text.split()
        clear_text = []
        for word in text:
            if word not in all_sw:
                clear_text.append(word)
        return ' '.join(clear_text)
    df['paragraphs'] = df['paragraphs'].apply(delete_stop_words)
    print('Your file is lemmatized. Please find enclosed interview_lemmatized.xlsx')
    return df.to_excel('interview_lemmatized.xlsx')