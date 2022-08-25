# requestinspector
A tool to use interactsh from python for automating OOB things

# Usage

```python
>>> from sources.interactsh import Interactsh
>>> with Interactsh() as handle
>>>     a.get_handle()
'http://7p6124c7562v4035s95y8k5p085073fhs.interact.sh/'
>>> import requests
>>>     requests.get(a.get_handle())
>>>     a.poll()
[{'timestamp': '2022-06-09T12:32:38.387891517Z', 'host': '7p6124c7562v4035s95y8k5p085073fhs.7p6124c7562v4035s95y8k5p085073fhs.interact.sh', 'remote_address': 'xxx', 'raw-request': ';; opcode: QUERY, status: NOERROR, id: 32453\n;; flags: cd; QUERY: 1, ANSWER: 0, AUTHORITY: 0, ADDITIONAL: 1\n\n;; OPT PSEUDOSECTION:\n; EDNS: version 0; flags: do; udp: 512\n\n;; QUESTION SECTION:\n;7p6124c7562v4035s95y8k5p085073fhs.interact.sh.\tIN\t AAAA\n', 'protocol': 'dns'}, {'timestamp': '2022-06-09T12:32:38.410108026Z', 'host': '7p6124c7562v4035s95y8k5p085073fhs.7p6124c7562v4035s95y8k5p085073fhs.interact.sh', 'remote_address': 'xxxx', 'raw-request': ';; opcode: QUERY, status: NOERROR, id: 34065\n;; flags: cd; QUERY: 1, ANSWER: 0, AUTHORITY: 0, ADDITIONAL: 1\n\n;; OPT PSEUDOSECTION:\n; EDNS: version 0; flags: do; udp: 512\n\n;; QUESTION SECTION:\n;7p6124c7562v4035s95y8k5p085073fhs.interact.sh.\tIN\t AAAA\n', 'protocol': 'dns'}, {'timestamp': '2022-06-09T12:32:38.429969193Z', 'host': '7p6124c7562v4035s95y8k5p085073fhs.7p6124c7562v4035s95y8k5p085073fhs.interact.sh', 'remote_address': 'xxxxx', 'raw-request': .........
```

By using the context manager, the handle is automatically deregistered once the context is ended.