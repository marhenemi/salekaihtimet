"""
Created: linre-90/15.3.2024
"""
import pickle
import time
from collections import deque
from s_utils import minutes_to_seconds


MEM_QUE = deque([]) # Memory
MEMQ_LEN = 50 # How many entries memory module can remember.


class MemFsFormat():
    """
    Format to save memory to disk in temporary power outages, etc. 
    Stored memory should be considered stale after 30 min.
    """
    def __init__(self, timestamp, data) -> None:
        self.timestamp = timestamp
        self.data = data


def __write_mem_file(data: deque, current_timestamp: float):
    """Save memory content fo file system file."""
    file = "s_mem.mem"
    memFileContent = MemFsFormat(current_timestamp, data)
    with open(file, "wb") as f:
        pickle.dump(memFileContent, f)


def __read_mem_file(current_timestamp: float):
    """Read memory contents from filesystem"""
    try:
        file = "s_mem.mem"
        with open(file, "rb") as f:
            memFileContent = pickle.load(f)
            if len(memFileContent.data) <= 0 or len(memFileContent.data) > MEMQ_LEN:
                # Stored Mem size is too big, ignore everything
                return None
            if abs(current_timestamp - memFileContent.timestamp) < minutes_to_seconds(30):
                # Check data age
                return memFileContent.data
            return None
    except Exception as e:
        return None # Does not matter what is wrong don't use file contents


def init_memory(adjust_interval: int, snapshot_interval: int, current_timestamp: float)->None:
    """Initialize memory module. 
    'Adjust_interval' is interval when motor adjusts, passed in as minutes. 
    'snapshot_interval' is passed in as seconds.
    """
    # Set max len
    global MEMQ_LEN
    MEMQ_LEN = int(minutes_to_seconds(adjust_interval) / snapshot_interval)
    # Try to restore from filesystem
    fileQueue = __read_mem_file(current_timestamp)
    if fileQueue != None and len(fileQueue) > 0:
        global MEM_QUE
        MEM_QUE = fileQueue


def use_memory(val: float, current_timestamp: float)->None:
    """
    Insert new value to memory.
    """
    if len(MEM_QUE) < MEMQ_LEN:
        # There is still room
        MEM_QUE.appendleft(val)
    else:
        # queueu is full and old value needs to be popped before adding new
        MEM_QUE.pop()
        MEM_QUE.appendleft(val)
    # Save memory state to file in different thread
    __write_mem_file(MEM_QUE, current_timestamp)


def read_mem_average()->float:
    """Calculate average value of items stored in memory. Returns -1 if memory is not full yet otherwise average."""
    memLen = len(MEM_QUE)
    if memLen < MEMQ_LEN:
        return -1
    return sum(MEM_QUE) / memLen


def is_memory_hydrated():
    """Check if memory contains enough data to be usable."""
    return len(MEM_QUE) == MEMQ_LEN


"""
********************* TESTS ************************
"""

def __test_clean_up():
    MEM_QUE.clear()


def __test__mem_insert_len():
    for x in range(0,60):
        use_memory(x, time.time())
    assert len(MEM_QUE) == 50, "Queue too long error"
    print("\tTest pass __test__mem_insert_len")
    __test_clean_up()


def __test__mem_average():
    for x in range(0,60):
        use_memory(1, time.time())
    assert read_mem_average() == 1, "Queue average error"
    __test_clean_up()

    for x in range(0,60):
        use_memory(x, time.time())
    assert read_mem_average() == 34.5, "Queue average error"

    print("\tTest pass __test__mem_average")
    __test_clean_up()


def __test__mem_hydration_test():
    for x in range(0,60):
        use_memory(x, time.time())
    assert True == is_memory_hydrated(), "Memory should be hydrated with these values"
    __test_clean_up()

    for x in range(0,20):
        use_memory(x, time.time())
    assert False == is_memory_hydrated(), "Memory should not be hydrated with these values"
    __test_clean_up()
    print("\tTest pass __test__mem_hydration_test")


def __test__mem_timestamp():
    t = time.time()
    for x in range(0,60):
        use_memory(x, t)
    
    assert __read_mem_file(t +  minutes_to_seconds(69)) == None, "Cached memory should be invalid."
    assert __read_mem_file(t +  minutes_to_seconds(30)) == None, "Cached memory should be invalid."
    assert __read_mem_file(t +  minutes_to_seconds(21)) != None, "Cached memory should be valid."
    assert __read_mem_file(t +  minutes_to_seconds(29)) != None, "Cached memory should be valid."

    print("\tTest pass __test__mem_timestamp")
    __test_clean_up()


if __name__ == "__main__":
    init_memory(5, 6, time.time())
    print("Running memory module tests...")
    __test__mem_insert_len()
    __test__mem_average()
    __test__mem_hydration_test()
    __test__mem_timestamp()
    print("Memory module tests all passed...")
