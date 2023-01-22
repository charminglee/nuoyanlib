# nuoyanLib

## 介绍

我的世界中国版ModSDK开发函数库，整合了众多开发中常用的算法，封装了部分常用的官方接口。  
目前该项目仅由 _**诺言Nuoyan**_ 一人开发，所有代码均为原创（有标注的除外）。  
该项目可供大家学习参考，当然也可以应用于您个人/团队的项目中，希望nuoyanLib能提高大家的代码编写效率以及更轻松地实现复杂的效果！  
感谢大家支持作者、支持该项目，喜欢的话可以点个Star噢，您的支持是作者最大的动力！  
> 项目地址：https://gitee.com/charming-lee/nuoyanLib

## 功能一览

- [**base（基础库）**](/nuoyanLib/basic)  
    > 包含clientcomp、servercomp、nuoyanClientSystem、nuoyanServerSystem、nuoyanScreenNode模块。  

    减少了客户端和服务端创建组件（Component）的需要编写的繁琐的代码，并为客户端（ClientSystem）、服务端（ServerSystem）及UI类（ScreenNode）提供了功能扩展。


- [**client（客户端函数库）**](/nuoyanLib/client)  
    > 包含animator、effector、player、setting、sound、ui模块。

    为自定义UI控件动画、更好的序列帧/粒子特效管理等提供了解决方案。


- [**server（服务端函数库）**](/nuoyanLib/server)  
    > 包含entity、globalPlayerManager、hurt、inv模块。

    涵盖了实体获取、实体操作、全局玩家管理、范围伤害、背包管理等各种功能。


- [**util（实用工具库）**](/nuoyanLib/util)  
  > 包含calculator、enum、error、item、test、util、vector模块。

  提供了多种数学计算函数、更多的枚举值、错误报告管理等实用工具。


- [**mctypes（MC类型注解库）**](/nuoyanLib/mctypes)  
  没有实际功能，来源于官方ModSDK补全库文件，包含ModSDK中的所有类型（如BaseUIControl、BookManager、ServerSystem等），主要用于类型注解，让IDE帮助您检查代码中可能出现的类型错误。


- [**gametick**](/gametick)  
  主要用于实现超过30帧的tick事件。[查看详细介绍](/gametick/README.md)



## 使用说明

1. 点击页面上方“克隆/下载”按钮，或在右侧发行版处选择一个版本下载；
2. 解压后将“nuoyanLib”文件夹放至行为包脚本根目录（即scripts文件夹）下；
3. 打开nuoyanLib/_config.py文件，将您的模组名称、客户端系统名称和服务端系统名称填入对应位置即可。  
    > 请确保填入_config.py的信息与您的模组对应，否则部分功能将无法使用。

## 相关文档

- 参考文档：https://gitee.com/charming-lee/nuoyanLib/wikis/%E5%8F%82%E8%80%83%E6%96%87%E6%A1%A3/base%EF%BC%9A%E5%9F%BA%E7%A1%80%E5%BA%93  
- 技术文档：

## 贡献

- 本项目欢迎全体开发者共同参与开发，如果您有好的算法或修改建议，可将您修改后的项目文件进行推送或直接进行在线编辑，成为本项目的贡献者。
- 如果您对本项目有任何意见或建议，比如想要新增什么功能，欢迎在[Issues](https://gitee.com/charming-lee/nuoyanLib/issues)提出。
> 具体方法请自行搜索gitee和git相关教程。

## 未来计划

1. 封装常用官方接口；
2. 完成服务端引擎事件的自动监听；
3. 增加更多实用功能；
4. 重新整理函数文档注释；
5. 优化代码；
6. ...

## 版权说明

nuoyanLib遵循《木兰宽松许可证第2版》，您可以将nuoyanLib应用于任何项目中，修改与否由您决定，但请保留nuoyanLib中每个文件头部的版权注释。
> 更多内容请自行查阅[LICENSE](/LICENSE)文件。

## 联系作者

如在使用过程中遇到问题，可通过以下方式联系作者：  
- QQ：1279735247
- 邮箱：1279735247@qq.com
- gitee：https://gitee.com/charming-lee

## 更新信息

【2023.02.xx】版本：v1.0.0 正式发布