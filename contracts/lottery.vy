# @version ^0.3.1

NUM_TICKETS: constant(uint256) = 1024

ticket_buyers: address[NUM_TICKETS]
num_ticket_buyers: uint256
winner: address
winner_index: uint256
winner_payout: uint256
ticket_cost: uint256
buy_period_start_block: uint256
buy_period_end_block: uint256
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
    _buy_period_start_block: uint256,
    _buy_period_end_block: uint256,
    _ticket_cost: uint256,
    _admin_fee: uint256,
):
    assert _buy_period_start_block >= block.number, "can't time travel"
    assert _buy_period_end_block > _buy_period_start_block, "ticket-buying window too small"
    assert _admin_fee < 1

    self.buy_period_start_block = _buy_period_start_block
    self.buy_period_end_block = _buy_period_end_block
    self.ticket_cost = _ticket_cost
    self.for_the_boyz = _admin_fee
    self.admin = msg.sender


@external
@payable
def buy_ticket():
    assert self.num_ticket_buyers < NUM_TICKETS, "no more tickets available"
    assert block.number >= self.buy_period_start_block, "buy period hasn't started"
    assert block.number <= self.buy_period_end_block, "buy period has ended"
    assert msg.value >= self.ticket_cost, "purchase underpriced"

    self.ticket_buyers[self.num_ticket_buyers] = msg.sender
    self.num_ticket_buyers += 1

    log TicketBought(self.ticket_cost, msg.sender)


@external
def choose_winner():
    assert block.number > self.buy_period_end_block, "ticket-buying time not done"

    # Choose winner
    self.winner_index = convert(block.prevhash, uint256) % (self.num_ticket_buyers + 1)
    self.winner = self.ticket_buyers[self.winner_index]

    # Reward function caller
    send(msg.sender, self.ticket_cost)


@external
def pay_winner():
    assert self.winner != ZERO_ADDRESS, "choose_winner() must be called first"

    self.winner_payout = self.balance * (1 - self.for_the_boyz) - self.ticket_cost
    send(self.winner, self.winner_payout)
    send(self.admin, self.balance - self.ticket_cost)
    send(msg.sender, self.balance)

    log WinnerPaid(self.winner_payout, self.winner)
