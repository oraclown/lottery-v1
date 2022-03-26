# @version ^0.3.1

NUM_TICKETS: constant(uint256) = 100

ticket_buyers: public(address[NUM_TICKETS])
tickets_bought: public(uint256)
winner: public(address)
winner_index: public(uint256)
winner_payout: public(uint256)
ticket_price: public(uint256)
lottery_start: public(uint256)
lottery_end: public(uint256)
for_the_boyz: public(uint256) # a portion of total payout sent to admin
admin: public(address)

event TicketBought:
    amount: uint256
    buyer: address

event WinnerPaid:
    amount: uint256
    winner: address


@external
def __init__(
    _buy_period: uint256, # in seconds
    _ticket_price: uint256,
    _admin_fee: uint256,
):
    assert _buy_period >= 60*60, "buy period must be at least 1 hour"
    assert _admin_fee <= 100, "admin fee must be from 0-100, representing a percentage"
    assert _admin_fee >= 0, "admin fee must be from 0-100, representing a percentage"

    self.lottery_start = block.timestamp
    self.lottery_end = self.lottery_start + _buy_period
    self.ticket_price = _ticket_price
    self.for_the_boyz = _admin_fee
    self.admin = msg.sender


@external
@payable
def buy_ticket():
    assert self.tickets_bought < NUM_TICKETS, "no more tickets available"
    assert block.timestamp <= self.lottery_end, "lottery has ended"
    assert msg.value >= self.ticket_price, "purchase underpriced"

    self.ticket_buyers[self.tickets_bought] = msg.sender
    self.tickets_bought += 1

    log TicketBought(self.ticket_price, msg.sender)


@external
def choose_winner():
    assert block.timestamp > self.lottery_end, "lottery isn't over"

    # Choose winner
    self.winner_index = convert(block.prevhash, uint256) % (self.tickets_bought + 1)
    self.winner = self.ticket_buyers[self.winner_index]

    # Reward function caller
    send(msg.sender, self.ticket_price)


@external
def pay_winner():
    assert self.winner != ZERO_ADDRESS, "choose_winner() must be called first"

    self.winner_payout = self.balance * (1 - self.for_the_boyz / 100) - self.ticket_price

    send(self.winner, self.winner_payout)
    send(self.admin, self.balance - self.ticket_price)
    send(msg.sender, self.balance)

    log WinnerPaid(self.winner_payout, self.winner)


@external
def num_tickets() -> uint256:
    return NUM_TICKETS

# TODO: make getter for entire ticket_buyers array
@external
def get_ticket_buyers() -> address[NUM_TICKETS]:
    return self.ticket_buyers
