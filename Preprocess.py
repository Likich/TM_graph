def getText(text_file):
  with open(text_file) as f:
      text = f.readlines()
      lines =  '\n'.join(text)
  return lines

def read_additional_stopwords(file_path):
    with open(file_path, "r") as file:
        # Splitting by comma since your stopwords are comma-separated
        additional_stopwords = file.read().split(',')
    return additional_stopwords
additional_stopwords = read_additional_stopwords('additional_stopwords.txt')



def preprocess_all(text_files, add_stop_words):
  import nltk
  import gensim
  import stop_words
  import pandas as pd
  import nltk.data
  from gensim import corpora
  import stop_words
  import pickle
  nltk.download('stopwords')
  nltk.download('wordnet')
  nltk.download('punkt')
  rus = stop_words.get_stop_words('russian')
  en = stop_words.get_stop_words('english')
  all_sw = rus + en
  additional = ['инт', 'инф']
  additional_stopwords = read_additional_stopwords('additional_stopwords.txt')
  all_sw += additional
  all_sw += additional_stopwords


  def preprocess(text_file, lemmatized_excel_file, length_restrict, bigram_mincount, additional_stopwords):
    ''' length_restrict - the minimum length of the word to leave in the text
        bigram_mincount – Ignore all words and bigrams with total collected count lower than this value.'''
    print('Reading your transcripts...')

    def dataset_raw(text_file):
      text = getText(text_file)
      paragraphs = text.split('\n')
      df = pd.DataFrame(paragraphs,
                      columns = ['paragraphs'],
                      index = range(1, len(paragraphs)+1))
      return df
    
    df_raw = dataset_raw(text_files)
    print('Raw dataset ready')
    print('Processing your lemmatized dataset...')
    df = pd.read_excel(lemmatized_excel_file, engine="openpyxl", index_col = 0)
    
    def text_to_array(length_restrict, lemmatized_df):
      ''' length_restrict - the minimum length of the word to leave in the text'''
      x_rus = []
      print(len(lemmatized_df))
      for i in range(len(lemmatized_df)):  
        string_spl = str(lemmatized_df['paragraphs'].iloc[i]).split()
        for i in string_spl:
          if i == 'nan':
            string_spl.remove(i)
        # if len(string_spl) > length_restrict:
        x_rus.append(string_spl)
      united =  []
      for i in x_rus:
        for j in i:
          united.append(j)
      df_counts = pd.DataFrame({'text':united})
      df_counts = (df_counts['text'].str.split(expand=True)
                    .stack()
                    .value_counts()
                    .rename_axis('vals')
                    .reset_index(name='count'))
      
      return x_rus, df_counts
    x_rus, df_counts = text_to_array(length_restrict, df)
  
    
    def purification(array_to_clear):
        stop_words_set = set(all_sw)
        x_rus_c = []

        for document in array_to_clear:
            # Keep words that are NOT in the stop words set
            cleared_document = [word for word in document if word not in stop_words_set]
            x_rus_c.append(cleared_document)

        return x_rus_c
    
    def make_corpus(clear_text_set, bigram_mincount):
      '''bigram_mincount – Ignore all words and bigrams with total collected count lower than this value.'''
      bigram = gensim.models.Phrases(clear_text_set, min_count=bigram_mincount, threshold=40)
      clear_text_set = [bigram[line] for line in clear_text_set]
      x_train_rus = [' '.join(i) for i in clear_text_set]
      dictionary = corpora.Dictionary(clear_text_set)
      corpus = [dictionary.doc2bow(text) for text in clear_text_set]
      return x_train_rus, dictionary, corpus
    print('Purifying the dataset with additional stop words...')
    x_rus_c = purification(x_rus)
    print('Constructing the corpus...')
    x_train_rus, dictionary, corpus = make_corpus(x_rus_c, bigram_mincount)
    united =  []
    for i in x_rus:
      for j in i:
        united.append(j)
    df_counts_new = pd.DataFrame({'text':united})
    df_counts_new = (df_counts_new['text'].str.split(expand=True)
                    .stack()
                    .value_counts()
                    .rename_axis('vals')
                    .reset_index(name='count'))
    
    return df_raw, df_counts, df_counts_new, x_train_rus, x_rus, dictionary, corpus
  

  df_raw, df_counts, df_counts_new, x_train_rus_alligned, x_rus_alligned, dictionary, corpus = preprocess(text_files, 'interview_lemmatized.xlsx', 2, 3, all_sw)
  print('Here is your words frequencies. Please check what words you want to add to stop list and add them to additional stopwords list.')
  print(len(x_train_rus_alligned))
  # print(df_counts_new.head(20))




  def preprocess_original(text_file, lemmatized_excel_file, length_restrict, bigram_mincount, additional_stopwords):
      ''' length_restrict - the minimum length of the word to leave in the text
          bigram_mincount – Ignore all words and bigrams with total collected count lower than this value.'''
      print('Reading your transcripts...')
      nltk.download('stopwords')
      nltk.download('wordnet')
      nltk.download('punkt')
      rus = stop_words.get_stop_words('russian')
      en = stop_words.get_stop_words('english')
      all_sw = rus + en
      additional = ['инт', 'инф']
      additional_stopwords = read_additional_stopwords('additional_stopwords.txt')
      all_sw += additional
      all_sw += additional_stopwords
      print(all_sw)

      def getText(text_file):
        with open(text_file) as f:
            text = f.readlines()
            lines =  '\n'.join(text)
        return lines
      
      def dataset_raw(text_file):
        text = getText(text_file)
        paragraphs = text.split('\n')
        df = pd.DataFrame(paragraphs,
                        columns = ['paragraphs'],
                        index = range(1, len(paragraphs)+1))
        return df
      

      df_raw = dataset_raw(text_files)
      print('Raw dataset ready')
      print('Processing your lemmatized dataset...')
      df = pd.read_excel(lemmatized_excel_file, engine="openpyxl", index_col = 0)
      
      def text_to_array(length_restrict, lemmatized_df):
        ''' length_restrict - the minimum length of the word to leave in the text'''
        x_rus = []
        for i in range(len(lemmatized_df)):  
          string_spl = str(lemmatized_df['paragraphs'].iloc[i]).split()
          for i in string_spl:
            if i == 'nan' or len(i) < length_restrict+1:
              string_spl.remove(i)
          if len(string_spl) > length_restrict:
            x_rus.append(string_spl)
        united =  []
        for i in x_rus:
          for j in i:
            united.append(j)
        df_counts = pd.DataFrame({'text':united})
        df_counts = (df_counts['text'].str.split(expand=True)
                      .stack()
                      .value_counts()
                      .rename_axis('vals')
                      .reset_index(name='count'))
        
        return x_rus, df_counts
      x_rus, df_counts = text_to_array(length_restrict, df)


      # def purification(array_to_clear):
      #   x_rus_c = []
      #   for i in array_to_clear:
      #     for j in i:
      #       if j in all_sw:
      #         i.remove(j)
      #   for i in array_to_clear:
      #     x_rus_c.append(list(set(i)))
      #   return x_rus_c
      def purification(array_to_clear):
          stop_words_set = set(all_sw)
          x_rus_c = []

          for document in array_to_clear:
              # Keep words that are NOT in the stop words set
              cleared_document = [word for word in document if word not in stop_words_set]
              x_rus_c.append(cleared_document)

          return x_rus_c
    

      
      def make_corpus(clear_text_set, bigram_mincount):
        '''bigram_mincount – Ignore all words and bigrams with total collected count lower than this value.'''
        bigram = gensim.models.Phrases(clear_text_set, min_count=bigram_mincount, threshold=40)
        clear_text_set = [bigram[line] for line in clear_text_set]
        x_train_rus = [' '.join(i) for i in clear_text_set]
        dictionary = corpora.Dictionary(clear_text_set)
        corpus = [dictionary.doc2bow(text) for text in clear_text_set]
        return x_train_rus, dictionary, corpus
      print('Purifying the dataset with additional stop words...')
      x_rus_c = purification(x_rus)
      print(x_rus_c)
      print('Constructing the corpus...')
      x_train_rus, dictionary, corpus = make_corpus(x_rus_c, bigram_mincount)
      united =  []
      for i in x_rus_c:
        for j in i:
          united.append(j)
      df_counts_new = pd.DataFrame({'text':united})
      df_counts_new = (df_counts_new['text'].str.split(expand=True)
                      .stack()
                      .value_counts()
                      .rename_axis('vals')
                      .reset_index(name='count'))
      
      return df_raw, df_counts, df_counts_new, x_train_rus, x_rus, dictionary, corpus

  df_raw, df_counts, df_counts_new, x_train_rus, x_rus, dictionary, corpus = preprocess_original(text_files, 'interview_lemmatized.xlsx', 2, 3, all_sw)
  dictionary.save('dictionary')
  # df_raw.to_csv('df_raw.csv')

  corpora.MmCorpus.serialize('corpus',corpus)
  with open("x_train_rus", "wb") as fp:   #Pickling
      pickle.dump(x_train_rus, fp)
  with open("x_train_rus_alligned", "wb") as fp:   #Pickling
      pickle.dump(x_train_rus_alligned, fp)
  with open("x_rus", "wb") as fp:   #Pickling
      pickle.dump(x_rus, fp)
  with open("all_sw", "wb") as fp:   #Pickling
      pickle.dump(all_sw, fp)


  return df_counts_new[0:30]