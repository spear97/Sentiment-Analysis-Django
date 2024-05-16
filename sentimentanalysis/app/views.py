from django.shortcuts import render
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax
import json

MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

# Create your views here.
def index(request):
    return render(request, 'index.html')

# Event that will Handle the Sentiment Analysis for this application
def sentiment_analysis(request):
    if request.method == 'POST':
        txt = request.POST.get('txt')

        encoded_text = tokenizer(txt, return_tensors='pt')
        output = model(**encoded_text)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)

        scores_dict = {
            'neg': scores[0],
            'neu': scores[1],
            'pos': scores[2],
            'txt': json.dumps(txt),
        }

        print(scores_dict)

        return render(request, 'index.html', scores_dict)