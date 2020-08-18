# FGO-Automata 中文版README

注：这是我个人修改调整后的版本，基于Meowcolm024的原版但已经和原版不是同一回事了，README也砍了不少的
如果要体验完整版请点击 [这里](https://github.com/Meowcolm024/FGO-Automata)

注：这版本的README仅包括安装和配置。

**关于展示视频和安装/脚本编写教程可以参考 [Wiki](https://github.com/Meowcolm024/FGO-Automata/wiki)**

## 安装

需要的外部应用： *ADB*（已经带上不需要额外下）。 需要的Python Package： *PIL*, *OpenCV* 和 *numpy*

1. Clone 这个 repo: ```git clone https://github.com/Meowcolm024/FGO-Automata.git```
2. 安装必要的Python包: ```pip install -r requirements.txt```

## 设定

请学习python或者照例子改。例子是指gouliang.py以及qp.py

## 注意事项

1. 需要**关闭**技能确认。
2. 建议缩短敌人消失时间和使用二倍速
4. 分辨率为`1920x1080`，其余的分辨率这边没考虑支持了。

## FGO-Automata Script

请参见Wiki中[Automata Script](https://github.com/Meowcolm024/FGO-Automata/wiki/Automata-Script)条目。

## 指南

### 1. 初始化

#### a. 导入Package

```python
from core.Automata import Automata
```

#### b. 建立 Class

```python
bb = Automata("assets/Ember4.png", "assets/wucan.png")
```

* 第一个参数为指向**关卡**模板图片的**路径**，第二个参数为指向**助战**模板图片的**路径**。

#### c. AP相关（可选）

```python
bb.set_apples(0, "assets/gold.png")
```

* 您可以不设置此项，则默认不会使用金苹果。
* 参函数接受两个参数，第一个为苹果的数量，第二个为苹果（包括石头）模板图片的路径（也就是选择补充AP的物品）。

### 2. 开始战斗

#### 1. 快速开始

```python
bb.quick_start()
```

- 使用这个语句开始战斗
- **注意**：如果不使用`quick_start()`，需要分别设置下面三个命令

#### 2. 重新设定关卡（可选）

```python
bb.select_checkpoint("assets/checkpoint2.png") # the argument is optional
```

- 参数为模板图片路径

#### 3. 使用进阶助战选择（可选）

```python
rin.advance_support()  # w/o any param
ryougi.advance_support(tms=5)  # update time only
shiki.advance_support(spt="assets/sp3.png", tms=1)
```

- `spt`是模板图片路径（可选），`tms`是助战列表刷新次数（可选）

#### 4. 开始战斗（可选）

```python
shiki.start_battle()
```

### 3. 战斗中

#### 1. 选择指令卡

```python
bb.select_cards([7])
```

```python
bb.select_cards([1,2,3])
```

- 需要提供一个最多3个元素的数组，数字*1～5*为从左到右的五张普通指令卡，*6～8*为从左到右的3张宝具卡。您也可以不选满，这样剩下的卡会随机补充。

#### 2. 选择从者技能

```python
# skill w/o target
bb.select_servant_skill(4)
```

```python
# with target Servant
bb.select_servant_skill(2, 3)
```

- 对于没有目标从者的技能（如“直死之魔眼”）传入一个参数。即*1～9*，从左往右数。
- 对于有目标从者的技能（如“初始的卢恩”）需要提供两个参数，第一个同上，第二个为目标从者（*1～3*，从左到右对应的从者）

#### 3. 选择御主技能

```python
# skill w/o target
bb.select_master_skill(2)
```

```python
# with target Servant
bb.select_master_skill(1, 3)
```

```python
# Order Change
bb.select_master_skill(3, 1, 1)
```

- 大体上同从者技能。*1～3*为从左往右数的三个御主技能。
- 可选的第二个参数为目标从者。
- 对于换人服的换人技能，需要提供三个参数。第一个为技能代号应该是第3个。第二个为先发从者代号（1～3），第三个为支援从者代号（1～3）。

### 4. 结束战斗

```python
# finish
bb.finish_battle()
```

## 自动战斗（这个没管，请稳定3t）


## 制作模板图片

以下是模板图片的两个例子：

![checkpoint](assets/Qp4.png)

- 关卡模板图片

![support](assets/wucan.png)

- 助战模板图片

> 关于助战的模板图片，可以考虑先用游戏中的礼装过滤，再使用从者头像作为助战的模板图片。
