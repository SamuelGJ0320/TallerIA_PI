from django.shortcuts import render

from django.shortcuts import render
from movie.models import Movie
import os
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv

def get_embedding(text, client, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def recommendations(request):
    load_dotenv('api_keys_1.env')  # Cargar la API key de OpenAI
    client = OpenAI(api_key=os.getenv('openai_api_key'))

    query = request.GET.get('query')
    recommendations = []  # Cambiamos esto para ser una lista de recomendaciones

    if query:
        emb_req = get_embedding(query, client)
        items = Movie.objects.all()

        sim = []
        for movie in items:
            emb = np.frombuffer(movie.emb)
            sim.append(cosine_similarity(emb, emb_req))
        sim = np.array(sim)

        # Obtener los índices de las 5 películas más similares
        indices = np.argsort(sim)[-5:][::-1]  # Obtenemos los últimos 5 índices y los invertimos

        # Agregar las películas recomendadas a la lista
        for idx in indices:
            recommendations.append(items[int(idx)])  # Convertir a int aquí

    return render(request, 'recommendations.html', {'recommendations': recommendations})  # Cambia 'recommendation' a 'recommendations'
