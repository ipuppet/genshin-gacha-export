genshin-gacha-export

> source: [sunfkny/genshin-gacha-export](https://github.com/sunfkny/genshin-gacha-export)

## Usage

`python main.py`

## Config

Path: `config/config.json`

```json
{
    "auto_archive": true,
    "export_html": true,
    "export_uigf_json": true,
    "export_xlsx": true,
    "url": ""
}
```

| Name             | Description                                                                                    | Type   | Default |
| :--------------- | :--------------------------------------------------------------------------------------------- | :----- | :------ |
| auto_archive     | Automatic archiving of old data to `archive`                                                   | bool   | true    |
| export_html      | Export HTML Report                                                                             | bool   | true    |
| export_xlsx      | Export [UIGF.W](https://github.com/DGP-Studio/Snap.Genshin/wiki/StandardFormat) Excel Workbook | bool   | true    |
| export_uigf_json | Export [UIGF.J](https://github.com/DGP-Studio/Snap.Genshin/wiki/StandardFormat) JSON           | bool   | true    |
| url              | getGachaLog url                                                                                | string |         |
