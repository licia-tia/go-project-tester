#!/usr/bin/python3

import os
import base64


ng_words = []
must_words = []


def init(commit):
    os.system('git reset --hard ' + commit)
    os.system('go get ./...')
    # os.system('dep init')
    # os.system('dep ensure')
    # os.system('go get -d -v ./...')


def test(cmd, path):
    for i in ng_words:
        if i in cmd:
            return
    if len(must_words) != 0:
        for i in must_words:
            if i in cmd:
                print("Now testing " + path)
                os.system(cmd)
                break
        return
    print("Now testing " + path)
    os.system(cmd)


def main(before, after):
    os.system('mkdir results')
    os.system('rm ./results/*')
    os.system('mkdir ./results/before')
    os.system('mkdir ./results/after')
    init(before)
    list_dirs = os.walk('.')
    for root, dirs, files in list_dirs:
        for d in dirs:
            path = os.path.join(root, d)
            cmd = "go test {0} -timeout 3s -count=1 -test.bench=. -cpuprofile ./results/before/{1}_cpu.out -memprofile ./results/before/{1}_mem.out > ./results/before/{1}_std.out".format(
                path, base64.urlsafe_b64encode(bytes(path, 'UTF-8')))
            test(cmd, path)

    init(after)
    list_dirs = os.walk('.')
    for root, dirs, files in list_dirs:
        for d in dirs:
            path = os.path.join(root, d)
            cmd = "go test {0} -timeout 3s -count=1 -test.bench=. -cpuprofile ./results/after/{1}_cpu.out -memprofile ./results/after/{1}_mem.out > ./results/after/{1}_std.out".format(
                path, base64.urlsafe_b64encode(bytes(path, 'UTF-8')))
            test(cmd, path)

    os.system('tar cvf ' + after + '.tar ./results/*')
    os.system('mv ' + after + '.tar /gogogo/')


if __name__ == "__main__":
    before = 'a4f24690a48567d0cbfad2f1b767d786bc53c393'
    after = '92635fa6bffd9db9b2cca8ce8f978bfebabd9c29'
    main(before, after)
