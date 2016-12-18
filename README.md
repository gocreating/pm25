# PM25

研究發電廠與PM 2.5濃度之關係

## 目標輸出結果

| 發電機編號 | 對 PM 2.5 影響程度(%) |
| --- | --- |
| 核一#1 | 79% |
| 核二#1 | 56 % |

## Part 1. PM 2.5

### Dataset

The whole daatset could be found on the [official site](ftp://gpssensor.ddns.net:2121/)

### Sample Dataset

- <ftp://gpssensor.ddns.net:2121/data.log-20161212.gz>
- <ftp://gpssensor.ddns.net:2121/data.log-20161213.gz>
- <ftp://gpssensor.ddns.net:2121/data.log-20161214.gz>
- <ftp://gpssensor.ddns.net:2121/data.log-20161215.gz>
- <ftp://gpssensor.ddns.net:2121/data.log-20161216.gz>
- <ftp://gpssensor.ddns.net:2121/data.log-20161217.gz>

### Preprocessing

We define the target output format to be `.csv` file with header:

| Field  | Data Type | Description
| --- | --- | --- |
| longitude | Float | - |
| latitude | Float | - |
| pm25 | Float | The concentration of PM2.5 in μg/m<sup>3</sup> |
| timestamp | String | Timestamp with format `YYYY/MM/DD HH:mm`, and the `mm` part can only be `10`, `20`, `30`, `40` and `50` |

> #### example.csv
| longitude  | latitude | pm25 | timestamp |
| --- | --- | --- | --- |
| 120.5678 | 21.5566 | 71 | 2016/12/25 19:40
| 120.5678 | 21.5566 | 68 | 2016/12/25 19:50

## Part 2. Power Generator Data

### Dataset

- [台電系統(含外購電力)各機組發電量即時資訊](https://sheethub.com/data.gov.tw/政府資料開放平臺資料集清單/uri/4080)
- [水火力發電廠位置及機組設備](http://data.gov.tw/node/8934)
- [核能發電廠位置及機組設備](http://data.gov.tw/node/10858)

### Preprocessing

## Reference

### LASS

- [LASS - README](https://lass.hackpad.com/LASS-README-DtZ5T6DXLbu)
- [LASS - Data specification](https://lass.hackpad.com/LASS-Data-specification-1dYpwINtH8R)
- [How to get data log from server](https://lass.hackpad.com/How-to-get-data-log-from-server-Ztu9mpUsGL9)
