import sys, requests, asyncio
from crawl import crawl_site_async

async def main() -> None:
    args = sys.argv

    if len(args) < 2:
        print("no website provided") 
        sys.exit(1)
    elif len(args) > 2:
        print("too many arguments provided")
        sys.exit(1)
    else:
        print(f"Starting crawl of: {args[1]}")
        base_url = args[1]

    data = await crawl_site_async(base_url)

    for page in data.values():
        print(f'Located {len(page["outgoing_links"])} outgoing links on {page["url"]}')

    sys.exit(0)



if __name__ == "__main__":
    asyncio.run(main())
