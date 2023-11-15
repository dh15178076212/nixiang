## pcap2curl2python

## 第三方模块

```
 pip install scapy
```

## 支持的协议

```
http 协议
请求方式目前只可以用 get, post
```

## 食用教程

### pcap2curl.py

```
根据你的 pacap 文件和 端口号 进行解析,我这里的目标网址端口号就是 443

运行完成后根据生成的 txt 文件去分析
```

###  run_curl.py

```
把 txt 文件中分析好的 curl 放到 该文件中就可以正常使用
```

## 生成的文件是什么含义

```
curl_GET.txt  存放所有的 get 请求的 curl
curl_POST.txt 存放所有的 post 请求的 curl
error.txt     存放所有解析错误的请求
```

![image-20231115114505489](readme.assets\image-20231115114505489.png)

![image-20231115130132116](readme.assets\image-20231115130132116.png)

![image-20231115130444793](readme.assets\image-20231115130444793.png)