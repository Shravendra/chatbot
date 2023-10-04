import json
import openai
from django.shortcuts import render
from django.views.decorators.csrf import  csrf_exempt
from langchain.llms import OpenAI
from django.http import JsonResponse



openai.api_key = "openai-api-key"


@csrf_exempt
def chatbot(request, query=None):
    if request.method == 'POST' or query is not None:
        query = query or request.POST.get('query')
        
        # Check if it is the first interaction
        if not query:
            response = "Hi, I am AI Bot. How may I help you?"
        else:
            # Generate response to user query
            prompt = "You: " + query + "\nAI Bot:"
            if len(prompt) <= 10:
                max_tokens = 64
            elif len(prompt) <= 20:
                max_tokens = 128
            elif len(prompt) <= 30:
                max_tokens = 256
            else:
                max_tokens = 2048

            response = openai.Completion.create(
                engine='text-davinci-003',
                prompt=prompt,
                max_tokens=max_tokens,
                n=1,
                stop=None,
                temperature=0.7,
            )
            response = response.choices[0].text.strip()
        
        # Return JSON response with answer
        return JsonResponse({'response': response})

    return render(request, 'chatbot/chatbot.html', {})


@csrf_exempt
def process_query(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            query = data.get('query')
            if not query:
                return JsonResponse({'response': 'Query is empty'})
            
            response = chatbot(request, query)
            answer = json.loads(response.content.decode('utf-8'))['response']
            
            # Return the complete answer
            return JsonResponse({'response': answer})
        
        except json.decoder.JSONDecodeError as e:
            return JsonResponse({'response': f'Error: {str(e)}'})
        
        except Exception as e:
            return JsonResponse({'response': f'Error: {str(e)}'})   
