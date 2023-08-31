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







def find_minimal_replacements(road_length, non_working_lights):
    replacements = 0
    working_lights = set(range(0, road_length // 20 + 1))

    while non_working_lights:
        light_to_replace = None
        max_illumination_deficit = 0

        for non_working_light in non_working_lights:
            illumination_needed = 1 - illumination(0)  # Initial illumination needed
            for working_light in working_lights:
                distance = abs(working_light - non_working_light) * 20
                if distance <= 90:  # Check within 90 meters
                    illumination_needed -= illumination(distance)
            
            if illumination_needed > max_illumination_deficit:
                light_to_replace = non_working_light
                max_illumination_deficit = illumination_needed

        if light_to_replace is None:
            break

        working_lights.add(light_to_replace)
        non_working_lights.remove(light_to_replace)
        replacements += 1

    return replacements

# Example usage
road_length = 2000000
non_working_lights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]  # Example non-working light indexes
minimal_replacements = find_minimal_replacements(road_length, non_working_lights)

print("Minimal number of replacements to achieve cumulative illumination of at least 1:", minimal_replacements)



lowest_illumination_index = find_lowest_illumination_index(road_length, non_working_lights)


print("Index of the street light to be replaced:", lowest_illumination_index)

