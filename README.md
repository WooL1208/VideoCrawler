# 素材網站影片爬蟲機器人

此工具會至pexels網站下載影片，未來會新增多素材網站爬蟲的功能

此工具為了搜集影片資料集而開發

## Usage

```shell
python main.py --video --search {keywords}
```

## Installation

```shell
git clone https://github.com/WooL1208/VideoCrawler.git
```

## How to Use

1. 安裝必要套件
2. 使用args操作此程式

以下為必要套件：

> 注意：本軟體需運行在python 3.10以上的版本

```shell
pip install tqdm argparse requests selenium fake_useragent
```

args介紹：

1. 選擇是否要下載影片：

   ```shell
    python main.py --video --search {keywords}
    ```

2. 選擇是否要下載敘述：

    ```shell
    python main.py --script --search {keywords}
    ```

3. 選擇是否隱藏瀏覽器畫面

    ```shell
    python main.py --headless --video --search {keywords}
    ```

4. 選擇要搜尋的網站（尚未實裝）

   ```shell
    python main.py --video --engine {numbering} --search {keywords}
    ```

## File Explanation

| 檔案名稱 | 敘述  |
|  ----  |  ----  |
| main.py | 主要執行程式 |
| crawler_action.py | 執行爬蟲之動作 |
| crawler_method.py | 執行中所需之方法 |
| toolbox.txt | 開發過程中遭到棄用的方法 |

## License

MIT
