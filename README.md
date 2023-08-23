# nuoyanLib

---
 
> 目前该项目仍处于测试阶段，部分功能仍未开发或存在较多bug。

<br></br>

## 介绍

---

我的世界中国版ModSDK开发函数库，整合了众多开发中常用的算法，~~封装了部分常用的官方接口~~。  
目前该项目仅由 _**诺言Nuoyan**_ 一人开发，所有代码均为原创（有标注的除外）。  
该项目可供大家学习参考，也可以直接应用于您个人/团队的项目中，希望nuoyanLib能提高大家的代码编写效率以及更轻松地实现复杂的效果！  
感谢大家支持作者、支持该项目，喜欢的话可以点个Star噢，您的支持是作者最大的动力！

<br></br>

## 功能一览

---

- [**client（客户端函数库）**](/nuoyanLib/client)  

  > 包含clientcomp、clientTimer、effector、nuoyanClientSystem、player、setting、sound模块。

  提供了客户端扩展等实用功能。


- [**client.ui（UI库）**](/nuoyanLib/client/ui)  

  > 包含animator、itemFlyAnim、itemGridManager、itemTipsBox、nuoyanScreenNode、utils模块。

  提供了ScreenNode扩展、物品网格管理器等实用工具。


- [**server（服务端函数库）**](/nuoyanLib/server)  

  > 包含entity、globalPlayerManager、hurt、inv、nuoyanServerSystem、servercomp、serverTimer、structure模块。

  涵盖了服务端扩展、实体获取、实体操作、范围伤害、背包管理等各种功能。


- [**utils（通用工具库）**](/nuoyanLib/utils)  

  > 包含calculator、enum、error、item、mcRandom、utils、vector模块。

  提供了多种数学计算函数、更多的枚举值等实用工具。

<br></br>

## 使用说明

---

1. 点击页面上方“克隆/下载”按钮，下载ZIP；
2. 解压文件，将“nuoyanLib”文件夹放至您的scripts文件夹内；
3. 打开nuoyanLib/_config.py文件，将您的模组名称、客户端系统名称和服务端系统名称填入对应位置即可。  
    > 请确保填入_config.py的信息与您的模组对应，否则部分功能将无法使用。

<br></br>

## 参考文档

---

https://gitee.com/charming-lee/nuoyanLib/tree/master/%E5%8F%82%E8%80%83%E6%96%87%E6%A1%A3

<br></br>

## 贡献

---

本项目欢迎各位开发者共同参与开发，如果您有更好的算法或修改建议，可通过Pull Request或Issue的方式提交，成为本项目的贡献者。
> 具体方法请自行搜索git和gitee相关教程。

<br></br>

## 未来计划

---

1. 封装常用官方接口；
2. 完成服务端引擎事件的自动监听；
3. 增加更多实用功能；
4. 重新整理函数文档注释，完成参考文档的编写；
5. 优化代码；
6. 编写demo；
7. ...

<br></br>

## 版权说明

---

本项目遵循《木兰宽松许可证第2版》，您可以将nuoyanLib应用于任何商业/非商业项目中，允许修改其中的内容，但请保留nuoyanLib中每个文件头部的版权注释。
> 更多内容请自行查阅[LICENSE](/LICENSE)文件。

<br></br>

## 联系作者

---

如果在使用过程中遇到问题，可通过以下方式联系作者：
- QQ：1279735247
- 邮箱：1279735247@qq.com

<br></br>