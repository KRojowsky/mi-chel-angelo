from django.shortcuts import render
import requests
from bs4 import BeautifulSoup


def widget(request):
    return render(request, 'creator/index.html')


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

                if convert:
                    return render(request, 'creator/index.html', {
                        'product_html': product_html,
                        'content': content,
                        'selected_category': selected_category,
                        'image_url': image_url,
                        'product_id': product_id,
                        'custom_name': custom_name
                    })

                return render(request, 'creator/index.html', {
                    'content': content,
                    'selected_category': selected_category,
                    'image_url': image_url,
                    'product_id': product_id,
                    'custom_name': custom_name
                })

            except requests.exceptions.RequestException as e:
                error_message = f'Błąd podczas pobierania strony: {str(e)}'
                return render(request, 'creator/index.html', {'error_message': error_message})

    return render(request, 'creator/index.html')
