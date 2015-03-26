import sys

def main(filename):
    f = open(filename, mode='rt', encoding='utf-8')
    for li in f:
        sys.stdout.write(li)
    f.close()

if __name__ == '__main__':
    main(sys.argv[1])