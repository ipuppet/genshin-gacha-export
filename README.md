genshin-gacha-export

> source: [sunfkny/genshin-gacha-export](https://github.com/sunfkny/genshin-gacha-export)

## Usage

`python main.py`

## Config

Path: `config/config.json`

```json
{
    "auto_archive": true,
    "wish_types": [ "100", "200", "301", "302" ],
    "export_html": true,
    "export_uigf_json": true,
    "export_xlsx": true,
    "url": ""
}
```

| Name             | Description                                                                                    | Type   | Default                        |
| :--------------- | :--------------------------------------------------------------------------------------------- | :----- | :----------------------------- |
| auto_archive     | Automatic archiving of old data to `archive`                                                   | bool   | true                           |
| wish_types       | Included wish types                                                                            | array  | `["100", "200", "301", "302"]` |
| export_html      | Export HTML Report                                                                             | bool   | true                           |
| export_xlsx      | Export [UIGF.W](https://github.com/DGP-Studio/Snap.Genshin/wiki/StandardFormat) Excel Workbook | bool   | true                           |
| export_uigf_json | Export [UIGF.J](https://github.com/DGP-Studio/Snap.Genshin/wiki/StandardFormat) JSON           | bool   | true                           |
| url              | getGachaLog url: `https://hk4e-api.mihoyo.com/event/gacha_info/api/getGachaLog?*`              | string |                                |


#### `wish_types` possible values

- "100": 新手祈愿
- "200": 常驻祈愿
- "301": 角色活动祈愿
- "302": 武器活动祈愿

