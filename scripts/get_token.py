import requests

url = "http://127.0.0.1:8000/api/api-token-auth/"
data = {
    "username": "admin",  # Změň na své uživatelské jméno
    "password": "admin"                # Změň na své heslo
}

response = requests.post(url, json=data)

# Vytiskni status kód a text odpovědi
print("Status kód:", response.status_code)
print("Odpověď serveru:", response.text)

if response.status_code == 200:
    token = response.json().get('token')
    print("Tvůj autentizační token:", token)
else:
    print("Chyba při získávání tokenu:", response.json())
