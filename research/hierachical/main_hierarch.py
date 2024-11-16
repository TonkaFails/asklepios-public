import hierarch_bert
import pickle
import os
import time


def main(folder_name):
    hierarch_bert.generate_embeddings(folder_name)

if __name__ == "__main__":
    start = time.time()
    folder_name = 'leitlinien'
    main(folder_name)
    end = time.time()
    print(f"{end-start} seconds")

