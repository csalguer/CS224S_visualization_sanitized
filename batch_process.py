
from __future__ import print_function
from __future__ import with_statement
from collections import deque
import sys
import os
import csv
from prosody_reaper import ProsodicReaper
from multiprocessing import Process,Queue

class BatchProcess(object):
    """docstring for BatchProcess"""
    def __init__(self, batchFilename, featdumpFilename, debug=True):
        self.batchFilename = batchFilename
        self.featdumpFilename = featdumpFilename
        self.reaper = ProsodicReaper(batchFilename)
        self.debug = debug
        super(BatchProcess, self).__init__()


    #HELPER METHOD TO GET THE LAST ROW OF THE CSV DUMP FILE WHERE ALL THE FEATURES
    #ARE BEING PLACED. USED TO HELP RESTART OF PROCESSING FOR INTERRUPS
    def get_last_row(self):
        try:
            with open(self.featdumpFilename, 'r') as f:
                q = deque(csv.reader(f), 1)
                lastrow = q[0]
                participants = lastrow[0]
                if self.debug:
                    # print("Participants: ", participants)
                    print("Last Row: ", lastrow)
                return lastrow
        except IOError:
            print("No Known file named: {}".format(self.featdumpFilename))
            return None

    #HELPER METHOD TO GET THE PARTICIPANTS ASSUMING THE FILENAME FOLLOWS THE SPEEDDATING CORPUS
    #CONVENTIONS FOR NAMING, THAT IS: "(PARTICIPANT_ONE)-(PARTICIPANT_TWO).*"
    #ONLY TO BE USED WHEN THE LAST TWO ROWS ARE GUARANTEED TO BE PARTICIPANT PAIRS
    def get_last_participants(self):
        try:
            with open(self.featdumpFilename, 'r') as f:
                q = deque(csv.reader(f), 2)
                print(q)
                lastrow = q[0]
                penultimate = q[1]
                if "EOF" in lastrow:
                    print("FOUND EOF")
                    participants = lastrow.split('|')[1]
                else:
                    participants = "{}-{}".format(lastrow[0], penultimate[0])
                if self.debug:
                    print("Participants: ", participants)
                    # print("Last Row: ", lastrow)
                return participants
        except IOError:
            print("No Known file named: {}".format(self.featdumpFilename))
            return None



    #PROVIDES THE RESTART FRAMEWORK THAT CHECKS THE FINAL ROW TO ALLOW RESUMING OF 
    #PROCESSING IN CASE OF AN INTERRUPTION OR A RESTART. 
    def process(self):
        lastrow = self.get_last_row()
        with open(self.batchFilename) as f:
            batch = f.readlines()
        batch = [x.strip() for x in batch]
        if lastrow is None:
            print("FIRST LAUNCH: COLD START")
            print("CREATING FILE")
            filesRemaining = batch
            indexStopped = len(batch) - 1
        else:
            participants = self.get_last_participants()
            print("PREVIOUS RUNNING DETECTED")
            print("LEFT OFF ON PARTICIPANTS: [{}]".format(participants))
            indexStopped = batch.index(participants+".txt")
            filesRemaining = batch[indexStopped+1:]
        f = open(self.featdumpFilename, 'a')
        try:
            writer = csv.writer(f)
            for filename in filesRemaining:
                self.reaper.setParticipants(filename)
                feat = self.reaper.reapFeatures()
                writer.writerow(feat["MALE"])
                writer.writerow(feat["FEMALE"])
        finally:
            f.close()

    def test(self):
        lastRow = self.get_last_row(self.featdumpFilename)
        participants = self.get_last_participants(self.featdumpFilename)


    #HELPER METHOD TO STRIP THE PARTICIPANT NAMES FROM THE FEATURES FILE TO AVOID DIMENSION ERRORS IN REAPER CODE
    #THAT DUMPS MODELS
    def getOutputWithoutParticipants(self):
        with open(self.featdumpFilename,"rb") as source:
            rdr= csv.reader( source )
            with open("prosody_features_np.csv","wb") as result:
                wtr= csv.writer( result )
                for r in rdr:
                    if len(r) > 0:
                        print(r)
                        wtr.writerow( (r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10]) )


#DEFAULT USAGE: PROCESSES A FILE NAMED CONSOLIDATED_BATCH.PY AND OUTPUTS TO PROSODY FEATURES CSV
def main():
    try:
        bp = BatchProcess('consolidated_batch.txt', "prosody_features.csv")
        # queue = Queue()
        # p = Process(target=bp.process)
        # p.start()
        bp.getOutputWithoutParticipants()
    except MemoryError:
        print("RECOVERING FROM MEMORY ERROR:")
        print("ATTEMPTING RESTART")




if __name__ == '__main__':
    main()