import pickle
#import pandas as pd
import nltk

from train import *

FILENAME = "crisis_data_01JAN2006_31DEC2008.p"

def filter_file(filename):
	"""
	Returns a list of lead paragraphs that contain the relevant keywords
	"""
	words = ['bank', 'market', 'crisis', 'finance', 'financial', 'downturn', 'credit']

	leadParas = [] 
	file = open("crisis_data_01JAN2006_31DEC2008.p", "rb")
	df = pickle.load(file)	#['date', 'headline', 'lead_paragraph', 'print_page', 'word_count']
	for row in df.iterrows():
		text = row[1]['lead_paragraph']
		for word in words:
			if word in text:
				leadParas.append(text)
				break
	return leadParas

def tokenize_para(paraList):
	"""
	Return a list of list ([ [] ]) of sentences that form each lead paragraph
	"""
	allSentences = []  
	for para in paraList:
		tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
		allSentences.append(tokenizer.tokenize(para))
	return allSentences

if __name__ == "__main__":
	allSentencesLists = tokenize_para(filter_file(FILENAME))
	for sentList in allSentencesLists:
		for sent in sentList:
			inputVec = map_sent_to_embedding(embeddings_ref, sent)
			inputVec = inputVec.reshape((1, inputVec.shape[0]))
			pred = clf.predict_classes(inputVec, verbose=0)
			# print(sent)
			# print(pred)


