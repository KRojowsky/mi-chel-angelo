from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import os
from django.http import HttpResponseRedirect
from django.http import JsonResponse
import cohere


def widget(request):
    return render(request, 'creator/widget.html')


def landing_page_creator(request):
    return render(request, 'creator/landing-page-creator.html')


def product_details(request):
    if request.method == 'GET':
        product_id = request.GET.get('product_id', None)
        category = request.GET.get('category', None)
        new_category = request.GET.get('new_category', None)
        convert = request.GET.get('convert', None)

        selected_category = new_category if category == "Inna" else category

        if product_id:
            url = f'https://mi-store.pl/product-xxx-{product_id}.html'

            try:
                response = requests.get(url)
                response.raise_for_status()
                html_content = response.text
                soup = BeautifulSoup(html_content, 'html.parser')

                info0 = soup.find('div', class_='projector_navigation').find('h1') if soup.find('div', class_='projector_navigation') else None
                info1 = soup.find('del', class_='projector_prices__maxprice') if soup.find('del', class_='projector_prices__maxprice') else None
                info2 = soup.find('strong', class_='projector_prices__price') if soup.find('strong', class_='projector_prices__price') else None
                info3 = soup.find('span', class_='omnibus_price__value') if soup.find('span', class_='omnibus_price__value') else None
                info4 = soup.find('div', class_='projector_description description') if soup.find('div', class_='projector_description description') else None
                custom_name = request.GET.get('custom_name', info0.get_text() if info0 else None)

                product_name = custom_name if custom_name else (info0.get_text() if info0 else "Brak informacji")

                content = [
                    product_name,
                    info2.get_text() if info2 else "Brak informacji",
                    info1.get_text() if info1 else "Brak informacji"
                ]

                if info3:
                    content.append(
                        f'Najniższa cena produktu w okresie 30 dni przed wprowadzeniem obniżki: {info3.get_text()}')

                image_url = f'https://mi-store.pl/xxx_pm_product-image-{product_id}_1.jpg'

                product_html = f'''
                    <div class="product-box product-bf2 col-xs-12 col-sm-4 col-md-3 col-lg-3" style="">
                        <a href="{url}" class="">
                            <div class="product-img-box product-badges">
                                <img src="{image_url}" alt="{product_name}">
                            </div>
                        </a>
                        <div class="">
                            <div class="col-md-12" style="font-size: 0.9rem; color: #515151;">{selected_category}</div>
                            <div class="col-md-12" style="padding-bottom: 0.5rem; font-weight: 800; font-size: 1.4rem; color: #353535;">{product_name}</div>
                            <div class="col-md-12" style="padding-bottom: 0.5rem; font-size: 2rem;">
                                 #OD# <strong style="color: #ff6900; font-family: Bold;">{info2.get_text() if info2 else "Brak informacji"}</strong> <s style="color: #515151; font-family: Light;">{info1.get_text() if info1 else "Brak informacji"}</s>
                            </div>
                '''

                if info3:
                    product_html += f'''
                            <div class="col-md-12" style="padding-bottom: 0.5rem; font-size: 0.7rem; color: #515151;">Najniższa cena z 30 dni przed obniżką: {info3.get_text()}</div>
                    '''

                product_html += '''
                        </div>
                        <div class="col-md-12">
                            <a href="{url}" style="text-decoration: none;">
                                <div class="btn-classic">Kup teraz</div>
                            </a>
                        </div>
                    </div>
                '''



                product_blog = f'''
                
                ################ POCZĄTEK KARTY Z PRODUKTEM (WKLEJASZ W MIEJSCE GDZIE CHCESZ MIEĆ PRODUKT)
                
                
                
                <div class="product-box" data-product-id="{product_id}">
                    <a class="product-link" href="https://mi-store.pl/product-xxx-{product_id}.html">
                        <div class="product-img-box">
                            <img src="{image_url}" alt="{product_name}">
                        </div>
                    </a>
                    <div class="product-details">
                        <div class="category">{selected_category}</div>
                        <div class="name">{product_name}</div>
                        <div class="description">{info4.get_text()}</div>
                        <div class="price">
                            <strong></strong> <s class="old-price"></s>
                        </div>
                        <div class="the-lowest-price"></div>
                        <div class="buy">
                            <a class="btn" href="https://mi-store.pl/product-xxx-{product_id}.html">Kup teraz</a>
                        </div>
                    </div>
                </div>
                    
                    
                    
                ################ POCZĄTEK KARTY Z PRODUKTEM
                
                
                
                
                
                
                
                
                
                
                ############### POCZĄTEK MAPY(WKLEJASZ W MIEJSCE GDZIE CHCESZ MIEĆ MAPĘ)
                
                
                
                <div id="container">
                    <div id="map"></div>
                    <div id="controls">
                        <button id="locate-button" onclick="locateUser()">Pokaż moją lokalizację</button>
                        <div id="nearest-location"></div>
                    </div>
                </div>
                
                
                
                ################ KONIEC MAPY
                
                
                
                
                
                
                
                
                
                '''



                product_blog += '''
                ################ POCZĄTEK TEGO CO LECI ZUPEŁNIE NA SAM KONIEC KODU
                 
                 
                 
                 <script>
                    async function fetchProductData(productId, container) {
                        const url = `https://mi-store.pl/product-pol-${productId}.html`;
                        const proxyUrl = `https://api.allorigins.win/raw?url=${encodeURIComponent(url)}`;

                        try {
                            const response = await fetch(proxyUrl);
                            const text = await response.text();

                            const parser = new DOMParser();
                            const doc = parser.parseFromString(text, 'text/html');

                            const priceElement = doc.querySelector('strong.projector_prices__price');
                            const oldPriceElement = doc.querySelector('del.projector_prices__maxprice');
                            const lowestPriceElement = doc.querySelector('span.omnibus_price__value');

                            container.querySelector('.price strong').innerText = priceElement ? priceElement.innerText : '';
                            container.querySelector('.old-price').innerText = oldPriceElement ? oldPriceElement.innerText : '';
                            container.querySelector('.the-lowest-price').innerText = lowestPriceElement ? `Najniższa cena z 30 dni przed obniżką: ${lowestPriceElement.innerText}` : '';
                        } catch (error) {
                            container.querySelector('.price strong').innerText = 'Nie udało sie pobrać ceny';
                            container.querySelector('.old-price').innerText = '';
                            container.querySelector('.the-lowest-price').innerText = '';
                        }
                    }
                    
                    document.querySelectorAll('.product-box').forEach(container => {
                        const productId = container.getAttribute('data-product-id');
                        fetchProductData(productId, container);
                    });
                </script>
                
                
                <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
                 <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
                 <script>
                 document.addEventListener('DOMContentLoaded', function() {
                        initMap();
                    });
                    
                    var map;
                    var userMarker;
                    var nearestMarker;
                    var nearestDistance = Infinity;
                    var nearestLocation = null;
                    
                    function initMap() {
                        map = L.map('map').setView([52.0, 19.0], 6);
                    
                        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                            attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                        }).addTo(map);
                    
                        var locations = [
                            {lat: 50.0875892, lon: 19.9853558, name: "Autoryzowany Salon Xiaomi Store w Krakowie<br>Centrum Handlowe Serenada, Kraków"},
                            {lat: 51.110, lon: 17.060, name: "Autoryzowany Salon Xiaomi Store we Wrocławiu<br>Pasaż Grunwaldzki, Wrocław"},
                            {lat: 52.406, lon: 16.933, name: "Autoryzowany Salon Xiaomi Store w Poznaniu<br>Centrum Posnania, Poznań"},
                            {lat: 50.259, lon: 19.022, name: "Autoryzowany Salon Xiaomi Store w Katowicach<br>Galeria Katowicka, Katowice"},
                            {lat: 54.380, lon: 18.600, name: "Autoryzowany Sklep Xiaomi Store w Gdańsku<br>Galeria Bałtycka, Gdańsk"},
                            {lat: 54.518, lon: 18.538, name: "Autoryzowany Salon Xiaomi Store w Gdyni<br>Centrum Riviera, Gdynia"},
                            {lat: 50.067, lon: 19.945, name: "Autoryzowany Salon Xiaomi Store w Krakowie<br>Galeria Krakowska, Kraków"},
                            {lat: 52.291, lon: 20.935, name: "Autoryzowany Salon Xiaomi Store w Warszawie<br>Galeria Młociny, Warszawa"},
                            {lat: 51.246, lon: 22.548, name: "Autoryzowany Salon Xiaomi Store w Lublinie<br>Centrum Handlowo-Rozrywkowe Lublin Plaza, Lublin"},
                            {lat: 50.037, lon: 22.004, name: "Autoryzowany Salon Xiaomi Store w Rzeszowie<br>Galeria Rzeszów, Rzeszów"},
                            {lat: 50.812, lon: 19.120, name: "Autoryzowany Salon Xiaomi Store w Częstochowie<br>Galeria Jurajska, Częstochowa"},
                            {lat: 52.400, lon: 16.920, name: "Autoryzowany Salon Xiaomi Store w Poznaniu<br>Centrum Avenida, Poznań"},
                            {lat: 50.320, lon: 19.090, name: "Autoryzowany Salon Xiaomi Store w Czeladzi<br>Centrum Handlowe M1, Czeladź"},
                            {lat: 51.779, lon: 19.448, name: "Autoryzowany Salon Xiaomi Store w Łodzi<br>Centrum Handlowe Manufaktura, Łódź"}
                        ];
                    
                        locations.forEach(function(location) {
                            var marker = L.marker([location.lat, location.lon]).addTo(map);
                            marker.bindPopup(location.name);
                        });
                    }
                    
                    function locateUser() {
                        if (navigator.geolocation) {
                            navigator.geolocation.getCurrentPosition(function(position) {
                                var lat = position.coords.latitude;
                                var lon = position.coords.longitude;
                                userMarker = L.marker([lat, lon], {color: 'blue'}).addTo(map);
                                map.setView([lat, lon], 13);
                                userMarker.bindPopup("Twoja przybliżona lokalizacja").openPopup();
                    
                                var locations = [
                                    {lat: 50.0875892, lon: 19.9853558, name: "Autoryzowany Salon Xiaomi Store w Krakowie<br>Centrum Handlowe Serenada, Kraków"},
                                    {lat: 51.110, lon: 17.060, name: "Autoryzowany Salon Xiaomi Store we Wrocławiu<br>Pasaż Grunwaldzki, Wrocław"},
                                    {lat: 52.406, lon: 16.933, name: "Autoryzowany Salon Xiaomi Store w Poznaniu<br>Centrum Posnania, Poznań"},
                                    {lat: 50.259, lon: 19.022, name: "Autoryzowany Salon Xiaomi Store w Katowicach<br>Galeria Katowicka, Katowice"},
                                    {lat: 54.380, lon: 18.600, name: "Autoryzowany Sklep Xiaomi Store w Gdańsku<br>Galeria Bałtycka, Gdańsk"},
                                    {lat: 54.518, lon: 18.538, name: "Autoryzowany Salon Xiaomi Store w Gdyni<br>Centrum Riviera, Gdynia"},
                                    {lat: 50.067, lon: 19.945, name: "Autoryzowany Salon Xiaomi Store w Krakowie<br>Galeria Krakowska, Kraków"},
                                    {lat: 52.291, lon: 20.935, name: "Autoryzowany Salon Xiaomi Store w Warszawie<br>Galeria Młociny, Warszawa"},
                                    {lat: 51.246, lon: 22.548, name: "Autoryzowany Salon Xiaomi Store w Lublinie<br>Centrum Handlowo-Rozrywkowe Lublin Plaza, Lublin"},
                                    {lat: 50.037, lon: 22.004, name: "Autoryzowany Salon Xiaomi Store w Rzeszowie<br>Galeria Rzeszów, Rzeszów"},
                                    {lat: 50.812, lon: 19.120, name: "Autoryzowany Salon Xiaomi Store w Częstochowie<br>Galeria Jurajska, Częstochowa"},
                                    {lat: 52.400, lon: 16.920, name: "Autoryzowany Salon Xiaomi Store w Poznaniu<br>Centrum Avenida, Poznań"},
                                    {lat: 50.320, lon: 19.090, name: "Autoryzowany Salon Xiaomi Store w Czeladzi<br>Centrum Handlowe M1, Czeladź"},
                                    {lat: 51.779, lon: 19.448, name: "Autoryzowany Salon Xiaomi Store w Łodzi<br>Centrum Handlowe Manufaktura, Łódź"}
                                ];
                    
                                locations.forEach(function(location) {
                                    var distance = getDistance(lat, lon, location.lat, location.lon);
                                    if (distance < nearestDistance) {
                                        nearestDistance = distance;
                                        nearestLocation = location;
                                        if (nearestMarker) {
                                            nearestMarker.setIcon(new L.Icon.Default());
                                        }
                                        nearestMarker = L.marker([location.lat, location.lon], {color: 'red'}).addTo(map);
                                        nearestMarker.bindPopup(location.name).openPopup();
                                    }
                                });
                    
                                document.getElementById('nearest-location').innerHTML = 
                                    `<b>Najbliższa lokalizacja:</b><br> ${nearestLocation.name} (${nearestDistance.toFixed(2)} km)`;
                            });
                        } else {
                            alert("Twoja przeglądarka nie obsługuje geolokalizacji.");
                        }
                    }
                    
                    function getDistance(lat1, lon1, lat2, lon2) {
                        var R = 6371;
                        var dLat = (lat2 - lat1) * Math.PI / 180;
                        var dLon = (lon2 - lon1) * Math.PI / 180;
                        var a = 
                            0.5 - Math.cos(dLat)/2 + 
                            Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * 
                            (1 - Math.cos(dLon))/2;
                    
                        return R * 2 * Math.asin(Math.sqrt(a));
                    }
                 </script>
                    
                <style>
                    @keyframes glow {
                        0% {
                            box-shadow: 0 0 0 #ff6600;
                        }
                        50% {
                            box-shadow: 0 0 20px #ff6600;
                        }
                        100% {
                            box-shadow: 0 0 0 #ff6600;
                        }
                    }
                
                    @keyframes float {
                        0% {
                            transform: translateY(10px);
                        }
                        50% {
                            transform: translateY(-10px);
                        }
                        100% {
                            transform: translateY(10px);
                        }
                    }
                
                    .product-box {
                        display: flex;
                        align-items: center;
                        box-sizing: border-box;
                        justify-content: space-between;
                    }
                
                    .product-img-box {
                        flex: 1;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        margin: 20px;
                    }
                
                    .product-img-box img {
                        max-width: 70%;
                        height: auto;
                        border-radius: 10px;
                        animation: float 5s ease-in-out infinite;
                        transition: transform 0.3s ease;
                    }
                
                    .product-details {
                        flex: 2;
                        padding: 0 20px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: flex-start;
                    }
                    
                    .product-details .name{
                        font-weight: bold;
                        padding-bottom: 10px;
                        font-size: 18px;
                    }
                    
                    .category, .old-price, .the-lowest-price{
                        color: #888;
                    }
                
                    .product-details .category,
                    .product-details .name,
                    .product-details .price,
                    .product-details .buy {
                        margin: 5px 0;
                        text-align: left;
                    }
                
                    .product-details .price {
                        display: flex;
                        align-items: center;
                    }
                
                    .product-details .price strong {
                        font-size: 25px;
                        color: #F3601F;
                        padding: 10px 0;
                    }
                
                    .product-details .price .old-price {
                        margin-left: 10px;
                        text-decoration: line-through;
                    }
                
                    .product-details .buy .btn {
                        display: inline-block;
                        padding: 10px 20px;
                        background-color: #ff6600;
                        color: #fff;
                        border-radius: 5px;
                        text-decoration: none;
                        text-align: center;
                        transition: background-color 0.3s ease, transform 0.3s ease;
                        animation: glow 2s infinite;
                        margin: 10px 0;
                    }
                
                    .btn:hover {
                        opacity: 0.6;
                        transition: 0.3s;
                    }
                
                    .product-details .buy .btn:hover {
                        background-color: #e65c00;
                        transform: translateY(-3px);
                    }
                    
                    @media (max-width: 768px) {
                        .product-box {
                            flex-direction: column;
                            align-items: center;
                            text-align: center;
                        }
                
                        .product-img-box {
                            margin: 10px;
                        }
                
                        .product-details {
                            padding: 0 10px;
                            align-items: center;
                        }
                
                        .product-details .price strong {
                            font-size: 20px;
                        }
                        
                        .product-details .buy .btn {
                            margin-bottom: 20px;
                        }
                    }
                    
                    #map {
                        height: 500px;
                        width: 100%;
                        max-width: 700px;
                        margin: 0 auto;
                        border-radius: 5px;
                        border: 1px solid #000;
                        border-style: dashed;
                    }
                    
                    #locate-button {
                        font-family: 'Roboto', Arial, sans-serif;
                        display: block;
                        margin: 20px auto;
                        padding: 10px 20px;
                        font-size: 16px;
                        cursor: pointer;
                        text-align: center;
                        border: 1px solid #333;
                        border-radius: 20px;
                        background-color: #FF6900;
                        color: #fff;
                    }
                    
                    #locate-button:hover {
                        box-shadow: 0 10px 10px 0 rgba(0,0,0,0.24);
                        opacity: .9;
                    }
                    
                    #nearest-location {
                        margin-top: 20px;
                        font-size: 16px;
                        text-align: center;
                        font-family: 'Roboto', Arial, sans-serif;
                        line-height: 1.4;
                    }
                </style>
                    
                    
                    
                ################ KONIEC TEGO CO LECI ZUPEŁNIE NA SAM KONIEC KODU
                '''



                if convert:
                    return render(request, 'creator/landing-page-creator.html', {
                        'product_html': product_html,
                        'product_blog': product_blog,
                        'content': content,
                        'selected_category': selected_category,
                        'image_url': image_url,
                        'product_id': product_id,
                        'custom_name': custom_name
                    })

                return render(request, 'creator/landing-page-creator.html', {
                    'content': content,
                    'selected_category': selected_category,
                    'image_url': image_url,
                    'product_id': product_id,
                    'custom_name': custom_name
                })

                patch_no_cache(response)
                return response

            except requests.exceptions.RequestException as e:
                error_message = f'Błąd podczas pobierania strony: {str(e)}'
                return render(request, 'creator/landing-page-creator.html', {'error_message': error_message})

    return render(request, 'creator/landing-page-creator.html')


