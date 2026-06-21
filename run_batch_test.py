    #run_batch_test.py

import subprocess
from concurrent.futures import ThreadPoolExecutor

RUNS = 20


def run_once(i):
    result = subprocess.run(
        ["python", "evolution.py"],
        capture_output=True,
        text=True
    )
    return result.stdout


def main():
    results = []

    with ThreadPoolExecutor(max_workers=6) as exe:
        futures = [exe.submit(run_once, i) for i in range(RUNS)]

        for f in futures:
            out = f.result()

            for line in out.split("\n"):
                if "FINAL:" in line:
                    try:
                        val = int(line.split(":")[1].strip())
                        results.append(val)
                    except:
                        pass

    print("\n=== BATCH RESULT ===")
    print("RUNS:", len(results))
    print("AVG:", sum(results) / len(results))
    print("MAX:", max(results))
    print("MIN:", min(results))


if __name__ == "__main__":
    main()