# Lottery V1

This is a simple lottery contract. The contract creator specifies a ticket-buying period, ticket cost, and admin fee.
People can buy lottery tickets (with the chain's native currency) only during the time alloted. After the buying window has passed,
a lottery winner is chosen and most of the pot is paid to them.

### Requirements:
- Python >= 3.9
- Install [ganache](https://github.com/trufflesuite/ganache)
- Install Python dependencies with [poetry](https://github.com/python-poetry/poetry):
```
poetry install
```

### Run tests:
```
poetry run brownie test
```

Thanks to [@heavychain](https://github.com/tkernell) for all the help!
    