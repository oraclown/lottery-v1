import pytest
from brownie import accounts, chain
from time import time
from brownie.convert import EthAddress
from brownie.convert.datatypes import Wei
import brownie
import random


LOTTERY_LENGTH = 60*60 # 1 hour
MAX_TICKETS = 13
TICKET_PRICE = 3
ADMIN_FEE = 1
GROSS_PAYOUT = MAX_TICKETS*TICKET_PRICE


def find_account(address):
    for account in accounts:
        if account.address == address:
            return account
    return None


@pytest.fixture(scope="function")
def lottery(LotteryV1):
    return LotteryV1.deploy(MAX_TICKETS, TICKET_PRICE, LOTTERY_LENGTH, ADMIN_FEE, {"from": accounts[0]})


def test_deploy_lottery(lottery):
    assert lottery.address != None
    assert lottery._owner == accounts[0]
    assert lottery._name == "LotteryV1"
    assert lottery.balance() == 0

    assert lottery.maxTickets() == MAX_TICKETS
    assert lottery.getTicketBuyers() == []
    assert lottery.ticketsBought() == 0
    assert lottery.ticketPrice() == TICKET_PRICE
    assert lottery.winner() == EthAddress("0x0000000000000000000000000000000000000000")
    assert abs(lottery.lotteryStart()) - int(time()) < 1
    assert lottery.lotteryEnd() == lottery.lotteryStart() + LOTTERY_LENGTH
    assert lottery.forTheBoyz() == ADMIN_FEE
    assert lottery.admin() == accounts[0]
    assert lottery.payWinnerCalled() == False


def test_buy_ticket(lottery):
    lottery.buyTicket({"from": accounts[1], "value": TICKET_PRICE})

    assert accounts[1].balance() == Wei("1000 ether") - TICKET_PRICE
    assert lottery.balance() == TICKET_PRICE
    assert lottery.ticketsBought() == 1
    assert lottery.ticketBuyers(0) == accounts[1]


def test_buy_ticket_fail(lottery):
    # Try to buy a ticket without enough funds
    with brownie.reverts("Ticket purchase underpriced"):
        lottery.buyTicket({"from": accounts[1], "value": 0})

    # Try to buy when no tickets left
    tickets_available = lottery.maxTickets() - lottery.ticketsBought()
    for i in range(tickets_available):
        lottery.buyTicket({"from": accounts[1], "value": TICKET_PRICE})
    
    with brownie.reverts("No more tickets left"):
        lottery.buyTicket({"from": accounts[1], "value": TICKET_PRICE})
    
    # Try to buy when lottery has ended
    chain.sleep(LOTTERY_LENGTH + 1)
    with brownie.reverts("Lottery is over"):
        lottery.buyTicket({"from": accounts[1], "value": TICKET_PRICE})


def test_choose_and_pay_winner(lottery):
    # Buy all tickets with random accounts
    for i in range(MAX_TICKETS):
        lottery.buyTicket({"from": accounts[random.randint(1, 9)], "value": TICKET_PRICE})
    min_balance = min([account.balance() for account in accounts])

    assert lottery.balance() == MAX_TICKETS * TICKET_PRICE
    assert lottery.ticketsBought() == MAX_TICKETS
    for buyer in lottery.getTicketBuyers():
        assert find_account(buyer).balance() < Wei("1000 ether")
        assert buyer != EthAddress("0x0000000000000000000000000000000000000000")

    # Choose winner
    chain.sleep(LOTTERY_LENGTH + 1)
    prev_balance = accounts[0].balance()
    lottery.chooseWinner({"from": accounts[0]})

    assert accounts[0].balance() == prev_balance + TICKET_PRICE
    assert lottery.winner() != EthAddress("0x0000000000000000000000000000000000000000")

    # Pay winner
    lottery.payWinner({"from": accounts[0]})
    winner_balance = find_account(lottery.winner()).balance()

    assert lottery.balance() == 0
    assert accounts[0].balance() == prev_balance + TICKET_PRICE*2 + GROSS_PAYOUT*ADMIN_FEE/100
    assert winner_balance >= min_balance + GROSS_PAYOUT - accounts[0].balance()
    assert lottery.payWinnerCalled() == True


def test_choose_winner_fail(lottery):
    with brownie.reverts("Lottery not over"):
        lottery.chooseWinner({"from": accounts[0]})


def test_pay_winner_fail(lottery):
    with brownie.reverts("Choose winner first"):
        lottery.payWinner({"from": accounts[0]})


def test_donate_to_lottery(lottery):
    prev_balance = accounts[0].balance()
    accounts[0].transfer(lottery, "1 ether")

    assert lottery.balance() == Wei("1 ether")
    assert accounts[0].balance() == prev_balance - Wei("1 ether")
