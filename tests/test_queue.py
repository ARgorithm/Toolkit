import ARgorithmToolkit

algo = ARgorithmToolkit.StateSet()
queue = ARgorithmToolkit.Queue("q",algo)

def test_declare():
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == "queue_declare"

def test_operations():
    queue.push(3)
    queue.push(9)
    assert queue.body == [3,9]
   
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == "queue_push"
    
    assert queue.front() == 3
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == "queue_front"
    
    assert queue.back() == 9
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == "queue_back"

    assert queue.front() == queue.pop()
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == "queue_pop"
    assert queue.body == [9]

    queue.pop()
    try:
        queue.pop()
    except ARgorithmToolkit.ARgorithmError:
        pass

def test_size():
    assert queue.empty() and len(queue)==0

    