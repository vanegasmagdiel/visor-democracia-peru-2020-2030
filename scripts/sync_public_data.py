#!/usr/bin/env python3
"""Copy all canonical data into the public GitHub Pages download directory."""
import shutil
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
def main():
    count=0
    for src in (BASE/'data').rglob('*'):
        if src.is_file():
            dst=BASE/'docs/data'/src.relative_to(BASE/'data')
            dst.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(src,dst)
            count+=1
    print(f'SYNCED {count} canonical data products')
if __name__=='__main__':
    main()
