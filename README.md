# PM25

研究發電廠與PM 2.5濃度之關係

## 目標輸出結果

輸出指定時間範圍內台灣所有核能及火力發電機對應 PM 2.5 濃度之影響程度

| 發電機名稱 | 對 PM 2.5 影響程度(%) |
| --- | --- |
| 核一#1 | 79% |
| 核二#1 | 56 % |

## Part 1. PM 2.5

### Dataset

The whole daatset could be found on the [official site](ftp://gpssensor.ddns.net:2121/).

### Sample Dataset

- <ftp://gpssensor.ddns.net:2121/data.log-20161212.gz>
- <ftp://gpssensor.ddns.net:2121/data.log-20161213.gz>
- <ftp://gpssensor.ddns.net:2121/data.log-20161214.gz>
- <ftp://gpssensor.ddns.net:2121/data.log-20161215.gz>
- <ftp://gpssensor.ddns.net:2121/data.log-20161216.gz>
- <ftp://gpssensor.ddns.net:2121/data.log-20161217.gz>
- <ftp://gpssensor.ddns.net:2121/data.log-20161218.gz>

### Preprocessing

We define the target output format to be `.csv` file with header:

| Field  | Data Type | Description
| --- | --- | --- |
| latitude | Float | - |
| longitude | Float | - |
| pm25 | Float | The concentration of PM2.5 in μg/m<sup>3</sup> |
| timestamp | String | Timestamp with format `YYYY/MM/DD HH:mm`, and the `mm` part can only be `00`, `10`, `20`, `30`, `40` and `50` |

> #### Example
> /data/pm25/csvs/2016-12-20.csv
>
| latitude | longitude | pm25 | timestamp |
| --- | --- | --- | --- |
| 21.5566 | 120.5678 | 71 | 2016/12/25 19:40
| 21.5566 | 120.5678 | 68 | 2016/12/25 19:50

#### Usage

```
/src/pm25 $ python preprocess_LASS.py [../../data/pm25/logs] [../../data/pm25/csvs] [-v]
```

> `-v` switch allows error reporting

1. Turn log files into csv files
2. Drop data when any following rules is matched:
  - Empty data
  - NA, NAN, none data
  - Any data with zero value
  - Error datetime

```
/src/pm25 $ python extractTaiwanCsv.py [../../data/pm25/reducedCsvs]
```

Extract entries near Taiwan.

## Part 2. Power Generator Data

### Dataset

- [台電系統(含外購電力)各機組發電量即時資訊](https://sheethub.com/data.gov.tw/政府資料開放平臺資料集清單/uri/4080)
- [水火力發電廠位置及機組設備](http://data.gov.tw/node/8934)
- [核能發電廠位置及機組設備](http://data.gov.tw/node/10858)

### Collecting

> To Be Documented

### Preprocessing

We manually searched out the longitudes and latitudes of generators and merge them with open data to give [`/data/power/raw.csv`](https://github.com/gocreating/pm25/blob/master/data/power/raw.csv) with following header:

| Field  | Data Type | Description
| --- | --- | --- |
| name | String | The identifier of generators |
| latitude | Float | - |
| longitude | Float | - |
| load | Float | The working load of generators in percentage |
| timestamp | String | Timestamp with format `YYYY/MM/DD HH:mm`, and the `mm` part can only be `00`, `10`, `20`, `30`, `40` and `50` |

## Part 3. Compute

### relayMetrices.py

```
/src/compute $ python relayMetrices.py 10 60
```

Calculate weight param metrices with arguments `r1` and `r2`:

- `/data/relayMetrices/dfR1Pm25Sum.csv`
- `/data/relayMetrices/dfR1WeightSum.csv`
- `/data/relayMetrices/dfR2Pm25Sum.csv`
- `/data/relayMetrices/dfR2WeightSum.csv`

> ### Note
> This step will take several days!

The format of these metrices is like following:

| | 協和#1 | 台中#1 | ... | 星元#1 | 嘉惠#1 |
| --- | --- | --- | --- | --- | --- |
| 2016/12/17 00:00 | -21.65610874 | -21.65610874 | ... | 3.502609225 | 0.704510358 |
| 2016/12/17 00:10 | -18.59080956 | -18.59080956 | ... | 2.18297131 | 0.697338471 |
| ... | ... | ... | ... | ... | ... |
| 2016/12/23 23:40 | -9.457467469 | -9.457467469 | ... | -1.206004589 | 8.70393683 |
| 2016/12/23 23:50 | -9.251565115 | -9.251565115 | ... | -0.77633429 | 10.38556501 |

### populateGeneratorPm25.py

```
/src/compute $ python populateGeneratorPm25.py
```

Remove meaningless power generator and from the above 4 metrices we can calculate weighted pm2.5 concentrations metrix `/data/pm25.csv` for each timestamp and for each power generator.

### Manual Correction

Manually remove the following columns of `/data/pm25.csv`:

- `桂山發電廠`
- `桂山發電廠.1`
- `桂山發電廠.2`
- `桂山發電廠.3`
- `桂山發電廠.4`

### compute.py

```
/src/compute $ python compute.py
```

Output the final result `/data/computed.csv`

## Part 4. Analytics

### Usage

```
/src $ python /src/compute.py
```

## Reference

### LASS

- [LASS - README](https://lass.hackpad.com/LASS-README-DtZ5T6DXLbu)
- [LASS - Data specification](https://lass.hackpad.com/LASS-Data-specification-1dYpwINtH8R)
- [How to get data log from server](https://lass.hackpad.com/How-to-get-data-log-from-server-Ztu9mpUsGL9)
