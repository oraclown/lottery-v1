"""
Deploy Lottery contract

$ brownie run deploy_lottery.py --network ropsten

Deployed on Polygon Mumbai testnet:
https://mumbai.polygonscan.com/address/0x6cBa90fFcbA80d30D52798Be8C26e7236bA49322
"""
from brownie import accounts, LotteryV1
from brownie.convert.datatypes import Wei
import os
from dotenv import load_dotenv


load_dotenv()

MAX_TICKETS = 10**6
TICKET_PRICE = Wei("2 ether") # 2 MATIC
LOTTERY_LENGTH = 60*60*24 # 1 day
ADMIN_FEE = 3 # 3%


def main():
    acct = accounts.load(os.getenv("LOCAL_ACCOUNT_NAME"))
    LotteryV1.deploy(
        MAX_TICKETS,
        TICKET_PRICE,
        LOTTERY_LENGTH,
        ADMIN_FEE,
        {"from": acct},
        publish_source=True
    )

if __name__ == "__main__":
    main()
