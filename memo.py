import csv
import os
import time

from bruteForce import get_sac_from_file
from utils import Memoization

memoization = Memoization()


def compute_and_recover(i, p1_left, p2_left, objets, start_time, timeout, best_solution):
    # Check if the timeout is reached
    if time.time() - start_time > timeout:
        raise TimeoutError("Timeout reached during the computation")

    if i < 0 or p1_left <= 0 or p2_left <= 0:
        return 0, []

    if (i, p1_left, p2_left) in memoization.cache:
        return memoization.cache[(i, p1_left, p2_left)]

    option1_value, option1_items = compute_and_recover(i - 1, p1_left, p2_left, objets, start_time, timeout,
                                                       best_solution)

    option2_value = 0
    option2_items = []
    if objets[i].p1 <= p1_left and objets[i].p2 <= p2_left:
        prev_value, prev_items = compute_and_recover(i - 1, p1_left - objets[i].p1, p2_left - objets[i].p2, objets,
                                                     start_time, timeout, best_solution)
        option2_value = objets[i].valeur + prev_value
        option2_items = [objets[i].id] + prev_items

    if option2_value > option1_value:
        best_value, best_items = option2_value, option2_items
    else:
        best_value, best_items = option1_value, option1_items

    # Update the best solution if it improves the current one
    if best_value > best_solution[0]:
        best_solution[0] = best_value
        best_solution[1] = best_items

    memoization.cache[(i, p1_left, p2_left)] = (best_value, best_items)
    return best_value, best_items


def sort_objects_by_potential(objets):
    return sorted(objets, key=lambda obj: obj.valeur / (obj.p1 + obj.p2), reverse=True)


def save_results_to_csv(results, filename):
    headers = ["Problem", "Max_Value", "Objects_Taken", "Avg_Execution_Time"]

    # Check if file exists and is non-empty
    file_exists = os.path.isfile(filename) and os.path.getsize(filename) > 0

    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(headers)  # write header only if file does not exist

        writer.writerows(results)


if __name__ == "__main__":
    timeouts = [10, 60, 120]  # your desired timeouts in seconds

    for i in range(1, 9):  # loop from pb1 to pb8
        results = []

        problem_name = f"pb{i}"
        file_path = f"objects/{problem_name}.txt"

        total_time = 0
        min_time = float("inf")
        max_time = 0

        # These variables might also need to be updated based on the variation in multiple runs
        max_value = 0
        objects_taken = []

        sac, objets = get_sac_from_file(file_path)
        objets = sort_objects_by_potential(objets)
        for timeout in timeouts:
            start_time = time.time()
            # Clear the cache at the beginning of each run
            memoization.cache.clear()
            # Maintain the best solution found [value, items]
            best_solution = [0, []]
            try:
                max_value, solution = compute_and_recover(len(objets) - 1, sac.p1Max, sac.p2Max, objets, start_time,
                                                          timeout, best_solution)
            except TimeoutError:
                max_value, solution = best_solution  # Use the best found solution on timeout
            end_time = time.time()
            # Display results
            print(f"\nResults for {problem_name}:")
            print(f"\nResults with a timeout of {timeout} seconds:")
            print(f"Max value: {max_value}")
            print(f"Objects taken: {solution}")
            results.append([problem_name, max_value, solution, timeout])

            save_results_to_csv(results, "results.csv")
