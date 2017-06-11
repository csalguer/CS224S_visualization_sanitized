from __future__ import print_function
modulePath = 'cpl_lib/' # change as appropriate
import sys
import os
sys.path.append(modulePath)
# now you're good to import the modules
import dspUtil
import praatTextGrid
import scipy.io.wavfile as wav 
import myWave
import audioop
import numpy as np
import csv


class ProsodicReaper(object):
    """docstring for ProsodicReaper"""
    def __init__(self, filename="sample.wav", fileList=None):
        super(ProsodicReaper, self).__init__()
        self.filename = filename
        self.fileList = fileList
        if self.fileList is None:
            participants = self.filename.split('.')[0].split('-')
            print(participants)
            self.participants = participants
        else:
            print(self.fileList)

    

    #REAPS THE TWO FEATURE VECTORS PRESENT FROM A SINGLE SPEED DATING FILE
    def reapFeatures(self):
        tg_pathname = self.getFilepathForTG()
        wav_pathname = self.getFilepathForWAV()
        timingsForDate = self.getIntervalsFromTG(tg_pathname)
        male_timings = timingsForDate["MALE"]
        female_timings = timingsForDate["FEMALE"]
        numChannels, numFrames, fs, sig = myWave.readWaveFile(wav_pathname)
        
        assert numChannels is not 0
        print(numChannels, numFrames, fs)
        print("\tFrame Sample Rate: ",fs)
        print("\tData Array Shape: ", sig[0].shape)
        male_vec = self.calculateFeatures(male_timings, fs, sig[0])
        female_vec = self.calculateFeatures(female_timings, fs, sig[0])
        male_vec.insert(0, self.participants[0])
        female_vec.insert(0, self.participants[1])
        return {"MALE":male_vec, "FEMALE":female_vec}


    #INITIAL WAY OF PROCESSING BATCHES, USED IN OTHER REAPER CODE BUT NOT FOR FINAL USE
    #TO BE DEPRECATED WITH BATCH_PROCESS.PY TO ALLOW FOR EASY RESUMING OF PROCESSING 
    #UPON INTERRUPT DUE TO MEMORY LEAK IN DSPUTILS LIBRARY USED FOR THE F0 CALCULATION
    #WHICH USES A DEEPCOPY FOR OPERATIONS: 
    #               NOTE: WE DID NOT TOUCH ANY BROKEN CODE IN THE LIBRARY, INCLUDING THIS MEMORY LEAK
    def reapFeaturesList(self):
        assert self.fileList is not None
        with open(self.fileList) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        f = open("features4.csv", 'wt')
        try:
            writer = csv.writer(f)
            for file in content:
                self.setParticipants(file)
                feat = self.reapFeatures()
                writer.writerow(feat["MALE"])
                writer.writerow(feat["FEMALE"])
        finally:
            f.close()


    def setParticipants(self, filename):
        self.filename = filename
        participants = filename.split('.')[0].split('-')
        print(participants)
        self.participants = participants


    #MAIN METHOD USED TO PERFORM THE F0 AND RMS CALCULATIONS
    def calculateFeatures(self, timings, fs_rate, signal_data):
        F0_arr = []
        RMS_arr = []
        for (start_t, end_t) in timings:
            # print("\t(s,e) = ", "(", start_t, ", ", end_t, ")")
            start_index = dspUtil.getFrameIndex(start_t, fs_rate)
            end_index = dspUtil.getFrameIndex(end_t, fs_rate)
            # print("\t\tConverted(s,e) = ", "(", start_index, ", ", end_index, ")")
            assert start_t is not end_t
            utterance = signal_data[start_index:end_index]
            # result =  dspUtil.calculateF0OfSignal(signal_data, fs_rate, tmpDataPath='temp/', \
            #     tStart=start_t, tEnd=end_t)
            F0_result = dspUtil.calculateF0once(utterance, fs_rate)
            #RMS_result = dspUtil.calculateRMSOnce(utterance)
            RMS_result = audioop.rms(utterance, 2)
            F0_arr.append(F0_result)
            RMS_arr.append(RMS_result)
            # print("F0: ", F0_result)
            # print("RMS: ", RMS_result)
        vec = self.packageFeatures(F0_arr, RMS_arr)
        print(vec)
        return vec


    #REWRITTEN METHOD FOR CALCULATING RMS: NATIVE PYTHON IMPLEMENTATION, NOT THROUGH PRAAT
    def np_audioop_rms(self, data):
        """audioop.rms() using numpy; avoids another dependency for app"""
        # _checkParameters(data, width)
        fromType = (np.int8, np.int16, np.int32)[width // 2]
        return np.power(np.frombuffer(data, dtype=fromType), 2.0).mean() ** .5

    #HELPER METHOD TO RETURN A FULLY PACKAGED FEATURE VECTOR CONTAINING ALL THE STATISTICS GIVEN TWO LISTS
    #CONTAINING THE VALUE DISTRIBUTIONS FOR F0 AND RMS
    def packageFeatures(self, F0, RMS):
        F0_min = min(F0)
        F0_max = max(F0)
        FSum = sum(F0)
        F0_mean = FSum/len(F0)
        F0_std = np.std(F0)
        F0_range = F0_max - F0_min


        RMS_min = min(RMS)
        RMS_max = max(RMS)
        RSum = sum(RMS)
        RMS_mean = RSum/len(RMS)
        RMS_std = np.std(RMS)
        RMS_range = RMS_max - RMS_min
        return [F0_min, F0_max, F0_mean, F0_std, F0_range, RMS_min, RMS_max, RMS_mean, RMS_std, RMS_range]



    #METHOD TO RETRIEVE ALL UTTERANCE TIMINGS AS DEFINED IN THE TEXTGRID
    def getIntervalsFromTG(self, filepath):
        textGrid = praatTextGrid.PraatTextGrid(0, 0)
        # arrTiers is an array of objects (either PraatIntervalTier or PraatPointTier)
        arrTiers = textGrid.readFromFile(filepath)
        # print(arrTiers)
        speakers = {}
        for tier in arrTiers:
            sexOfSpeaker = tier.getName()
            # print(sexOfSpeaker)
            # print(tier.getName())
            # print(tier.getType())
            intervals = []
            for i in range(tier.getSize()):
                value = tier.get(i)
                start, end, txt = value
                # print("\t", start, end, txt)
                if txt == "":
                    intervals.append((start, end))
            assert len(intervals) is not 0
            speakers[sexOfSpeaker] = intervals
        assert len(speakers) is not 0
        return speakers
                


    #HELPER METHOD TO GET FILENAME FOR THE TEXTGRID FOR THE FILENAME GIVEN UPON INIT. ASSUMES THE FILE HAS A
    #STRUCTURE TO THAT OF THE SPEEDDATING CORPUS WITH THE FORM "(PARTICIPANT_ONE)-(PARTICIPANT_TWO).*"
    def getFilepathForTG(self, rev=False):
        assert self.participants is not None
        filepath = 'speeddating_corpus/textgrids/' + "-".join(self.participants) + ".TextGrid"
        rev_filepath = 'speeddating_corpus/textgrids/' + "-".join(reversed(self.participants)) + ".TextGrid"
        if rev:
            return rev_filepath
        return filepath
    #HELPER METHOD TO GET FILENAME FOR THE AUDIO FOR THE FILENAME GIVEN UPON INIT. ASSUMES THE FILE HAS A
    #STRUCTURE TO THAT OF THE SPEEDDATING CORPUS WITH THE FORM "(PARTICIPANT_ONE)-(PARTICIPANT_TWO).*""
    def getFilepathForWAV(self, rev=False):
        assert self.participants is not None
        filepath = 'speeddating_corpus/wavefiles/' + "_".join(self.participants) + ".wav"
        rev_filepath = 'speeddating_corpus/wavefiles/' + "_".join(reversed(self.participants)) + ".wav"
        if rev:
            return rev_filepath
        return filepath

# class F0Features:
#     def __init__(self, F0_min, F0_max, F0_mean, F0_std, F0_range):
#     self.F0_min = F0_min
#     self.F0_max = F0_max
#     self.F0_mean = F0_mean
#     self.F0_std = F0_std
#     self.F0_range = F0_range


if __name__ == '__main__':
    #prosody = ProsodicReaper(fileList="test_batch4.txt")
    #prosody.reapFeaturesList()
    p = ProsodicReaper('102-122.txt')
    print(p.reapFeatures())