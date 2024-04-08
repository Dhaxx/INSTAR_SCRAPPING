import os

from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.get("https://www.botucatu.sp.gov.br/portal/editais/1")

btn_buscar = driver.find_element(By.ID, "buscar")
# input_ano_licitacao = driver.find_element(By.ID, "form_ano_processo")

# input_ano_licitacao.send_keys("2024")
btn_buscar.click()

while True:
    modals_processo = driver.find_elements(By.CLASS_NAME, "ed_cont_edital")

    for modal in modals_processo:
        try:
            discr = modal.find_element(By.CLASS_NAME, "ed_descricao_edital").text
            discr = discr.replace("'", "`")
        except:
            continue

        try:
            info_element = modal.find_element(By.CLASS_NAME, 'ed_info_edital')
            divs = info_element.find_elements(By.TAG_NAME, 'div')
                
            for div in divs:
                if"Nº Licitação:" in div.text:
                    # Extraindo o ano da licitação
                    licitacao = div.text.split(":")[1].strip()
                    ano = licitacao.split("/")[1]
                if "Nº Processo:" in div.text:
                    # Extraindo o número do processo
                    processo = div.text.split(":")[1].strip()
                    numero_processo = processo.split("/")[0]
        except:
            continue

        with open("output.txt", "a", encoding='utf-8') as file:
            file.write(f"update cadlic set discr = '{discr[:1024]}' where processo = '{numero_processo}' and ano = '{ano}';\n")
    
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        paginacao = driver.find_element(By.ID, 'campoPaginacao')
        max_value = paginacao.get_attribute('max')
        pagina_atual = paginacao.get_attribute('value')

        if int(pagina_atual) == int(max_value):
            break
        else:
            btn_proximo = driver.find_element(By.XPATH, '//*[@id="ed_conteudo"]/div[3]/div[5]/div/a[3]/div/span')
        btn_proximo.click()
    except:
        break
