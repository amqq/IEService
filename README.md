# Image Editing Service #

IEService is lightweight image editing service like [Thumbor](https://github.com/thumbor/thumbor).
IEService is very small , useful and easy to use,

## Installation ##

At First install python 3.7+ on your os then install pillow ,Socket with pip and following codes:

- `pip install pillow` 
- `pip install socket`

After that get IEService with git
- git `git clone https://github.com/amqq/IEService.git`

## Run IEService ##

you can run IEService after installation by 

- `cd <IEService folder path>`
- `python3 IEService.py`

## Configuration ##

After you run IEService When Debug_Mode is False, IEService let you to configure them with some inputs

## Usage ##

IEService Just work with url Api there are type of IEService url Api

- Minimum resizer API :

`http://<YOUR_DOMAIN>:5001/?a=r&w=<IMAGE_WEIGHT>&p=<IMAGE_NAME>`

- Maximum resizer api :

`http://<YOUR_DOMAIN>:5001/?action=resize&weight=<IMAGE_WEIGHT>&height=<IMAGE_HIGHT>&quality=<IMAGE_QUALITY>&format=<jpeg OR webp OR png>&path=<IMAGE_NAME>`

- Minimum Image Cropper API :

`http://<YOUR_DOMAIN>:5001/?a=c&l=<IMAGE_LEFT>&t=<IMAGE_TOP>&p=<IMAGE_NAME>`

- Maximum Image Cropper API :

`http://<YOUR_DOMAIN>:5001/?action=crop&left=<IMAGE_LEFT>&right=<IMAGE_RIGHT>&top=<IMAGE_TOP>&bottom=<IMAGE_BOTTOM>&quality=<IMAGE_QUALITY>&format=<jpeg OR webp OR png>&path=<IMAGE_NAME>`

- Minimum Image Crop And Resize API:

`http://<YOUR_DOMAIN>:5001/?a=rc&l=<IMAGE_LEFT>&t=<IMAGE_TOP>&w=<IMAGE_WEIGHT>&p=<IMAGE_NAME>`

- Maximum Image Crop And Resize API :

`http://<YOUR_DOMAIN>:5001/?action=crop&left=<IMAGE_LEFT>&right=<IMAGE_RIGHT>&top=<IMAGE_TOP>&bottom=<IMAGE_BOTTOM>&weight=<IMAGE_WEIGHT>&height=<IMAGE_HIGHT>&quality=<IMAGE_QUALITY>&format=<jpeg OR webp OR png>&path=<IMAGE_NAME>`

## API Parameter ##

- ### Base Required Parameter ###
  - `action` or `a` => Action name to do `required` 
    - can be set (`r` or `resize` to "Resize Image")  (`c` or `crop` to "Crop part of image") (`cr` to "Crop and Resize Image")
  - `path` or `p` => path of image `required`
  - `format` or `f` => format of response image (jpeg,png,webp) `optional`
  - `quality` or `q` => quality of response image (1 to 99) `optional`

- ### Image Resizer API Parameter ###
  - `weight` or `w` => weight of response image `required`
  - `height` or `h` => height of response image `optional` 

- ### Image Cropper API Parameter ###
  - `left` or `l` => left pixels of image to crop `required`
  - `top` or `t` => top pixels of image to crop `required`
  - `right` or `r` => right pixels of image to crop `optional` 
  - `bottom` or `b` => bottom pixels of image to crop `optional` 

- ### Crop And Resize API Parameter ###
  - `weight` or `w` => weight of response image `required`
  - `height` or `h` => height of response image `optional` 
  - `left` or `l` => left pixels of image to crop `required`
  - `top` or `t` => top pixels of image to crop `required`
  - `right` or `r` => right pixels of image to crop `optional` 
  - `bottom` or `b` => bottom pixels of image to crop `optional` 
