import random, subprocess, time

def wait_and_remove_first_completed(processes, wait=1, timeout=7200):           # Waits for the first subprocess in the list to complete and removes it from the list.
  for _, p in [[t, p] for t in range(int(timeout / wait)) for p in processes]:  # Cartesian product of waits and processes
    if p.poll() is not None: processes.remove(p); return                        # First process to complete
    if (p == processes[-1]): time.sleep(wait)                                   # Wait after each set of processes to give another process a chance to finish
  raise RuntimeError(f"No subprocess finished within the timeout: {timeout}s.");# No processes completed in the time out period so something has probably gone wrong

if __name__ == "__main__":                                                      # Tests
  S = []                                                                        # Processes currently being run
  N = 40                                                                        # Total number of processes to run
  P = 10                                                                        # Number to run in parallel
  D =  2                                                                        # Dispersion of wait times

  print(f"Run {N} jobs through {P} processes v1\nAction  Run  Load")            # The title of the piece

  for i in range(N):                                                            # Start each process
    print(f"Start {i+1:5d} {len(S):5d}")                                        # Processes started and number of processes running
    if len(S) >= P: wait_and_remove_first_completed(S)                          # Wait for a process to complete if the working set is full
    S.append(subprocess.Popen(["sleep", f"{random.randint(D, 2* D)}"]))         # Start a process that does a random amount of sleeping as work

  while S: print(f"Wait {len(S):12d}"); S.pop().wait()                          # Wait for remaining processes to complete                                            # Wait in the most convenient order as the order makes no difference

  print("Finished")
