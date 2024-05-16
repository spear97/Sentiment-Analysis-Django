# Import necessary modules
from django.shortcuts import render
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import json

# Load pre-trained RoBERTa model and tokenizer
MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

# Define the index view
def index(request):
    return render(request, 'index.html')

# Define the sentiment_analysis view
def sentiment_analysis(request):
    # Check if the request method is POST
    if request.method == 'POST':
        # Get the input text from the request
        txt = request.POST.get('txt')

        # Tokenize the input text
        encoded_text = tokenizer(txt, return_tensors='pt')
        
        # Perform sentiment analysis using the pre-trained model
        output = model(**encoded_text)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)

        # Create a dictionary to store sentiment scores and input text
        scores_dict = {
            'neg': scores[0],
            'neu': scores[1],
            'pos': scores[2],
            'txt': json.dumps(txt),
        }

        # Render the index.html template with sentiment scores
        return render(request, 'index.html', scores_dict)