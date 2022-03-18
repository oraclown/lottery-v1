# Lottery V1

Lottery contract creator specifies the start and length time (start + interval) of the lottery.
People can buy tickets to the lottery only during the interval period. After the interval time has elapsed,
a lottery winner is chosen.

To buy tickets, people pay with a specified amount of a unique token. This token's is in `contracts/token.vy`. To make this token available to potential ticket-buyers, airdrop it to participants in the testnet run or put it on Uniswap somehow.

To pick a winner, uniformly project a random seed evenly across a number of choices (ticket buyers). Lottery V1 will use the block hash after a certain time interval as the random seed. Security issues with this seed are discussed later. Not sure why, but [projecting the hash string directly results in an uneven distribution](https://stats.stackexchange.com/questions/26344/how-to-uniformly-project-a-hash-to-a-fixed-number-of-buckets), so the hash string must first be converted to a large number before moded. Python example:
```python
def random_choice(block_hash_string: str, num_ticket_buyers: int) -> int:
    choice = 0

    for i in range(len(block_hash_string)):
        choice += 16**i*block_hash_string[i]

    return choice % num_ticket_buyers

ticket_buyers = ["0xfakeaddr1..", "0xfakeaddr2", "0xfakeaddr3"]
winner_idx = random_choice("fakeblockhashstr", len(ticket_buyers))
print("winner", ticket_buyers[winner_idx])
```
Why a [simpler way](https://stackoverflow.com/questions/33809770/hash-function-that-can-return-a-integer-range-based-on-string) doesn't work? Not sure. Onwards.

That's it. Keep it simple and maybe improve in a later version...
    