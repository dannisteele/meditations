"""Deterministic, stateless shuffled schedule: every passage once per cycle."""

import random
from datetime import date


def _raw_shuffle(ids: list[str], cycle: int) -> list[str]:
    order = list(ids)
    random.Random(f"meditations-cycle-{cycle}").shuffle(order)
    return order


def order_for_cycle(ids: list[str], cycle: int) -> list[str]:
    order = _raw_shuffle(ids, cycle)
    # Swapping positions 0 and 1 never moves the last element (len >= 3),
    # so the previous cycle's last item comes straight from its raw shuffle.
    if cycle > 0 and len(order) > 1 and order[0] == _raw_shuffle(ids, cycle - 1)[-1]:
        order[0], order[1] = order[1], order[0]
    return order


def passage_id_for(day: date, start: date, ids: list[str]) -> str:
    k = (day - start).days
    if k < 0:
        raise ValueError(f"{day} is before schedule start {start}")
    return order_for_cycle(ids, k // len(ids))[k % len(ids)]
