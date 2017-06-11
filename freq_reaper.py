import numpy as np

class FreqReaper(object):
    """docstring for ProsodicReaper"""
    def __init__(self, fileList=None):
        super(FreqReaper, self).__init__()
        self.unigram_set = set([])
        self.bigram_set = set([])

    # open the transcript for this speeddate (checking to see if it's saved with the participants in the reverse
    # order), process each line of the file, and add all unigrams and bigrams to the sets of unigrams and bigrams
    def extractOneUnigramBigram(self, file):
        try:
            with open('speeddating_corpus/transcripts/' + file) as f:
                lines = f.readlines()
        except:
            partial_reversal = file.split("-")
            reversed = partial_reversal[1].split(".")[0] + "-" + partial_reversal[0] + ".txt"
            try:
                with open('speeddating_corpus/transcripts/' + reversed) as f:
                    lines = f.readlines()
            except:
                return
        for line in lines:
            split_line = line.split(":")
            if split_line[0] != 'FILE NAME' and split_line[0] != 'AUDIO SOURCE' and split_line[0].strip() != '' and len(split_line) == 4:
                spoken_line = split_line[3]
                tokenized_line = spoken_line.strip().split()
                for token in tokenized_line:
                    self.unigram_set.add(token)
                for i in range(0, len(tokenized_line) - 1):
                    self.bigram_set.add(tokenized_line[i] + " " + tokenized_line[i + 1])

    # from a file that lists the transcripts, open the file, extract the list of transcripts,
    # and pass each transcript file to extractOneUnigramBigram for processing
    def makeAllUnigramBigramSet(self, filename):
        with open(filename) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        for file in content:
            self.extractOneUnigramBigram(file)

    # now that we've put all the unigrams and bigrams into sets (to preserve uniqueness), convert the sets
    # into a list so that we can use the indices
    def makeUnigramBigramList(self):
        self.unigrams = list(self.unigram_set)
        self.bigrams = list(self.bigram_set)

    # for a single line, extract all the bigrams from the line
    def getBigram(self, tokenized_line, bigram_results):
        for i in range(0, len(tokenized_line) - 1):
            bigram = tokenized_line[i] + " " + tokenized_line[i + 1]
            index = self.bigrams.index(bigram)
            if index in bigram_results:
                bigram_results[index] += 1
            else:
                bigram_results[index] = 1
        return bigram_results

    # for a single line, extract all the unigrams from the line
    def getUnigram(self, tokenized_line, unigram_results):
        for token in tokenized_line:
            index = self.unigrams.index(token)
            if index in unigram_results:
                unigram_results[index] += 1
            else:
                unigram_results[index] = 1
        return unigram_results

    # open file, process lines separately based on the gender of the speaker, and collect lists of unigrams and bigrams
    # for both the male and female speakers
    def getUnigramBigram(self, file):
        try:
            with open('speeddating_corpus/transcripts/' + file) as f:
                lines = f.readlines()
        except:
            return None

        male_unigram_results = dict()
        female_unigram_results = dict()
        male_bigram_results = dict()
        female_bigram_results = dict()
        for line in lines:
            split_line = line.split(":")
            if split_line[0] != 'FILE NAME' and split_line[0] != 'AUDIO SOURCE' and split_line[0].strip() != '' and len(split_line) == 4:
                gender = split_line[2].split()[1]
                spoken_line = split_line[3]
                tokenized_line = spoken_line.strip().split()
                if gender == "MALE":
                    male_unigram_results = self.getUnigram(tokenized_line, male_unigram_results)
                    male_bigram_results = self.getBigram(tokenized_line, male_bigram_results)
                else:
                    female_unigram_results = self.getUnigram(tokenized_line, female_unigram_results)
                    female_bigram_results = self.getBigram(tokenized_line, female_bigram_results)
        return {"MALE_UNIGRAM_RESULTS": male_unigram_results, "FEMALE_UNIGRAM_RESULTS": female_unigram_results,
                "MALE_BIGRAM_RESULTS": male_bigram_results, "FEMALE_BIGRAM_RESULTS": female_bigram_results}

    # check to see whether the file is saved with the participants in the reverse order and pass off file to
    # getUnigramBigram
    def writeUnigramBigramToFile(self, f, file):
        results = self.getUnigramBigram(file)
        if results == None:
            partial_reversal = file.split("-")
            reversed = partial_reversal[1].split(".")[0] + "-" + partial_reversal[0] + ".txt"
            results = self.getUnigramBigram(reversed)
            if results == None:
                return None
        return results

    # iterate through the list of all the files, hand the file off to writeUnigramBigramToFile, and add the results
    # to self.unprocessed_results for later processing
    def calculateUnigramBigrams(self):
        with open("consolidated_batch.txt") as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        self.unprocessed_results = list()
        for file in content:
            self.unprocessed_results.append(self.writeUnigramBigramToFile(f, file))
        self.total_lines = len(content) * 2

    # process the features, writing them out as feature vectors with 0s filling in all unigrams and bigrams that were
    # not observed in the conversation
    def processFreqFeatures(self):
        processed_results = np.zeros([self.total_lines, len(self.unigrams) + len(self.bigrams)])
        for i in range(0, len(self.unprocessed_results)):
            for key in self.unprocessed_results[i]["MALE_UNIGRAM_RESULTS"].keys():
                processed_results[i * 2][key] = self.unprocessed_results[i]["MALE_UNIGRAM_RESULTS"][key]
            for key in self.unprocessed_results[i]["MALE_BIGRAM_RESULTS"].keys():
                processed_results[i * 2][key + len(self.unigrams)] = self.unprocessed_results[i]["MALE_BIGRAM_RESULTS"][key]
            for key in self.unprocessed_results[i]["FEMALE_UNIGRAM_RESULTS"].keys():
                processed_results[i * 2 + 1][key] = self.unprocessed_results[i]["FEMALE_UNIGRAM_RESULTS"][key]
            for key in self.unprocessed_results[i]["FEMALE_BIGRAM_RESULTS"].keys():
                processed_results[i * 2 + 1][key + len(self.unigrams)] = self.unprocessed_results[i]["FEMALE_BIGRAM_RESULTS"][key]
        return processed_results


    def runAll(self):
        self.makeAllUnigramBigramSet("consolidated_batch.txt")
        self.makeUnigramBigramList()
        self.calculateUnigramBigrams()
        return self.processFreqFeatures()


if __name__ == '__main__':
    freq_reaper = FreqReaper()
    freq_reaper.makeAllUnigramBigramSet("consolidated_batch.txt")
    freq_reaper.makeUnigramBigramList()
    freq_reaper.calculateUnigramBigrams()
