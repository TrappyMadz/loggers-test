import logging
from fastapi import FastAPI, Request, HTTPException
import os
import model
from pythonjsonlogger.json import JsonFormatter
import sys


LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

AUTHORIZED_DEBT = 100

logger = logging.getLogger('MyBank')
logger.setLevel(LOG_LEVEL)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(LOG_LEVEL)

formatter = JsonFormatter("%(asctime)s %(levelname)s %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

app = FastAPI()
balance = 100

logger.info('App Started !')

@app.get("/")
async def health(request: Request):
    logger.info(f"Health required by {request.client.host}.")
    return {"message" : "MyBank is healthy !"}

@app.get("/balance")
async def get_balance():
    logger.info(f"Balance requested ! Balance is {balance}.")
    message = f"Your balance is {balance}."
    if balance < 0 :
        logger.warning(f"Balance is negative ! The user is in debt.")
        message += "Watchout, you are in debt !"
    return {"message" : message}

@app.post("/deposit")
async def add_to_balance(deposit: model.Transaction):
    global balance
    if deposit.value <= 0:
        logger.error(f"Deposit must be a positive number ! Current deposit : {deposit.value}")
        raise HTTPException(status_code=400, detail=f"Deposit must be a positive number ! Current deposit : {deposit.value}")
    
    balance += deposit.value
    logger.info(f"{deposit.value} successfully added to balance. New balance : {balance}")
    return {"message" : f"{deposit.value} successfully added to balance. New balance : {balance}"}

@app.post("/withdrawal")
async def withdraw_from_balance(withdraw: model.Transaction):
    global balance

    if withdraw.value <= 0:
        logger.error(f"Withdrawal must be a positive number ! Current withdraw : {withdraw.value}")
        raise HTTPException(status_code=400, detail=f"Withdrawal must be a positive number ! Current withdraw : {withdraw.value}")

    message = ""
    if balance - withdraw.value < -AUTHORIZED_DEBT:
        logger.error(f"User don't have enough money ! Authorized debt : {AUTHORIZED_DEBT}, current balance : {balance}, withdrawal value : {withdraw.value}.")
        raise HTTPException(status_code=400, detail=f"You don't have enough money ! Current balance : {balance}. Current authorized debt : {AUTHORIZED_DEBT}.") 
    elif balance - withdraw.value <= 0:
        logger.warning(f"Balance is negative ! The user is in debt.")
        message += "Watchout, you are in debt !"
    
    balance -= withdraw.value
    logger.info(f"{withdraw.value} successfully withdrawn ! New balance : {balance}.")
    return {"message" : f"{withdraw.value} successfully withdrawn ! Your new balance : {balance}." + message}