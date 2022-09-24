import os
import re
from bs4 import BeautifulSoup
import requests
import shutil

for pages in range(1, 31):
    print("O processo está na pagina {}".format(pages))
    page = requests.get("https://www.adorocinema.com/filmes/melhores/genero-13025/?page={}".format(pages))
    soup = BeautifulSoup(page.text, features="html.parser")

    titulos = []
    direcao = []
    genero = []
    elenco = []
    sinopse = []

    link_puro = []
    direcao_puro = []
    elenco_puro = []
    genero_puro = []

    imgs_links = []
    a = []

    coluna1 = []
    coluna2 = []
    coluna3 = []

    # Obtém o titulo
    for i in soup.find_all("a", class_="meta-title-link"):
        texto_puro = i.getText()
        titulos += [texto_puro]

    # Obtém os gêneros
    for i in soup.find_all("div", class_='meta-body-item meta-body-info'):
        genero_puro += [i.getText().strip()]

    # Organiza os gêneros
    for x in range(len(genero_puro)):
        genero += [''.join(genero_puro[x].splitlines())]
        genero[x] = genero[x].replace(",", ", ")
        genero[x] = strValue = re.sub(".*/", '', genero[x])

    # Obtém os diretores
    for i in soup.find_all("div", class_="meta-body-item meta-body-direction"):
        direcao_puro += [i.getText().strip()]

    # Organiza os diretores
    for x in range(len(direcao_puro)):
        direcao += [''.join(direcao_puro[x].splitlines())]
        direcao[x] = direcao[x].replace("Direção:", "")
        direcao[x] = direcao[x].replace(",", ", ")

    # Obtém o elenco
    for i in soup.find_all("div", class_='meta-body-item meta-body-actor'):
        elenco_puro += [i.getText().strip()]

    # Organiza o elenco
    for x in range(len(elenco_puro)):
        elenco += [''.join(elenco_puro[x].splitlines())]
        elenco[x] = elenco[x].replace("Elenco:", "")
        elenco[x] = elenco[x].replace(",", ", ")

    # Obtém a sinopse
    for i in soup.find_all("div", class_="content-txt"):
        texto_puro = i.getText().strip()
        sinopse += [texto_puro]

    # Obtém as imagens
    for i in soup.find_all("img", class_='thumbnail-img'):
        link_puro += [i]

    # Filtra apenas os links do 'link_puro' e armazena
    for x in range(len(link_puro)):
        a += re.findall(r'(https?://\S+)', str(link_puro[x]))
        # Remover '"' nos links
        imgs_links += [str(a[x]).replace('"', "")]

    # Cria as pastas e copia os arquivos samples
    if os.path.exists(("pagina {}".format(pages))):
        continue
    else:
        os.mkdir("pagina {}".format(pages))

        if os.path.exists("pagina {}/img".format(pages)):
            continue
        else:
            os.mkdir("pagina {}/img".format(pages))

        if os.path.exists("pagina {}/css".format(pages)):
            continue
        else:
            os.mkdir("pagina {}/css".format(pages))
            shutil.copy2('sample/style.css', 'pagina {}/css'.format(pages))

    # Baixa todas imagens
    for i in range(len(titulos)):
        img_data = requests.get(imgs_links[i]).content
        with open('pagina {}/img/{}'.format(pages, titulos[i]) + '.jpg', 'wb') as handler:
            handler.write(img_data)

    # Editando os arquivos -
    h1 = []
    img = []
    span_direcao = []
    span_genero = []
    span_elenco = []
    p_sinopse = []
    next_page = []
    previous_page = []

    with open("sample/sample.htm") as f:
        soup_file = BeautifulSoup(f, features="html.parser")

        # Encontra as imagens
        for i in soup_file.find_all("img", class_='img-cartaz'):
            img += [i]

        # Insere o local das imagens
        for i in range(len(img)):
            img[i]['src'] = 'img/{}'.format(titulos[i] + '.jpg')

        # Encontra a tag tittle
        for i in soup_file.find_all("h1", class_='tittle'):
            h1 += [i]

        # Insere o titulo
        for i in range(len(h1)):
            h1[i].insert(0, titulos[i])

        # Encontra a tag gênero
        for i in soup_file.find_all("span", class_='genero'):
            span_genero += [i]

        # Insere gênero
        for i in range(len(span_genero)):
            span_genero[i].insert(0, genero[i])

        # Encontra a tag direção
        for i in soup_file.find_all("span", class_='direcao'):
            span_direcao += [i]

        # Insere direcão
        for i in range(len(span_direcao)):
            span_direcao[i].insert(0, direcao[i])

        # Encontra a tag elenco
        for i in soup_file.find_all("span", class_='elenco'):
            span_elenco += [i]

        # Insere elenco
        for i in range(len(span_elenco)):
            span_elenco[i].insert(0, elenco[i])

        # Encontra a tag limiter(sinopse)
        for i in soup_file.find_all("p", id='limiter'):
            p_sinopse += [i]

        # Insere a sinopse
        for i in range(len(p_sinopse)):
            p_sinopse[i].insert(0, sinopse[i])

        # Encontra as próximas paginas
        previous_page = soup_file.find("a", class_='previous-page')
        next_page = soup_file.find("a", class_='next-page')

        if pages == 1:
            next_page['href'] = '../pagina {}/sample.htm'.format(pages + 1)
        if pages == 30:
            previous_page['href'] = '../pagina {}/sample.htm'.format(pages - 1)
        else:
            next_page['href'] = '../pagina {}/sample.htm'.format(pages + 1)
            previous_page['href'] = '../pagina {}/sample.htm'.format(pages - 1)

        # Salva as alterações
        html = soup_file.prettify("utf-8")
        with open("pagina {}/sample.htm".format(pages), "wb") as file:
            file.write(html)
