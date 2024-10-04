import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
import os
import re
import requests
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("--input", help="Name of the input file (relative)")
parser.add_argument("--output", help="Output directory name (relative)")
parser.add_argument(
    "--pool_size", type=int,
    help="Number of parallel requests (and disk writes)")
args = parser.parse_args()

links = []
with open(args.input, "r", encoding='cp1252') as fp:
    tsv_file = csv.reader(fp, delimiter="\t")
    for line in tsv_file:
        links.append(re.sub(
            "/html/",
            "/art/",
            re.sub(".html$", ".jpg", line[6]
        )))
links = links[1:]

def download(idx: int, link: str) -> None:
    response = requests.get(link)
    with open(os.path.join(args.output, f"{idx}.jpg"), "wb") as fp:
        fp.write(response.content)

os.makedirs(args.output, exist_ok=True)
with ThreadPoolExecutor(args.pool_size) as executor:
    futures = []
    for i, link in enumerate(links):
        futures.append(executor.submit(download, i, link))
    i = 0
    for f in tqdm(as_completed(futures), total=len(futures)):
        pass
