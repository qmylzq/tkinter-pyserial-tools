# tkinter-pyserial-tool
serial control tool by Python based on tkinter and pyserial
[Watch the video](https://www.bilibili.com/video/av78238440)
## Project description
This is a Python application,uesd for controlling serial comports
## Advantages
It's like secureCRT,but more friendly for python,When connect serial equipments,run tk_serial.py file,choose correct comport and standard command file like the file command.xlsx,it can write the commandline in command.xlsx into the serial comport automatcally.
It's useful for automatic test.
## overview picture

![tkinter-pyserial-tool overview](https://github.com/qmylzq/tkinter-pyserial-tools/blob/master/%E4%B8%B2%E5%8F%A3%E5%B7%A5%E5%85%B7.png)
## dependences
python 3.7

tkinter(in windows system can import directly but install it first in linux)

pyserial(click the link below and install first both in windows and linux system)
[pyserial-3.4-py2.py3-none-any.whl](https://files.pythonhosted.org/packages/0d/e4/2a744dd9e3be04a0c0907414e2a01a7c88bb3915cbe3c8cc06e209f59c30/pyserial-3.4-py2.py3-none-any.whl)
## instructions
1.connect the serial equipment with PC

2.run tk_serial.py (or use pyinstaller to make one exe file)

3.choose correct comport and baudrate 

4.click the "连接"（connect）button，if succeed，then com_log_text insert"串口成功打开"

5.click the"选择文件"（choose file）button to choose a command excel to conduct,the conmands will show in the middle list of the tk

6.notice that,the command in the command excel need to be in standard format,and the conmand need to be included in the code_dic.py

7.if you have new command to write in ,you need to add the code context in the code_dic.py,if not,there must be wrong 

8.click the "执行"(conduct the conmand)button ,and power your equipment

9.then it will write the command into the serial comports,and the conduct result(ok or failed) will show in the middle list 

10.the result will saved in an auroresult.txt file 

11.just power off one equipment and power another equipment on ,click the "执行"button ,it will run in loop

## on running picture 
![on running picture](https://github.com/qmylzq/tkinter-pyserial-tools/blob/master/%E8%BF%90%E8%A1%8C%E6%88%AA%E9%9D%A2.png)

 
