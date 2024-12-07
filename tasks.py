def sum_data(data, parameters):
    return sum(data)

def multiply_data(data, parameters):
    factor = parameters.get("factor", 1)
    return [x * factor for x in data]