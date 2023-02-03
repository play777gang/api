from fastapi import FastAPI
from pydantic import BaseModel

from pynubank import Nubank

nu = Nubank()

refresh_token = nu.authenticate_with_cert('18341606771', 'em88005424', 'src67e.p12')

# A variável feed conterá a página atual com as transações
print(nu.get_card_balance())