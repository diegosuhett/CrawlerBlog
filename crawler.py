from uteis import *

class Crawler:

    base_url = ''
    num_pages = 0
    num_links_pages = 0
    retorno = []

    def __init__(self, base_url, num_pages, num_links_pages):
        Crawler.base_url = base_url
        Crawler.num_pages = num_pages
        Crawler.num_links_pages = num_links_pages
        self.separa_paginas()

    @staticmethod
    def separa_paginas():
        res = retorna_html_parse(Crawler.base_url)
        count = 1

        try:
            for links in res.find_all('a', class_='page'):
                if count <= Crawler.num_pages:
                    print('Crawler página: ' + str(count))
                    url = links.get('href')
                    Crawler.links_por_page(url)
                    count += 1
                else:
                    break
        except Exception as e:
            print('Error: ' + str(e))

        print(Crawler.retorno)

    @staticmethod
    def links_por_page(url_pagina):
        res = retorna_html_parse(url_pagina)
        count = 1
        for link in res.find_all('a', class_='link'):
            if count <= Crawler.num_links_pages:
                url = link.get('href')
                print('Varrendo link: "' + url + '"')

                result = Crawler.percorre_page(url)
                Crawler.retorno.append(result)
                count += 1
            else:
                break

    @staticmethod
    def percorre_page(page_url):
        res_pagina = retorna_html_parse(page_url)

        titulo = res_pagina.find('h1', class_='entry-title').text
        sub_titulo = res_pagina.find('div', class_='resumo').text
        autor = res_pagina.find('span', class_='fn').text
        data_post = formata_data(res_pagina.find('span', class_='post-date updated').text)

        content_imagem_titulo = res_pagina.find_all('meta', attrs={'itemprop': 'url'})
        content_imagem_body = res_pagina.find_all('figure', class_='wp-block-image')
        content_video = res_pagina.find_all('source')
        imagens = Crawler.busca_imagem(content_imagem_titulo, content_imagem_body)
        videos = Crawler.busca_video(content_video)

        dicionario = {"titulo": titulo,
            "sub-titulo": sub_titulo,
            "autor": autor,
            "data": data_post,
            "links-imagens": imagens,
            "links-video": videos}

        return dicionario

    @staticmethod
    def busca_imagem(html_imagem_titulo, html_imagem_body):
        array_imagem = []
        for link_titulo in html_imagem_titulo:
            link_titulo_split = str(link_titulo).split('"')
            array_imagem.append(link_titulo_split[1])

        for link_body in html_imagem_body:
            link_body_split = str(link_body).split('"')

            if len(link_body_split) >= 16:
                array_imagem.append(link_body_split[15])

        return array_imagem

    @staticmethod
    def busca_video(html_video):
        array_video = []
        for link in html_video:
            link_split = str(link).split('"')
            array_video.append(link_split[1])

        return array_video