from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer
import re


class TextSummary:

    def __init__(self, document):
        self.ps = PorterStemmer()
        self.document = str(document).lower()

    def __word_tokenize(self, text):
        text = re.sub("[^a-z ]", "", text)
        return word_tokenize(text)

    def __sent_tokenize(self, text):
        return sent_tokenize(text)

    def __find_stem(self, text):
        return self.ps.stem(text)

    def __simplify_sentence(self, sent):
        text = list()
        for word in self.__word_tokenize(sent):
            text.append(self.__find_stem(word))
        return text

    def calculate_word_score(self):
        doc = self.document
        stopwords_list = set(stopwords.words('english'))
        word_list = self.__word_tokenize(doc)
        stem_words = [self.__find_stem(word) for word in word_list]
        word_score = dict()
        for word in stem_words:
            if word in stopwords_list:
                continue
            if word not in word_score.keys():
                word_score[word] = 1
            else:
                word_score[word] += 1
        return word_score

    def calculate_sentence_score(self):
        doc = self.document
        word_score = self.calculate_word_score()
        sent_token = self.__sent_tokenize(doc)
        sent_score = dict()
        for sent in sent_token:
            stem_words = (self.__simplify_sentence(sent))
            score = 0
            for word in stem_words:
                if word in word_score.keys():
                    score += (word_score[word])

            if sent not in sent_score.keys():
                sent_score[sent] = score
            else:
                sent_score[sent] += score

        return sent_score

    def summarize(self, threshold=1.0):
        score = self.calculate_sentence_score()

        # print(score.values())
        score_mean = (sum(score.values()) / len(score)) / threshold
        summary = ""
        for sent, score in score.items():
            if score >= score_mean:
                summary += str(sent).capitalize() + " "
        return summary
