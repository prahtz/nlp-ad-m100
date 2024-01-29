import re


def create_time_aggregated_descriptions_dict(data, descriptions_dict):
    """
    Computes a dictionary that associates each aggregation column in 'data' to its description contained in 'descriptions_dict'
    """
    aggregation_dict = {
        "avg": "Average",
        "std": "Standard deviation of",
        "min": "Minimum",
        "max": "Maximum",
    }
    new_descriptions_dict = {}
    group_dict = {}
    for col in data.columns:
        if col != "timestamp" or col != "value":
            name = col[:-4]
            suffix = col[-3:]
            for group, (key, description) in enumerate(descriptions_dict.items()):
                x_idx = key.find("X")
                y_idx = key.find("Y")
                description = description[0].lower() + description[1:]
                if x_idx != -1 and y_idx == -1:
                    match = re.match(key[:x_idx] + "([0-9]+)" + key[x_idx + 1 :], name)
                    if match:
                        x = match[1]
                        description = re.sub("X", x, description)
                        new_descriptions_dict[name + f"_{suffix}"] = aggregation_dict[suffix] + " " + description
                        group_dict[name + f"_{suffix}"] = group
                        break

                elif x_idx != -1 and y_idx != -1:
                    match = re.match(key[:x_idx] + "([0-9]+)" + key[x_idx + 1 : y_idx] + "([0-9]+)" + key[y_idx + 1 :], name)
                    if match:
                        x, y = match[1], match[2]
                        description = re.sub("X", x, description)
                        description = re.sub("Y", y, description)
                        new_descriptions_dict[name + f"_{suffix}"] = aggregation_dict[suffix] + " " + description
                        group_dict[name + f"_{suffix}"] = group
                        break
                else:
                    if name == key:
                        new_descriptions_dict[name + f"_{suffix}"] = aggregation_dict[suffix] + " " + description
                        group_dict[name + f"_{suffix}"] = group
                        break
    return new_descriptions_dict, group_dict
