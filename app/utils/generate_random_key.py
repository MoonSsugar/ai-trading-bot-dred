import random


def generate_key(amount: int) -> str:
    first_part = "nb" + "".join(random.choices("0123456789", k=2))
    second_part = "".join(random.choices("0123456789", k=4))
    third_part = "".join(random.choices("0123456789", k=2)) + "qx"

    return f"{first_part}-{second_part}-{third_part}"
