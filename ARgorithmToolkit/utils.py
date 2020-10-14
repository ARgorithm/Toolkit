# Base template that all algorithms will use

# error class to simplify user debugging
class ARgorithmError(Exception):

  def __init__(self,*args):
    if args:
        self.message = args[0]
    else:
        self.message = None
        
  def __str__(self):
    if self.message:
        return f'{self.message}'
    else:
        return f"There's an error within ARgorithm template usage"


# the template class proves as a base for our algorithms
class Template:

    def __init__(self):
        self.desc = "Not specified"
        self.states = []

    def add_state(self,state):
        assert type(state) == State , ARgorithmError("state should be of Type state")
        self.states.append(state)

    def __str__(self):
        state_desc = "\n".join([x for x in self.states]) if len(self.states) > 0 else ""
        return f"{self.desc}\n{state_desc}"


# the state template class to ensure each state is of same structure

class State:
    def __init__(self,**kwargs):
        self.content = {}
        for x in ['state_type','state_def','comments']:
            try:
                self.content[x] = kwargs[x]
            except:
                raise ARgorithmError(f"{x} should be present in State arguments")

    def __str__(self):
        data = str(self.content)
        return data