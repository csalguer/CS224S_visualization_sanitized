

class LabelPackager(object):
	"""docstring for LabelPackager"""
	def __init__(self, filename):
		super(LabelPackager, self).__init__()
		self.filename = filename


	#Function to open file, read CSV into list of lists [[..],[..],[..]]
	#Returns list of lists of size(elems_in_batch.txt)
	def readFeaturesFromCSV(self):
		with open(self.filename) as f:
		    content = f.readlines()
		# you may also want to remove whitespace characters like `\n` at the end of each line
		content = [x.strip() for x in content] 
		return content



		# f = open("features3.csv", 'wt')
  #       try:
  #           writer = csv.writer(f)
  #           for file in content:
  #               self.setParticipants(file)
  #               feat = self.reapFeatures()
  #               writer.writerow(feat["MALE"])
  #               writer.writerow(feat["FEMALE"])
  #       finally:
  #           f.close()



	#
	def getLabels(self):
