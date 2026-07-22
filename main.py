import sys

def main():
    args = sys.argv

    if len(args) < 2:
        print("no website provided") 
        sys.exit(1)
    elif len(args) > 2:
        print("too many arguments provided")
        sys.exit(1)
    else:
        print(f"starting crawl of: {args[1]}")

if __name__ == "__main__":
    main()
