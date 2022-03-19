# Lottery V1

Lottery contract creator specifies the ticket buying period (start & end blocks) of the lottery.
People can buy tickets to the lottery only during that window. After the interval time has elapsed,
a lottery winner is chosen and the pot is given to the winner.

To buy tickets, people pay some MATIC.

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
From the above stackexchange link: `..the first letter is more influential than the second..`

^This might not apply because the distribution of characters within the block hash itself is random, so it doesn't matter if the characters near the beginning of the hash are more likely to influence the random choice. Could test this by making a plot of random choices and orders of characters in a hash string.

Why a [simpler way](https://stackoverflow.com/questions/33809770/hash-function-that-can-return-a-integer-range-based-on-string) doesn't work? Not sure. Onwards.

Because of more chats with @heavychain^, the `random_choice` algo I'll use first will probably just be `blockhash % num_ticket_buyers`.
The blockhash is of a block number determined by the contract owner in the constructor. Once that block number has passed,
ticket buyers can trigger the `declare_winner` and `give_winner_rewards` functions. The `declare_winner`
function gets the block hash by calling a function of the Tellor oracle using the `BlockHash` query type query ID 
given the current chain ID and block number set at contract creation. The blockhash value retrieved from
Tellor oracle must have been reported long ago enough to allow for disputes and chain re-organizations.
Both the `declare_winner` and `give_winner_rewards` functions can be called by anyone, and give the
function caller a small reward, so that calling these functions is incentivised.

That's it. Keep it simple and maybe improve in a later version...

Thanks @heavychain for all the help!
    