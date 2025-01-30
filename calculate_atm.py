def get_atm(diff: int, ltp) -> int:
    current_strike = ltp - (ltp % diff)
    next_higher_strike = current_strike + diff
    if ltp - current_strike < next_higher_strike - ltp:
        return int(current_strike)
    return int(next_higher_strike)

print(get_atm(50, 23620.9)) # 23600

