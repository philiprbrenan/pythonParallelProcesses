import random, subprocess, time

def wait_and_remove_first_completed(processes, wait=1, timeout=7200):           # Waits for the first subprocess in the list to complete and removes it from the list.
  start_time = time.time()                                                      # Start time

  while True:                                                                   # Wait uptil timeout for the next process to finish
    for i, proc in enumerate(processes):                                        # Processes executing in parallel
      if proc.poll() is not None:                                               # Test process for completion
        processes.pop(i)                                                        # Remove completed process
        return                                                                  # Successfully waited for the next prcess to complete

    if (time.time() - start_time) > timeout:                                    # Time out if we have to wait to long for a process to  finish
      print(f"No subprocess finished within the timeout period of {timeout}.")

    time.sleep(wait)                                                            # Wait a bit before trying again


if __name__ == "__main__":
  processes = []                                                                # Processes being run
  N         = 40                                                                # Total number of processes to run
  P         = 10                                                                # Number to run in parallel
  D         =  2                                                                # Dispersion of wait times

  print("Action Done Count")

  i = 0                                                                         # Number of processes launched so far
  for i in range(N):
    print(f"Start {i+1:5d} {len(processes):5d}")
    if len(processes) >= P:                                                     # Room to start another process
      wait_and_remove_first_completed(processes)
    s = D + random.randint(0, D)                                                # Time to sleep in process
    processes.append(subprocess.Popen(["sleep", f"{s}"]))

  while processes:                                                              # Wait for remaining processes to complete
    print(f"Wait {len(processes):12d}")
    processes.pop().wait()

  print("Finished")
