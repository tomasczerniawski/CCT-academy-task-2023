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
    working_lights = [1] * (road_length // 20 + 1)  # Assume all lights are initially working

    for non_working_light in non_working_lights:
        working_lights[non_working_light] = 0  # Mark non-working light as not working

    while True:
        illumination_ok = True
        
        for idx in non_working_lights:
            illumination_sum = 0
            
            for i in range(len(working_lights)):
                if working_lights[i] == 1:
                    distance = abs(idx - i) * 20
                    illumination_value = illumination(distance) if illumination(distance) >= 0.01 else 0
                    illumination_sum += illumination_value
            
            if illumination_sum < 0.01 and working_lights[idx] == 1:
                illumination_ok = False
                break
            
            print(f"Non-working light {idx}: Total Illumination={illumination_sum}, Working Lights: {[i for i in range(len(working_lights)) if illumination(abs(i - idx) * 20) >= 0.01 and working_lights[i] == 1]}")
        
        if illumination_ok:
            break
        
        max_illumination_increase = -1
        light_to_replace = None
        
        new_non_working_lights = []
        
        for idx in non_working_lights:
            illumination_increase = 0
            
            for i in range(len(working_lights)):
                distance = abs(idx - i) * 20
                illumination_increase += illumination(distance) * (1 - working_lights[i])
            
            if illumination_increase > max_illumination_increase:
                max_illumination_increase = illumination_increase
                light_to_replace = idx
            else:
                new_non_working_lights.append(idx)
        
        if light_to_replace is None:
            break
        
        working_lights[light_to_replace] = 1
        non_working_lights = new_non_working_lights
        replacements += 1
        
    return replacements
# Example usage and printing
road_length = 2000000
non_working_lights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
minimal_replacements = find_minimal_replacements(road_length, non_working_lights)

print("Minimal number of replacements to achieve cumulative illumination of at least 1:", minimal_replacements)

lowest_illumination_index = find_lowest_illumination_index(road_length, non_working_lights)


print("Index of the street light to be replaced:", lowest_illumination_index)
print("Index of the street light to be replaced:", lowest_illumination_index)
