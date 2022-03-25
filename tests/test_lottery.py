import pytest
from brownie import accounts
from time import time
from brownie.convert import EthAddress


@pytest.fixture(scope="module")
def lottery(Lottery):
    # return accounts[0].deploy(Lottery, 60*60, 1, 1)
    return Lottery.deploy(60*60, 1, 1, {"from": accounts[0]})


def test_deploy_lottery(lottery):
    assert lottery.address != None
    assert lottery._owner == accounts[0]
    assert lottery._name == "Lottery"
    assert lottery.balance() == 0

    assert lottery.ticket_buyers(0) == EthAddress("0x0000000000000000000000000000000000000000")
    assert lottery.num_ticket_buyers() == 0
    assert lottery.winner() == EthAddress("0x0000000000000000000000000000000000000000")
    assert lottery.winner_index() == 0
    assert lottery.winner_payout() == 0
    assert lottery.ticket_price() == 1
    assert abs(lottery.lottery_start()) - int(time()) < 1
    assert lottery.lottery_end() == lottery.lottery_start() + 60*60
    assert lottery.for_the_boyz() == 1
    assert lottery.admin() == accounts[0]


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
