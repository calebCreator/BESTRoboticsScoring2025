import os
import json
from typing import List, Dict, Any, Optional, Callable, Union
import sqlite3

import main

import postProcessing
import shutil
from datetime import datetime


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

def calcualteTotalScore(match):
    global pointValues
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


def copy_database(src_db: Optional[str] = None, dest_db: Optional[str] = None) -> str:
    """
    Create a copy of the SQLite database file `scorecard.db`.

    - If `src_db` is not provided, the function looks for `scorecard.db` next to
      this module (`src/scorecard.db`).
    - If `dest_db` is not provided the function creates a filename next to the
      source file with suffix `_copy_YYYYmmdd_HHMMSS`.

    Returns the path to the copied file. Raises FileNotFoundError if the source
    database doesn't exist.
    """
    if src_db is None:
        # default to the directory above this module
        src_db = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scorecard.db')

    # resolve relative path
    if not os.path.isabs(src_db):
        src_db = os.path.join(os.path.dirname(os.path.dirname(__file__)), src_db)

    if not os.path.exists(src_db):
        raise FileNotFoundError(f"Source database not found: {src_db}")

    if dest_db is None:
        base, ext = os.path.splitext(src_db)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        #dest_db = f"{base}_copy_{timestamp}{ext}"
        dest_db = f"{base}_copy.db"

    shutil.copy2(src_db, dest_db)
    return dest_db


def set_column_for_all_rows(db_path: Optional[str] = None,
                            table: str = 'scoress',
                            column: str = 'ZtotalScore',
                            value_or_callable: Union[int, Callable[[Dict[str, Any]], int]] = 0) -> int:
    """
    Iterate over all rows in `table` inside `db_path` and set `column` to a new value.

    - `db_path` defaults to the file `scorecard.db` in the directory above this module.
    - `value_or_callable` may be an int (the value to set for every row) or a
      callable that receives a dictionary of the row (including 'rowid') and
      returns an int to set for that specific row.

    Returns the number of rows updated.
    """
    if db_path is None:
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scorecard_copy.db')

    if not os.path.isabs(db_path):
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), db_path)

    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database not found: {db_path}")

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Retrieve rowid and all columns so the callable has context
    cur.execute(f"SELECT rowid, * FROM {table}")
    cols = [d[0] for d in cur.description]  # first entry will be 'rowid'
    rows = cur.fetchall()

    updated = 0
    for r in rows:
        row = dict(zip(cols, r))
        if callable(value_or_callable):
            new_val = value_or_callable(row)
        else:
            new_val = value_or_callable

        # perform the update by rowid
        cur.execute(f"UPDATE {table} SET {column} = ? WHERE rowid = ?", (new_val, row['rowid']))
        updated += cur.rowcount

    conn.commit()
    conn.close()
    return updated

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
    print(calcualteTotalScore(matches[10]))

    copy_database()
    set_column_for_all_rows(value_or_callable = calcualteTotalScore)

    #for match in matches:
    #    print(str(match) + "\n\n\n")




