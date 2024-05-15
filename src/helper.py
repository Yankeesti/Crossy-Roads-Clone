import random
def pick_random(min : int, max: int,decimal_places: int) -> int:
    return round(random.uniform(min,max),decimal_places)