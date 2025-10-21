HOW TO USE JSON INPUTS
===================================
1. The key is the name of the input. NO DUPLICATE NAMES ALLOWED! The
key will be used as the name for the input label

2. "type" is the type of the input html element that will be used. 
Possible values: ["dropdown", "number", "checkbox"]

3. "options" is the set of options used in a dropdown element. Formatted
in a comma separated list format(Ex. "option1,option2,option3"). For "number" and 
"checkbox" elements, type "any".

4. "maxInput" is the maximum value "number" inputs can be incremented to. 
For "dropdown" and "checkbox" elements, use the value "none".

5. "pointValue" is the point value that the input's value is multiplied by.
For non-linear multipliers, express multipliers in list 
form(Ex. "0,3,9,27"). For non-linear multipliers, make sure that you 
include a "0" value, before the point value.

6. "multiplied" is a boolean that expresses whether or not the input is 
multiplied by an external scaling variable. ("true" or "false")

7. "lineBreak" is a boolean that defines whether or not the input has a 
newline character added after it. Should be defaulted to true. Used to 
add two inputs on the same horizontal line.