import os
import json
from typing import List, Dict, Any, Optional

import main

import postProcessing


def load_inputs_as_list(json_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Load input definitions from `inputs.json` and return a list of dictionaries.

    Each top-level key in the JSON (for example "Net True Factoids Installed") becomes
    one dictionary in the returned list. The dictionary contains a `name` key (the
    stripped input label) plus the properties defined in the JSON file for that input.

    If `json_path` is not provided the function will look for `public/inputs.json`
    next to this module (`src/public/inputs.json`). On error this returns an empty list.
    """
    if json_path is None:
        json_path = os.path.join(os.path.dirname(__file__), 'public', 'inputs.json')

    try:
        with open(json_path, 'r', encoding='utf-8') as fh:
            data = json.load(fh)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

    if not isinstance(data, dict):
        return []

    out: List[Dict[str, Any]] = []
    for key, value in data.items():
        entry: Dict[str, Any] = { 'name': key.strip() }
        # If the value is a mapping, merge its keys; otherwise store raw value
        if isinstance(value, dict):
            # copy the inner dict (keys left as-is from the JSON)
            for k, v in value.items():
                entry[k] = v
        else:
            entry['value'] = value
        out.append(entry)

    return out



#This function converts the json file into a dictionary of inputs and their point value
def turnInputsIntoPointValues(inputs):
    pointValues = {}

    for item in inputs:
        #Make the keys match the keys used in the database
        name = main.standardize(item["name"])
        
        value = item["pointValue"]

        #Convert from string to integers
        #if list
        if "," in value:
            #Turn into list
            value = value.split(",")

            #Turn elements in the list into ints
            for i in range(len(value)):
                value[i] = int(value[i])
        else:
            #Turn the value into an int
            value = int(value)


        #print(str(name) + ": " + str(value))
        pointValues[name] = value

    return pointValues

def calcualteTotalScore(match, pointValues):
    total = 0

    #Print matching column names
    # for input in match:
    #     if not input in pointValues.keys():
    #         print(str(input) + " not in pointValues")

    #     else:
    #         print(str(input) + " in pointValues")

    for input in match:
        #If it is in the point scoring
        if input in pointValues.keys():

            #Get the points that the team scored in the match
            try:
                scoreEntered = int(match[input])
            except:
                if match[input] == "true" or match[input] == "on":
                    scoreEntered = 1
                else:
                    scoreEntered = 0

            pointValue = pointValues[input]

            #See if the point value is a list
            if isinstance(pointValue, list):
                #If it is, get the right value from the list
                pointValue = pointValue[scoreEntered]

            points  = scoreEntered * pointValue
            #print(points)

            total += points
    


    return total

if __name__ == '__main__':
    # demo: load inputs.json and print a compact summary
    inputs = load_inputs_as_list(os.path.join(os.path.dirname(__file__), 'public', 'inputs.json'))
    print(f"Loaded {len(inputs)} input definitions")
    #for item in inputs:
        #print(item)
        #print(f"- {item.get('name')}: type={item.get('type')} maxInput={item.get('maxInput')}")

    pointValues = turnInputsIntoPointValues(inputs)
    #print(pointValues)



    matches = postProcessing.rows_to_dicts("scorecard.db", "SELECT * FROM scoress")
    #print(matches[0])
    print(calcualteTotalScore(matches[10], pointValues))
    #for match in matches:
    #    print(str(match) + "\n\n\n")




