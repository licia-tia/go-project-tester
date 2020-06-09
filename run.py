import benchmark
with open("commits") as f:
    for line in f:
        before, after = line.split()
        benchmark.main(before, after)