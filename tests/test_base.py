import ARgorithmToolkit

def test_base():
    a = ARgorithmToolkit.StateSet()
    a.states.append('test state')
    assert( len(a.states) == 1 )
    
def test_state():
    try:
        ARgorithmToolkit.State(state_def="ErrorTest")
        assert False , 'No error raised'
    except ARgorithmToolkit.ARgorithmError:
        pass

def test_variable():
    algo = ARgorithmToolkit.StateSet()
    s = ARgorithmToolkit.Variable("s",algo,10)
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == 'variable_declare'
    s.value += 1
    assert s.value == 11
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == 'variable_highlight'

def test_comment_state():
    algo = ARgorithmToolkit.StateSet()
    algo.add_comment("Hello world")
    last_state = algo.states[-1]
    assert last_state.content['state_type'] == 'comment'
    assert last_state.content['comments'] == 'Hello world'
    assert last_state.content['state_def'] == None
