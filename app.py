from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def formulario_reserva():
    return render_template('formulario.html')

@app.route('/buscar_hoteles', methods=['POST'])

def buscar_hoteles():
    nombre = request.form.get('nombre')

    # búsqueda en la página de Booking.com
    url = "https://www.booking.com/search.html?ss=" + nombre
    response = requests.get(url)

    print(url)

    soup = BeautifulSoup(response.text, "html.parser")
    # print(response.text)

    with open("soup.txt", "w", encoding="utf-8") as archivo:
        archivo.write(str(soup))
    
    # buscar nombres de los hoteles y guardar en un arreglo
    hoteles = []
    hotel_elements = soup.find_all("h3", class_="bui-card__title")
    for element in hotel_elements:
        nombre_hotel = element.text.strip()
        hoteles.append(nombre_hotel)

    # Obtener los 10 primeros hoteles encontrados
    hoteles_encontrados = hoteles[:10]

    return render_template('resultados.html', hoteles=hoteles_encontrados)

if __name__ == '__main__':
    app.run()