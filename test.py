from src.utils import load_unit_stats

def main():
    test = load_unit_stats("src/unit_stats.csv")
    print(f"{test['Huma']}")

if __name__ == "__main__":
    main()
