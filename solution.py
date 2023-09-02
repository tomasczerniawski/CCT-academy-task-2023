import math
import cProfile
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

        # Calculate the total illumination for each broken light
        illumination_sums = [0] * len(non_working_lights)

        for i, idx in enumerate(non_working_lights):
            for j in range(len(working_lights)):
                if working_lights[j] == 1:
                    illumination_sums[i] += illumination_values[abs(idx - j)]

            # If the illumination sum for this broken light is less than 1, mark it as not okay
            if illumination_sums[i] < 1:
                illumination_ok = False

            # Print information for debugging if show_process is True
            if show_process:
                light_status = "NOW Working" if working_lights[idx] == 1 else "Non-working"
                print(f"{light_status} light {idx}: Total Illumination={illumination_sums[i]}, Working Lights: {[i for i in range(len(working_lights)) if illumination_values[abs(i - idx)] >= 0.01 and working_lights[i] == 1]}")

        # If all broken lights have at least 1 illumination, stop the loop
        if illumination_ok:
            break

        # Find the broken light that contributes the least illumination to the total
        min_illumination_light = None
        min_illumination_value = float('inf')

        for i, illumination_sum in enumerate(illumination_sums):
            if illumination_sum < min_illumination_value:
                min_illumination_light = non_working_lights[i]
                min_illumination_value = illumination_sum

        # Replace the light that contributes the least illumination with a working light
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
non_working_lights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 195]
minimal_replacements = find_minimal_replacements(road_length, non_working_lights)

print("Minimal number of replacements to achieve cumulative illumination of at least 1:", minimal_replacements)

# Ask the user if they want to see the process prints
user_choice = input("Do you want to see the process (yes/no)? ").strip().lower()
if user_choice == "yes":
    minimal_replacements = find_minimal_replacements(road_length, non_working_lights, show_process=True)

lowest_illumination_index = find_lowest_illumination_index(road_length, non_working_lights)

print("Index of the street light to be replaced:", lowest_illumination_index)
