from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

text = "check my balance"
vector = model.encode(text)

print(len(vector))
print(vector[:5])