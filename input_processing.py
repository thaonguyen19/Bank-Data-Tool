import numpy as np

Dx = 50
Dy = 5
N = 239232
PRETRAINED_DATA = "glove.6B.50d.txt" 


def create_word_embedding(fileName):
	"""
	This maps an English word in the fileName to its 50-dim word embedding
	"""
	embeddings = {}	 
	file = open(fileName, 'r')
	for line in file:
		tokens = line.split()
		word = tokens[0]
		tokens.pop(0)
		embedding = np.zeros(Dx)
		for i in range(Dx):
			embedding[i] = float(tokens[i])
		embeddings[word] = embedding
	return embeddings


def map_sent_to_embedding(embeddings, sentence):	#return a concatenated matrix || average word vector???
	"""
	This returns the 50-dim vector that represents the average embedding for the whole sentence
	"""
	average_embedding = np.zeros(50)
	count = 0
	for word in sentence.split():
		if word in embeddings:
			average_embedding += embeddings[word]
			count += 1
	if (count==0) :
		return average_embedding
	else:
		return (average_embedding/count)


def map_sentences_scores(sentencesFile, scoresFile):
	"""
	This creates a training set that maps the average embedding for each sentence to its 
	corresponding sentiment score (1-5)
	"""
	file1 = open(sentencesFile, "r")
	file2 = open(scoresFile, "r")

	scores = []
	for line in file2:
		tokens = line.split("|")
		score = float(tokens[1])
		scores.append(score)
	scores = np.asarray(scores)
	scores = np.digitize(scores, np.array([0.0, 0.2, 0.4, 0.6, 0.8, 1.0]), right=True)

	outputs = np.zeros((N, Dy))
	for i in range(len(scores)):
		outputs[i, scores[i]-1] = 1

	############################################
	index_to_sentence = dict()
	for line in file1:
		tokens = line.split("|")
		# print(line)
		# print(tokens[1][:-1])
		index_to_sentence[int(tokens[1][:-1])] = tokens[0]

	index_to_sentence = sorted(index_to_sentence.items(), key=lambda s: s[0])	#sort sentences in order of their ids
	sentencesList = []
	for tup in index_to_sentence:	#tuple has the form (id, sentence)
		sentencesList.append(tup[1])

	inputs = np.zeros((N, Dx))
	for i in range(len(sentencesList)):
		inputs[i, :] = map_sent_to_embedding(embeddings_ref, sentencesList[i])
		
	return inputs, outputs	#return np.arrays

#inputs and corresponding labels
embeddings_ref = create_word_embedding(PRETRAINED_DATA)
inputs, outputs = map_sentences_scores("dictionary.txt", "sentiment_labels.txt")
print(outputs)