import random, subprocess, time

def wait_and_remove_first_completed(processes, wait=1, timeout=7200):           # Wait for the first process in the specified array to complete and remove it from that array
  for _, p in [[t, p] for t in range(int(timeout / wait)) for p in processes]:  # Cartesian product of waits and processes
    if p.poll() is not None: processes.remove(p); return                        # Remove first process to complete
    if (p == processes[-1]): time.sleep(wait)                                   # Wait after each set of processes to give a process a chance to finish
  raise RuntimeError(f"No process finished within the timeout: {timeout}s.")    # No processes completed in the time out period so something has probably gone wrong

if __name__ == "__main__":                                                      # Tests
  S = []                                                                        # Processes currently being run
  N = 40                                                                        # Total number of jobs to run
  P = 10                                                                        # Number of processes to run concurrently in parallel
  D =  2                                                                        # Dispersion of wait times in each job

  print(f"Run {N} jobs through {P} processes v1\nAction  Run  Load")            # The title of the piece

  for i in range(N):                                                            # Start each job
    print(f"Start {i+1:5d} {len(S):5d}")                                        # Jobs started and number of processes running
    if len(S) >= P: wait_and_remove_first_completed(S)                          # Wait for a process to complete if the working set is full before starting the next job
    S.append(subprocess.Popen(["sleep", f"{random.randint(D, 2* D)}"]))         # Start a process that does a random amount of sleeping as work

  while S: print(f"Wait {len(S):12d}"); S.pop().wait()                          # Wait for remaining processes to complete. Wait in the most convenient order as the actual order makes no difference

  print("Finished")
