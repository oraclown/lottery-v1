# @version ^0.3.1

NUM_TICKETS: constant(uint256) = 1024

ticket_buyers: address[NUM_TICKETS]
num_ticket_buyers: uint256
winner: address
winner_index: uint256

ticket_cost: uint256
buy_period_start_block: uint256
buy_period_end_block: uint256
for_the_boyz: uint256 # a portion of total payout sent to admin

@external
def __init__(
    _buy_period_start_block: uint256,
    _buy_period_end_block: uint256,
    _admin_fee: uint256,
    _ticket_cost: uint256,
):
    assert _buy_period_start_block >= block.number, "can't time travel"
    assert _buy_period_end_block > _buy_period_start_block, "ticket-buying window too small"

    self.buy_period_start_block = _buy_period_start_block
    self.buy_period_end_block = _buy_period_end_block
    self.ticket_cost = _ticket_cost
    self.for_the_boyz = _admin_fee


@external
@payable
def buy_ticket():
    assert self.num_ticket_buyers < NUM_TICKETS, "no more tickets available"
    assert block.number >= self.buy_period_start_block, "buy period hasn't started"
    assert block.number <= self.buy_period_end_block, "buy period has ended"
    assert msg.value >= self.ticket_cost, "purchase underpriced"

    self.ticket_buyers[self.num_ticket_buyers] = msg.sender
    self.num_ticket_buyers += 1


@external
def choose_winner():
    assert block.number > self.buy_period_end_block, "ticket-buying time not done"

    # Choose winner
    self.winner_index = convert(block.prevhash, uint256) % (self.num_ticket_buyers + 1)
    self.winner = self.ticket_buyers[self.winner_index]

    # Reward function caller
    # TODO


@external
def pay_winner():
    # ensure winner is chosen
    # give some matic to function caller
    # give some matic to admin
    # TODO
    pass



