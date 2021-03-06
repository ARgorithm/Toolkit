## Designs

This folder contains design files for each kind of data structure and algorithm included in ARgorithmToolkit. These designs are logical plans on how the states are generated and how they should be interpreted during the AR rendering.

### Format of writing design

YAML has been used due to it being easily read by humans compared to json and can also be read by machines

```yaml
date: Date
category: Template
author: Author
# This is a template design that needs to be kept in mind while designing and writing yml files

# in states , store a list of state related to the data structure
states: 
  - <state_name>:
      description : description of state # explain what the state has to render
      definition:
        <attribute1>: description [required] # add [required] if it is always present
        <attribute2>: description 
        
# in class , store a list of classes that handling structure [OPTIONAL]
class:
  - ARgorithmToolkit.subpackage.class:
      description: purpose of class

# in function , add list of functions included for structure along with the state they generate
functions:
  - <function_name1>:
      description: what function does
      function:
        name: ARgorithmToolkit.subpackage.class.function
        parameters:
          required:
            - required parameter
          not_required:
            - a not required parameter 
          # The state might need the not required parameter , in which case a default value should be set
      state: state that it generates
  
  - <function_name2>:
      description: what function does
      function: None # Function for this hasnt been added to program
      state: None # Function does not affect state


```

If you using as <img src="https://raw.githubusercontent.com/tomchen/stack-icons/master/logos/visual-studio-code.svg" style="height:21px;" /> VS Code your editor then you should have your editor configured with the schema of `.design.yml`