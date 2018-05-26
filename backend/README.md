# Backend

## Files

```
test/
    init.py: Generate *.npy from images (of standard size), 
             must be executed before training if the images are changed.
    main.py: Test the model and generate a markdown.

webapi/
    model_wrapper.py: A wrapper for the model.
             Accepts an OpenCV-format image (channels: BGR, not RGB) of *Any* size.
    main.py: An ad-hoc api for wechat frontend, see webapi/README.md for usage.

init.py: Generate *.npy from images (of standard size), 
             must be executed before training if the images are changed.
             NOTE: The inputs to this script is (and should be) different from test/init.py.
model.py: Builds the model architecture.
utils.py: Global variables, data loader, configs, etc.
main.py: Trains the model.
```

## Usage

See `main.py`s for comments on usage.

