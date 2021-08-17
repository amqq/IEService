# Image Editing Service #

IEService is lightweight image editing service like [Thumbor](https://github.com/thumbor/thumbor).
IEService is very small , useful and easy to use,

## Installation ##

At First install python 3.7+ on your os then install pillow ,Socket with pip and following codes:

- `pip install pillow` 
- `pip install socket`

After that get IEService with git
- git `git clone https://github.com/alexbers/mtprotoproxy.git`

## Run IEService ##

you can run IEService after installation by 

- `cd <IEService folder path>`
- `python3 IEService.py`

## Configuration ##

After you run IEService When Debug_Mode is False, IEService let you to configure them with some inputs

## Usage ##

IEService Just work with url Api there are type of IEService url Api

- Minimum API :

`http://<YOUR_DOMAIN>:5001/?a=r&w=<IMAGE_WEIGHT>&p=<IMAGE_PATH+IMAGE_NAME>`

- Maximum api :

`http://<YOUR_DOMAIN>:5001/?action=resize&weight=<IMAGE_WEIGHT>&height=<IMAGE_HIGHT>&format=<jpeg OR webp OR png>&path=<IMAGE_PATH+IMAGE_NAME>`

## API Parameter ##

- ### Api Require Parameter ###
  - `action` or `a` => Action name to do
  - `path` or `p` => path of image
  - `weight` or `w` => weight of response image

- ### Api Optional Parameter ###
  - `height` or `h` => height of response image
  - `format` or `f` => format of response image (jpeg,png,webp)
  - `quality` or `q` => quality of response image (1 to 99)

