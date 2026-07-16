# Gas Station

## Question: 
## Find the starting gas station index that allows completing the full circuit.

def gas_station(str_arr):
    n = int(str_arr[0])
    stations = str_arr[1:]

    total_tank = 0
    current_tank = 0
    start_index = 0

    for i in range(n):
        gas, cost = map(int, stations[i].split(":"))
        balance = gas - cost

        total_tank += balance
        current_tank += balance

        if current_tank < 0:
            start_index = i + 1
            current_tank = 0

    return start_index + 1 if total_tank >= 0 else "impossible"

print(gas_station(["5", "1:2", "2:1", "3:4", "4:3", "5:2"]))  # Output: 2

## Interview note: 
### Greedy works because if tank fails at i, no station before i can be valid.
###Complexity: O(n)