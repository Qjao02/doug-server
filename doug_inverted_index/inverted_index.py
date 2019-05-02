import sys
import pickle
import unidecode

class Index:
    """ Inverted index datastructure """

    def __init__(self, tokenizer, stopwords=None):
        """
        tokenizer   -- NLTK compatible tokenizer function
        stemmer     -- NLTK compatible stemmer
        stopwords   -- list of ignored words
        """
        self.tokenizer = tokenizer
        self.index = defaultdict(list)
        self.documents = {}
        self.__unique_id = 0

        if not stopwords:
            self.stopwords = set()
        else:
            self.stopwords = set(stopwords)

    def lookup(self, word):
        """
        Lookup a word in the index
        """
        word = word.lower()
        word = unidecode.unidecode(word)
        try:
            urls = [self.documents.get(id, None) for id in self.index.get(word)]
        except:
            urls = []
        return urls

    def add(self, document, document_url):
        """
        Add a document string to the index
        """
        for token in [t.lower() for t in nltk.word_tokenize(document)]:
            if token in self.stopwords:
                continue

            if self.__unique_id not in self.index[token]:
                self.index[token].append(self.__unique_id)

        self.documents[self.__unique_id] = document_url
        self.__unique_id += 1

class InvertedIndex():
    @staticmethod
    def getIndex():
        file = open('inverted_index', 'rb')
        obj = pickle.load(file)
        return obj

if __name__ == "__main__":
    urls = []
    args = sys.argv[1:]

    obj = InvertedIndex.getIndex()

    for param in args:
        urls.append(obj.lookup(param))

    if urls:
        urls = list(set(urls[0]).intersection(*urls))
        urls.sort(reverse= True)
        print({"urls" : urls}, end="")