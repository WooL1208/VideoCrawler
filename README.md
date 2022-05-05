# 素材網站影片爬蟲機器人

此工具會至pexels網站下載影片，未來會新增多素材網站爬蟲的功能

此工具為了搜集影片資料集而開發

## Usage

```shell
python main.py --search {keywords}
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
pip install tqdm
pip install argparse
pip install requests
pip install selenium
pip install fake_useragent
```

args介紹：

1. 搜尋關鍵字：

    ```shell
    python main.py --search {keywords}
    ```

2. 選擇是否跳出瀏覽器畫面

    ```shell
    python main.py --headless
    ```

3. 選擇要搜尋的網站（尚未實裝）

   ```shell
    python main.py --engine {numbering}
    ```

## License

MIT