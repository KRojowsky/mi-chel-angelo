from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import os
from django.http import HttpResponseRedirect
from django.http import HttpResponse
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
                   <div class="product-box">
                       <a href="{url}" class="product-link">
                           <div class="product-img-box">
                               <img src="{image_url}" alt="{product_name}">
                           </div>
                       </a>
                       <div class="product-details">
                           <div class="category">{selected_category}</div>
                           <div class="name">{product_name}</div>
                           <div class="description">{info4.get_text()}</div>
                           <div class="price">
                                <strong>{info2.get_text() if info2 else "Brak informacji"}</strong> <s class="old-price">{info1.get_text() if info1 else "Brak informacji"}</s>
                           </div>
                '''

                if info3:
                    product_blog += f'''
                           <div class="the-lowest-price">Najniższa cena z 30 dni przed obniżką: {info3.get_text()}</div>
                    '''

                product_blog += f'''
                           <div class="buy">
                               <a href="{url}">
                                   <div class="btn">Kup teraz</div>
                               </a>
                           </div>
                       </div>
                   </div>
                '''

                product_blog += '''
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
                    
                        .product-details .category,
                        .product-details .name,
                        .product-details .price,
                        .product-details .buy {
                            margin: 10px 0;
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
                            color: #888;
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
                    </style>
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

            except requests.exceptions.RequestException as e:
                error_message = f'Błąd podczas pobierania strony: {str(e)}'
                return render(request, 'creator/landing-page-creator.html', {'error_message': error_message})

    return render(request, 'creator/landing-page-creator.html')


def add_to_file(request):
    if request.method == 'POST':
        product_html = request.POST.get('product_html', '')
        file_path = os.path.join('opinions.txt')  # Update this path
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
    response_text = None
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')
        co = cohere.Client("8lO0Yt2Sbk80gVYgrn3IlucmAU151GEhtoQfIFow")

        message = f"{user_input}"
        try:
            response = co.chat(message=message)
            response_text = response.text
        except Exception as e:
            response_text = f'Error: {e}'

        return JsonResponse({'response_text': response_text})

    return render(request, 'creator/testerka.html')
