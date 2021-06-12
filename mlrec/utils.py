from tabulate import tabulate


def display_statistics(stats: dict, tablefmt="simple", floatfmt=".4f"):
    keys = []
    values = []

    for k, v in stats.items():
        if k.startswith("_"):
            continue
        keys.append(k)
        values.append(v)

    print(
        tabulate(
            list(zip(keys, values)),
            ["keys", "statistics"],
            tablefmt=tablefmt,
            floatfmt=floatfmt,
        )
    )
    print()
