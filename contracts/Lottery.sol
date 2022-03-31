// SPDX-License-Identifier: MIT
pragma solidity >=0.8.13;

contract Lottery {
    uint256 public maxTickets;
    address[] public ticketBuyers;
    uint256 public ticketsBought;
    uint256 public ticketPrice;
    address public winner;
    uint256 public lotteryStart;
    uint256 public lotteryEnd;
    uint256 public forTheBoyz;
    address public admin;


    event ticketBought(address buyer, uint amount, uint ticketsBought);
    event winnerPicked(address winner, uint ticketsBought);
    event winnerPaid(address winner, uint amount);


    constructor(
        uint _maxTickets,
        uint256 _ticketPrice,
        uint256 _buyPeriod,
        uint256 _adminFee
    ) {
        require(_maxTickets > 0, "Max tickets must be greater than 0");
        require(_ticketPrice > 0, "Ticket price must be greater than 0");
        require(_buyPeriod >= 60*60, "Buy period must be at least 1 hour");
        require(_adminFee >= 0, "Admin fee must be 0-100, representing 0-100%");
        require(_adminFee <= 100, "Admin fee must be 0-100, representing 0-100%");
        
        maxTickets = _maxTickets;
        ticketPrice = _ticketPrice;
        lotteryStart = block.timestamp;
        lotteryEnd = lotteryStart + _buyPeriod;
        forTheBoyz = _adminFee;
        admin = msg.sender;
    }


    function buyTicket() public payable {
        require(block.timestamp <= lotteryEnd, "Lottery is over");
        require(ticketsBought < maxTickets, "No more tickets left");
        require(msg.value >= ticketPrice, "Ticket purchase underpriced");

        ticketBuyers.push(msg.sender);
        ticketsBought++;

        emit ticketBought(msg.sender, msg.value, ticketsBought);
    }


    function chooseWinner() public {
        require(block.timestamp > lotteryEnd);

        uint winnerIndex = uint(blockhash(block.number - 1)) % (ticketsBought + 1);
        winner = ticketBuyers[winnerIndex];

        (bool sent,) = msg.sender.call{value: ticketPrice}("");
        require(sent, "Failed to send reward for choosing the winner");

        emit winnerPicked(winner, ticketsBought);
    }


    function payWinner() public {
        require(winner != address(0));

        uint winnerPayout = address(this).balance * (1 - forTheBoyz / 100) - ticketPrice;
        (bool sent1,) = winner.call{value: winnerPayout}("");
        require(sent1, "Failed to send reward to the winner");
        emit winnerPaid(winner, winnerPayout);

        (bool sent2,) = admin.call{value: address(this).balance - ticketPrice}("");
        require(sent2, "Failed to send admin fee");

        (bool sent3,) = msg.sender.call{value: address(this).balance}("");
        require(sent3, "Failed to send reward for function caller");
    }


    function getTicketBuyers() public view returns (address[] memory) {
        return ticketBuyers;
    }
}