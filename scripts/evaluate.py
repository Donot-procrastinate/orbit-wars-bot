from kaggle_environments import make


def main():
    env = make("orbit_wars", debug=True)

    env.run([
        "agents/noop_agent.py",
        "agents/noop_agent.py",
    ])

    html = env.render(mode="html")

    with open("replays/noop_vs_noop.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("Replay saved to replays/noop_vs_noop.html")


if __name__ == "__main__":
    main()