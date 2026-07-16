# Coin Determiner

## Question: 
## Return the minimum number of coins needed to make the given amount using [1, 5, 7, 9, 11].

def coin_determiner(num):
    coins = [1, 5, 7, 9, 11]
    dp = [float("inf")] * (num + 1)
    dp[0] = 0

    for amount in range(1, num + 1):
        for coin in coins:
            if amount >= coin:
                dp[amount] = min(dp[amount], dp[amount - coin] + 1)

    return dp[num]

## Interview note: 
## Greedy does not always work here, so dynamic programming is safer.
## Complexity: O(amount × coins).