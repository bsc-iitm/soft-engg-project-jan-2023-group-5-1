from sentence_transformers import SentenceTransformer

print('Starting download...')
model = SentenceTransformer('paraphrase-distilroberta-base-v2')
print('Model Download complete...')