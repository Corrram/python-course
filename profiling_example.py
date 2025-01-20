import time

def process_data(data):
    def normalize(numbers):
        max_val = max(numbers)
        return [x / max_val for x in numbers]

    def square(numbers):
        time.sleep(1)
        return [x * x for x in numbers]

    def sort_numbers(numbers):
        sorted_numbers = []
        while numbers:
            min_val = min(numbers)
            numbers.remove(min_val)
            sorted_numbers.append(min_val)
        return sorted_numbers

    data = normalize(data)
    data = square(data)
    data = sort_numbers(data)
    return data

if __name__ == '__main__':
    import random

    long_list = [random.randint(1, 100) for _ in range(30_000)]
    result = process_data(long_list)