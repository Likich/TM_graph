import stop_words
import pymystem3
import pandas as pd
import numpy as np

def preprocess_single_line(line:str, prefix_rm, sw, mstem):
    if prefix_rm is not None:
        if line.startswith(prefix_rm):
            print('removing a line')
            return ''
    # remove numbers and make letters lowercase
    line = ''.join([c for c in line.lower() if c.isalpha() or c.isspace()]) # ''.join([c.lower() for c in line if c.isalpha()])
    # split all whitespace to be only one space (tabs, double space, etc -> single space)
    line = ' '.join(line.split())
    # delete english text
    line = ' '.join([word for word in line.split() if ord(word[0]) > 1039])
    # lemmatize
    line = ' '.join(mstem.lemmatize(line))
    # clean stop words

    line = ' '.join(word for word in line.split() if not word in sw)
    return line

lang_to_interviewer = {
    'ru': 'Интервьюер:',
    'en': 'Interviewer:',
}

def lemmatize_all(text_file, include_interviewer=True, language=''):
    sw = (
        set(stop_words.get_stop_words('russian')).union(
        set(stop_words.get_stop_words('english')).union(
        set(['интервьюер', 'информант', 'инт', 'инф'])))
    )
    mstem = pymystem3.Mystem()

    with open(text_file, 'r') as file:
        raw_text = file.readlines()
    if not include_interviewer:
        prefix_rm = lang_to_interviewer[language]
    else:
        prefix_rm = None
    print('about to work')
    text = [preprocess_single_line(line, prefix_rm=prefix_rm, sw=sw, mstem=mstem) for line in raw_text]
    print('did work')
    print('everything lemmatized')
    print(pd.DataFrame({'paragraphs':text}).head())
    return pd.DataFrame({'paragraphs':text}).to_excel('interview_lemmatized.xlsx')

    # masks = []
    # print('Lemmatizing...')
    # # def getText(tex, include_interviewer):
    # #     with open(tex) as f:
    # #         text = f.readlines()
    # #     if not include_interviewer:
    # #         # Filter out paragraphs that start with "Интервьюер:"
    # #         text = [line for line in text if not line.strip().startswith("Интервьюер:")]
    # #     lines = '\n'.join(text)
    # #     return lines

    # # def getText(tex):
    # #     with open(tex) as f:
    # #         text = f.readlines()
    # #         lines =  '\n'.join(text)
    # #     return lines
    # # text = getText(text_file, include_interviewer)
    # with open(text_file) as f:
    #     text = f.readlines()
    # if not include_interviewer:
    #     masks.append([0 if line.strip().startswith('Интервьюер:') else 1 for line in text])
    #     text = text[masks[-1]]
    #     # text = [line for line in text if not line.strip().startswith("Интервьюер:")]
    # lines = '\n'.join(text)
    # paragraphs = lines.split('\n')
    # df = pd.DataFrame(paragraphs,
    #                 columns = ['paragraphs'],
    #                 index = range(1, len(paragraphs)+1))
    # df['paragraphs'] = df['paragraphs'].str.lower()

    # def delete_punctuation(text):
    #     clear_text = ""
    #     for symbol in text:
    #         if symbol.isalpha():
    #             clear_text += symbol
    #         else:
    #             clear_text += " "
    #     return clear_text
    # def delete_double(text):
    #     while "  " in text:
    #         text = text.replace("  ", " ").strip()
    #     return text
    # def delete_eng(text):
    #     text = text.split()
    #     masks.append([1 if ord(word[0])>1039 else 0 for word in text])
    #     return text[masks[-1]]
    #     # clear_text = []
    #     # for word in text:
    #     #     if ord(word[0]) > 1039:
    #     #         clear_text.append(word)
    #     # return " ".join(clear_text)
    # df['paragraphs'] = df['paragraphs'].apply(delete_punctuation)
    # df['paragraphs'] = df['paragraphs'].apply(delete_double)

    # mstem = pymystem3.Mystem()

    # def lemmatize(text):
    #     return ''.join(mstem.lemmatize(text)).strip()
    # df['paragraphs'] = df['paragraphs'].apply(lemmatize)
    # rus = stop_words.get_stop_words('russian')
    # en = stop_words.get_stop_words('english')
    # all_sw = rus + en
    # len(all_sw)
    # additional = ['интервьюер', 'информант']
    # all_sw += additional
    
    # def delete_stop_words(text):
    #     text = text.split()
    #     clear_text = []
    #     for word in text:
    #         if word not in all_sw:
    #             clear_text.append(word)
    #     return ' '.join(clear_text)
    # df['paragraphs'] = df['paragraphs'].apply(delete_stop_words)
    # df['paragraphs'] = df['paragraphs'].apply(delete_eng)
    # print('Your file is lemmatized. Please find enclosed interview_lemmatized.xlsx')
    # return df.to_excel('interview_lemmatized.xlsx')


def lemmatize_all_eng(text_file, include_interviewer=True):
    from nltk.stem import WordNetLemmatizer
    import nltk
  
    lemmatizer = WordNetLemmatizer()
    import stop_words
    import pandas as pd
    print('Lemmatizing...')

    def getText(tex, include_interviewer):
        with open(tex) as f:
            text = f.readlines()
        if not include_interviewer:
            # Filter out paragraphs that start with "Интервьюер:"
            text = [line for line in text if not line.strip().startswith("Interviewer:")]
        lines = '\n'.join(text)
        return lines
    
    text = getText(text_file, include_interviewer)
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