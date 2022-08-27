
# Pre-processing

Convert and merge all TIFF files under the `alert/` and `alertDate/` folders to a set of tiles of size 256x256 pixels of the format .npy


## Installation

requirements installation

```batsh
pip install -r requirements.txt
```
    
## Usage

Download both folder alert and alertDate from [Hansen folder](https://console.cloud.google.com/storage/browser/earthenginepartners-hansen/S2alert?pageState=(%22StorageObjectListTable%22:(%22f%22:%22%255B%255D%22))&prefix=&forceOnObjectsSortingFiltering=false) on Google cloud,
then execute the following command.
```batch
python tiff2TWM.py --alert_path alert/ --alertDate_path alertDate/ --max_zoom 15
```

