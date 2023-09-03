import math

def illumination(distance):
    return 3 ** (-(distance / 90) ** 2)

def find_closest_working_light_distance(non_working_light, working_lights):
    closest_distance = float('inf')

    for working_light in working_lights:
        dist = abs(working_light - non_working_light) * 20
        if dist < closest_distance:
            closest_distance = dist
    
    return closest_distance

def find_lowest_illumination_index(road_length, non_working_lights):
    min_illumination = float('inf')
    min_index = -1

    working_lights = set(range(0, road_length // 20 + 1)) - set(non_working_lights)

    for non_working_light in non_working_lights:
        illumination_at_light = illumination(find_closest_working_light_distance(non_working_light, working_lights))

        # Consider only working street lights providing illumination of at least 0.01
        valid_working_lights = [working_light for working_light in working_lights
                                if illumination(abs(working_light - non_working_light) * 20) >= 0.01]

        # Calculate cumulative illumination from valid working lights
        cumulative_illumination = illumination_at_light + sum(
            illumination(abs(working_light - non_working_light) * 20) for working_light in valid_working_lights)

        if cumulative_illumination < min_illumination:
            min_illumination = cumulative_illumination
            min_index = non_working_light
    
    return min_index

def calculate_illumination_values(road_length):
    illumination_values = [illumination(i * 20) if illumination(i * 20) >= 0.01 else 0 for i in range(road_length // 20 + 1)]
    return illumination_values

def find_minimal_replacements(road_length, non_working_lights, show_process=False):
    replacements = 0
    working_lights = [1] * (road_length // 20 + 1)  # Assume all lights are initially working

    for non_working_light in non_working_lights:
        working_lights[non_working_light] = 0  # Mark non-working light as not working

    illumination_values = calculate_illumination_values(road_length)

    while True:
        illumination_ok = True

        # Calculate the total illumination for each broken light using a dictionary
        illumination_sums = {}

        for idx in non_working_lights:
            illumination_sums[idx] = 0

        for j in range(len(working_lights)):
            if working_lights[j] == 1:
                for idx in non_working_lights:
                    illumination_sums[idx] += illumination_values[abs(idx - j)]

        # Check if the illumination sum for each broken light is less than 1
        for idx in non_working_lights:
            if illumination_sums[idx] < 1:
                illumination_ok = False

            # Print information if show_process is True
            if show_process:
                light_status = "REPLACED" if working_lights[idx] == 1 else "Non-working"
                print(f"{light_status} light {idx}: Total Illumination={illumination_sums[idx]}, Working Lights: {[i for i in range(len(working_lights)) if illumination_values[abs(i - idx)] >= 0.01 and working_lights[i] == 1]}")

        # If all broken lights have at least 1 illumination, stop the loop
        if illumination_ok:
            break

        # Find the broken light
        min_illumination_light = None
        min_illumination_value = float('inf')

        for idx in non_working_lights:
            if illumination_sums[idx] < min_illumination_value:
                min_illumination_light = idx
                min_illumination_value = illumination_sums[idx]

        # Check if min_illumination_light is a valid index before accessing illumination_sums
        if min_illumination_light is not None and min_illumination_light in illumination_sums:
            # Replace the broken light
            working_lights[min_illumination_light] = 1
            replacements += 1

            # Print information for debugging if show_process is True
            if show_process:
                if illumination_sums[min_illumination_light] >= 1:
                    light_status = "Now Working"
                else:
                    light_status = "Replacing"

                print()
                print(f"{light_status} light {min_illumination_light}. Total replacements: {replacements}")
                print()
            
    return replacements

# Example usage and printing

road_length = 2000000
non_working_lights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 40, 41, 42, 43, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62]
minimal_replacements = find_minimal_replacements(road_length, non_working_lights)

print("Minimal number of replacements to achieve cumulative illumination of at least 1:", minimal_replacements)

lowest_illumination_index = find_lowest_illumination_index(road_length, non_working_lights)

print("Index of the street light to be replaced:", lowest_illumination_index)

user_choice = input("Do you want to see the process (yes/no)? ").strip().lower()
if user_choice == "yes":
    minimal_replacements = find_minimal_replacements(road_length, non_working_lights, show_process=True)

