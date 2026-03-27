#---------------------------------------------------------------------------------------------------
# Importando bibliotecas
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#---------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------
# Configurações do navegador
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')  # Iniciar maximizado
options.add_argument('--disable-infobars')  # Desabilitar infobars
options.add_argument('--disable-extensions')  # Desabilitar extensões
options.page_load_strategy = 'normal' # Vai carregar a página normalmente
#---------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------
# Inicializa os serviços do Chrome automaticamente usando as definições acima
driver = webdriver.Chrome(options=options)

# Abrindo PJE e fazendo o login
driver.get("https://pje1g.trf3.jus.br/pje/login.seam")

sleep(4)
#---------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------
#Tentando fazer login no PJE
try:
    # Identificando os IDs, inserindo as credenciais e entrando no PJE
    login = driver.find_element(By.ID, 'username').send_keys('') # ALTERAR CPF AQUI
    senha = driver.find_element(By.ID, 'password').send_keys('') # ALTERAR SENHA AQUI
    sleep(2)
    clic = driver.find_element(By.XPATH, '//*[@id="kc-login"]').click()

    sleep(6)

    print("Login concluído com sucesso!\n")

#Caso falhe
except:
    print("Falha no Login!\n")
    sleep(2)
    driver.quit()
#---------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------
# Redirecionar para uma URL específica do PJE após o login
nova_url = "https://pje1g.trf3.jus.br/pje/Push/listView.seam"
driver.get(nova_url)

sleep(6)
#---------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------
#FORMA DE CARREGAR A PAGÍNA COMPLETAMENTE ATÉ O FINAL
try:
    final_pagina = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.ID, 'j_id215:j_id219:j_id236')))         
    print("Final da página encontrado\n")

    total_processos_pagina = (final_pagina.text)[0:4] #Para um total de processos na página com 4 dígitos(PODE TROCAR PARA A QUANTIDADE DE DÍGITOS QUE QUISER)
    print(f"Total de processos para excluír: {total_processos_pagina}\n")

except:
    print("Erro ao achar o final da página!")
    driver.quit()

sleep(3)
#---------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------
#Lógica principal, é o loop do while que possibilita a exclusão de todos os processos usando uma lógica simples
contador = 1
while True:
    sleep(4)

    try:
        botao_excluir = driver.find_element(By.ID, f'j_id215:j_id219:0:excluiProcessoButton')
        botao_excluir.click()
        print("Botão de excluir encontrado!")
        print(f"Excluindo o processo...")

    except:
        print("Botão de excluir não encontrado!")

    sleep(2)

    #Clica na caixa de span que aparece
    alerta = driver.switch_to.alert
    alerta.accept()

    #Esperando aparecer a caixa de mensagem com a informação sobre o processo
    try:
        WebDriverWait(driver, 300).until(EC.visibility_of_element_located((By.ID, "dialogMessage")))
        sleep(3)
        print(f"Excluido {contador} processo!\n")
        contador += 1

    except:
        print(f"Não encontrado a caixa de mensagem!")        
    
    if total_processos_pagina == 300:
            print(f"300 Processos foram excluídos, caso precise excluir mais, rode o programa novamente.\n")
            break
#---------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------
#Fecha a janela e encerra o script
driver.quit()
print('Processamento concluído e os processos foram excluídos.')
#---------------------------------------------------------------------------------------------------
