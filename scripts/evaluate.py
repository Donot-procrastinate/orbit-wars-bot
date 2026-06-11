from kaggle_environments import make


def main():
    env = make("orbit_wars", configuration={"seed": 42}, debug=True)

    env.run([
        "agents/heuristic_v1.py",
        "random",
    ])

    final = env.steps[-1]
    for i, s in enumerate(final):
        print(f"Player {i}: reward={s.reward}, status={s.status}")

    # Render in a notebook
    html = env.render(mode="html")

    with open("replays/heuristic_v1_vs_random.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("Replay saved to replays/heuristic_v1_vs_random.html")


if __name__ == "__main__":
    main()