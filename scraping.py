import json
from time import sleep
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm


def ultimo_resultado():
    with open("LotoFacilResultados.json", "r") as jogos:
        ultimo_jogo = json.load(jogos)
        return list(ultimo_jogo.keys())[-1]


def buscar_ultimo_concurso():
    url = 'http://loterias.caixa.gov.br/wps/portal/'

    conn = requests.get(url)
    soup = BeautifulSoup(conn.content, 'html.parser')
    lotofacil = soup.find_all('p', {'class': "description"})
    conn.close()
    return lotofacil[3].text.split()[1]

def salvar_concursos():
    url = 'http://loterias.caixa.gov.br/wps/portal/loterias/landing/lotofacil'

    options = Options()
    # options.add_argument("--headless")
    driver = webdriver.Chrome('C:\\Users\\darla\\anaconda3\\chromedriver.exe', options=options)
    wait = WebDriverWait(driver, 10)
    driver.get(url)

    # Último concurso em nosso arquivo
    ultimo_concurso_arquivo = ultimo_resultado()
    # Conecta na página e procura pelo elemento span que contém o número do concurso
    tag_com_numero_concurso = driver.find_element(By.XPATH, '//*[@id="resultados"]/div[1]/div/h2/span')
    pagina_numero_concurso = tag_com_numero_concurso.get_attribute('outerHTML')
    soup_numero_concurso = BeautifulSoup(pagina_numero_concurso, 'html.parser')
    numero_ultimo_concurso = soup_numero_concurso.text.split()[1]

    # Validar se o último concurso em nosso arquivo é o mesmo do último concurso na página da caixa
    iguais = ultimo_concurso_arquivo == numero_ultimo_concurso

    lista_numeros_concursos = []
    # Se for falso, faz o scraping de todos os concurso faltantes
    if not iguais:
        for concurso in tqdm(range(int(ultimo_concurso_arquivo) + 1, int(numero_ultimo_concurso) + 1)):
            wait.until(EC.presence_of_element_located((By.NAME, "concurso"))).send_keys(concurso)
            wait.until(EC.presence_of_element_located((By.NAME, "concurso"))).send_keys(Keys.ENTER)
            sleep(2)
            # Procura o elemento na página
            elemento = driver.find_element(By.XPATH,
                                           '//*[@id="resultados"]/div[2]/div/div/div[1]/ul')
            # Baixa o conteúdo daquele elemento
            html_content = elemento.get_attribute('outerHTML')
            # Parsea o conteúdo HTML encontrado
            soup = BeautifulSoup(html_content, 'html.parser')
            linhas_tabela = soup.find_all('li')
            if elemento:
                print(f"\nConcurso {concurso} encontrado com sucesso, aguarde a inclusão em nossa base.")
            else:
                print(f"Concurso {concurso} não foi encontrado")

            numeros = []
            for i, x in enumerate(linhas_tabela):
                numeros.append(int(x.get_text()[41:43]))
            # Adiciona todos os numeros na lista
            lista_numeros_concursos.append((concurso, numeros))
            # Apaga o campo de busca
            wait.until(EC.presence_of_element_located((By.NAME, "concurso"))).clear()
            # Espera 5 segundos até a próxima busca
            sleep(3)
            print("*"*80)

    with open("LotoFacilResultados.json", 'r') as arquivo:
        # Lê o arquivo
        dicionario_concursos = json.load(arquivo)

        for concurso, jogo in lista_numeros_concursos:
            dicionario_concursos[concurso] = jogo
        obj = json.dumps(dicionario_concursos)

        with open("LotoFacilResultados.json", "w") as concursos:
            concursos.write(obj)

    print("Todos os concursos encontrados foram salvos em nossa base com sucesso")

    driver.quit()


if __name__ == '__main__':
    salvar_concursos()

