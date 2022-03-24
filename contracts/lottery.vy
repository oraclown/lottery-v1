# @version ^0.3.1

NUM_TICKETS: constant(uint256) = 10**6

ticket_buyers: address[NUM_TICKETS]
num_ticket_buyers: uint256
winner: address
winner_index: uint256
winner_payout: uint256
ticket_cost: uint256
lottery_start: uint256
lottery_end: uint256
for_the_boyz: uint256 # a portion of total payout sent to admin
admin: address

event TicketBought:
    amount: uint256
    buyer: address

event WinnerPaid:
    amount: uint256
    winner: address


@external
def __init__(
    _buy_period: uint256, # in seconds
    _ticket_cost: uint256,
    _admin_fee: uint256,
):
    assert _buy_period >= 60*60, "buy period must be at least 1 hour"
    assert _admin_fee <= 100, "admin fee must be from 0-100, representing a percentage"
    assert _admin_fee >= 0, "admin fee must be from 0-100, representing a percentage"

    self.lottery_start = block.timestamp
    self.lottery_end = self.lottery_start + _buy_period
    self.ticket_cost = _ticket_cost
    self.for_the_boyz = _admin_fee
    self.admin = msg.sender


@external
@payable
def buy_ticket():
    assert self.num_ticket_buyers < NUM_TICKETS, "no more tickets available"
    assert block.timestamp >= self.lottery_start, "lottery hasn't started"
    assert block.timestamp <= self.lottery_end, "lottery has ended"
    assert msg.value >= self.ticket_cost, "purchase underpriced"

    self.ticket_buyers[self.num_ticket_buyers] = msg.sender
    self.num_ticket_buyers += 1

    log TicketBought(self.ticket_cost, msg.sender)


@external
def choose_winner():
    assert block.timestamp > self.lottery_end, "lottery isn't over"

    # Choose winner
    self.winner_index = convert(block.prevhash, uint256) % (self.num_ticket_buyers + 1)
    self.winner = self.ticket_buyers[self.winner_index]

    # Reward function caller
    send(msg.sender, self.ticket_cost)


@external
def pay_winner():
    assert self.winner != ZERO_ADDRESS, "choose_winner() must be called first"

    self.winner_payout = self.balance * (1 - self.for_the_boyz / 100) - self.ticket_cost

    send(self.winner, self.winner_payout)
    send(self.admin, self.balance - self.ticket_cost)
    send(msg.sender, self.balance)

    log WinnerPaid(self.winner_payout, self.winner)
