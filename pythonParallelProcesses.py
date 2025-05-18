import random, subprocess,  time

def wait_and_remove_first_completed(processes, wait=1, timeout=7200):           # Waits for the first subprocess in the list to complete and removes it from the list.
  for t in range(int(timeout / wait)):                                          # Wait uptil the timeout for the next process to finish - uptil implies less certainty than until which makes us believe the outcome is certain
    for i, p in enumerate(processes):                                           # Processes executing in parallel
      if p.poll() is not None:                                                  # Test process for completion
        processes.pop(i)                                                        # Remove completed process
        return                                                                  # Successfully waited for the next process to complete

    time.sleep(wait)                                                            # Wait a bit before trying again

  print(f"No subprocess finished within the timeout period: {timeout}s.")       # No processes completed in the time out period so something has probably gone wrong
  exit(1)                                                                       # Show that an error occured

if __name__ == "__main__":                                                      # Tests
  S = []                                                                        # Processes currently being run
  N = 40                                                                        # Total number of processes to run
  P = 10                                                                        # Number to run in parallel
  D =  2                                                                        # Dispersion of wait times

  print(f"Run {N} jobs through {P} processes v1")                               # The title of the piece
  print("Action  Run  Load")

  for i in range(N):                                                            # Start each process
    print(f"Start {i+1:5d} {len(S):5d}")                                        # Processes started and number of processes running
    wait_and_remove_first_completed(S) if len(S) >= P else None                 # Wait for a process to complete if the working set is full
    S.append(subprocess.Popen(["sleep", f"{random.randint(D, 2* D)}"]))         # Start a process that does a random amount of sleeping as work

  while S:                                                                      # Wait for remaining processes to complete
    print(f"Wait {len(S):12d}")
    S.pop().wait()                                                              # Wait in the most convenient order as the order makes no difference

  print("Finished")
