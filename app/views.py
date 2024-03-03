from rest_framework import viewsets
from .models import Todo
from .serializer import TodoSerializer
import requests


class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer


# Function to send a message to Telegram
def send_message(chat_id, text):
    token = "7125228403:AAFKCgfckkgW59N5yBZay5DlkakdPwk94vU"
    url = f"https://api.telegram.org/bot{7125228403:AAFKCgfckkgW59N5yBZay5DlkakdPwk94vU}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    response = requests.post(url, json=payload)
    return response.json()