def add_to_file(request):
    if request.method == 'POST':
        product_html = request.POST.get('product_html', '')
        file_path = os.path.join('opinions.txt')
        with open(file_path, 'a') as file:
            file.write(product_html + "\n")
        success_message = 'Kod HTML poprawnie utworzony'
        return render(request, 'creator/landing-page-creator.html', {'success_message': success_message})

    return render(request, 'creator/landing-page-creator.html')


def display_file_content(request):
    file_path = os.path.join('opinions.txt')
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
            wrapped_content = f'<div class="container lprow" style="">\n{file_content}</div>'
            return render(request, 'creator/landing-page-creator.html', {'file_content': wrapped_content})
    except FileNotFoundError:
        error_message = 'Plik opinions.txt nie istnieje.'
        return render(request, 'creator/landing-page-creator.html', {'error_message': error_message})


def clear_file_content(request):
    file_path = os.path.join('opinions.txt')
    try:
        open(file_path, 'w').close()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    except Exception as e:
        error_message = f'Błąd podczas czyszczenia pliku: {str(e)}'
        return render(request, 'creator/landing-page-creator.html', {'error_message': error_message})


def chatbot(request):
    return render(request, 'creator/chatbot.html')


def testerka(request):
    return render(request, 'creator/testerka.html')


def ninetygo(request):
    return render(request, 'creator/ninetygo.html')
