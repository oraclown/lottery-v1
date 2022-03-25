import pytest
from brownie import accounts
from time import time
from brownie.convert import EthAddress
import brownie


@pytest.fixture(scope="module")
def lottery(Lottery):
    # return accounts[0].deploy(Lottery, 60*60, 1, 1)
    return Lottery.deploy(60*60, 1, 1, {"from": accounts[0]})

    # get block at time of deployment
    # it will contain the timestamp at the time of deployment
    # TODO


def test_deploy_lottery(lottery):
    assert lottery.address != None
    assert lottery._owner == accounts[0]
    assert lottery._name == "Lottery"
    assert lottery.balance() == 0

    # TODO: write getter function for entire ticket_buyers array
    assert lottery.ticket_buyers(0) == EthAddress("0x0000000000000000000000000000000000000000")
    assert lottery.tickets_bought() == 0
    assert lottery.winner() == EthAddress("0x0000000000000000000000000000000000000000")
    assert lottery.winner_index() == 0
    assert lottery.winner_payout() == 0
    assert lottery.ticket_price() == 1
    assert abs(lottery.lottery_start()) - int(time()) < 1
    assert lottery.lottery_end() == lottery.lottery_start() + 60*60
    assert lottery.for_the_boyz() == 1
    assert lottery.admin() == accounts[0]


def test_buy_ticket(lottery):
    lottery.buy_ticket({"from": accounts[1], "value": 1})

    assert accounts[1].balance() == 999999999999999999999
    assert lottery.balance() == 1
    assert lottery.tickets_bought() == 1
    assert lottery.ticket_buyers(0) == accounts[1]


def test_buy_ticket_fail(lottery):
    with brownie.reverts("purchase underpriced"):
        lottery.buy_ticket({"from": accounts[1], "value": 0})
    
    # Buy all tickets so none left
    tickets_available = lottery.num_tickets({'from': accounts[1]}).return_value
    for i in range(tickets_available - lottery.tickets_bought()):
        lottery.buy_ticket({"from": accounts[1], "value": 1})
    
    with brownie.reverts("no more tickets available"):
        lottery.buy_ticket({"from": accounts[1], "value": 1})
    
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
