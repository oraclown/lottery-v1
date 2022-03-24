import pytest
from brownie import accounts
from time import time


@pytest.fixture(scope="module")
def lottery(Lottery):
    return accounts[0].deploy(Lottery, 60*60, 1, 1)


def test_deploy_lottery(lottery):
    assert lottery.address != None
    assert lottery._owner == accounts[0]
    assert lottery._name == "Lottery"
    assert lottery.balance() == 0

    assert lottery.ticket_cost() == 1
    assert lottery.for_the_boyz() == 1
    assert lottery.num_ticket_buyers() == 0

    # TODO how to test start and end times of the lottery?


def test_buy_ticket(lottery):
    pass


def test_buy_ticket_fail(lottery):
    pass


def test_choose_winner(lottery):
    pass


def test_choose_winner_fail(lottery):
    pass


def test_pay_winner(lottery):
    pass


def test_pay_winner_fail(lottery):
    pass
