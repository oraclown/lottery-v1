import pytest
from brownie import accounts
from time import time
from brownie.convert import EthAddress
import brownie


@pytest.fixture(scope="module")
def lottery(Lottery):
    # return accounts[0].deploy(Lottery, 60*60, 1, 1)
    return Lottery.deploy(10, 1, 60*60, 1, {"from": accounts[0]})

    # get block at time of deployment
    # it will contain the timestamp at the time of deployment
    # TODO


def test_deploy_lottery(lottery):
    assert lottery.address != None
    assert lottery._owner == accounts[0]
    assert lottery._name == "Lottery"
    assert lottery.balance() == 0

    assert lottery.maxTickets() == 10
    assert lottery.getTicketBuyers() == []
    assert lottery.ticketsBought() == 0
    assert lottery.ticketPrice() == 1
    assert lottery.winner() == EthAddress("0x0000000000000000000000000000000000000000")
    assert abs(lottery.lotteryStart()) - int(time()) < 1
    assert lottery.lotteryEnd() == lottery.lotteryStart() + 60*60
    assert lottery.forTheBoyz() == 1
    assert lottery.admin() == accounts[0]


def test_buy_ticket(lottery):
    lottery.buyTicket({"from": accounts[1], "value": 1})

    assert accounts[1].balance() == 999999999999999999999
    assert lottery.balance() == 1
    assert lottery.ticketsBought() == 1
    assert lottery.ticketBuyers(0) == accounts[1]


def test_buy_ticket_fail(lottery):
    print('start')
    with brownie.reverts("Ticket purchase underpriced"):
        lottery.buyTicket({"from": accounts[1], "value": 0})
    print('here')
    # Buy all tickets so none left
    tickets_available = lottery.maxTickets() - lottery.ticketsBought()
    for i in range(tickets_available):
        lottery.buyTicket({"from": accounts[1], "value": 1})
    
    with brownie.reverts("No more tickets left"):
        lottery.buyTicket({"from": accounts[1], "value": 1})
    
    # TODO: how to test when number of available tickets == 10**6?
    # because looping 10**6 times and buying a ticket each time takes forever

    # TODO: test when lottery is over


def test_choose_winner(lottery):
    pass


def test_choose_winner_fail(lottery):
    pass


def test_pay_winner(lottery):
    pass


def test_pay_winner_fail(lottery):
    pass
