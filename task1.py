import os
import shutil
import argparse
from concurrent.futures import ThreadPoolExecutor


def copy_file(src_file, dest_dir):
    shutil.copy(src_file, dest_dir)


def process_directory(source_dir, dest_dir):
    for root, dirs, files in os.walk(source_dir):
        for filename in files:
            src_file = os.path.join(root, filename)
            extension = os.path.splitext(filename)[1][1:]
            dest_subdir = os.path.join(dest_dir, extension)
            os.makedirs(dest_subdir, exist_ok=True)
            dest_file = os.path.join(dest_subdir, filename)
            copy_file(src_file, dest_subdir)


def main():
    parser = argparse.ArgumentParser(description='Process files in directory')
    parser.add_argument('source_dir', help='Path to the source directory')
    parser.add_argument('dest_dir', nargs='?', default='dist',
                        help='Path to the destination directory (default: dist)')
    args = parser.parse_args()

    source_dir = args.source_dir
    dest_dir = args.dest_dir

    os.makedirs(dest_dir, exist_ok=True)

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        for root, dirs, files in os.walk(source_dir):
            for directory in dirs:
                src_dir = os.path.join(root, directory)
                dest_subdir = os.path.join(
                    dest_dir, os.path.relpath(src_dir, source_dir))
                os.makedirs(dest_subdir, exist_ok=True)
                futures.append(executor.submit(
                    process_directory, src_dir, dest_subdir))

        for future in futures:
            future.result()

    print("Copying files completed.")


if __name__ == "__main__":
    main()
