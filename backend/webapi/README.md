# webapi

This is a web-api to wrap the model (tailored to the wechat frontend). 

url: http://166.111.5.246:8080/upload

## Start the Server

```bash
(backend)$ CUDA_VISIBLE_DEVICES=[gpu_id] python -m webapi.main
```

## NOTES

1. If the model is retrained, please modify `model_path` in `model_wrapper.py`;
2. Raw pictures are cropped using OpenCV. The logic is:
    - Scaling:
        1. If either `width` or `height` is less than desired, scale-up the image;
        2. Else they are both greater-than-or-equal-to desired, scale-down the image;
    - Cropping:
        1. Crop a rectangle of desired size in the center.

## Wechat Frontend

Code to select and send an image from wechat frontend to this api:

```javascript
// index.js

/** 
 * 选择照片 
 */
chooseImg: function () {
  var that = this
  wx.chooseImage({
    count: 1, // 默认9  
    sizeType: ['original', 'compressed'], // 可以指定是原图还是压缩图，默认二者都有  
    sourceType: ['album', 'camera'], // 可以指定来源是相册还是相机，默认二者都有  
    success: function (res) {
      // 返回选定照片的本地文件路径列表，tempFilePath可以作为img标签的src属性显示图片  
      var tempFilePaths = res.tempFilePaths
      that.setData({
        photos: tempFilePaths
      })
      console.log('上传图片:' + that.data.photos)
    }
  })
}

/** 
 * 上传照片 
 */
uploadImg: function () {
  var filePath = this.data.photos[0]
  console.log(filePath)
  wx.getImageInfo({
    src: filePath,
    success: function (res) {
      console.log('准备上传...')
      wx.uploadFile({
        url: 'http://166.111.5.246:8080/upload', //接口地址
        filePath: filePath,//文件路径
        name: 'file',//文件名，不要修改，Flask直接读取
        formData: {
          'user': 'test'
        }, // 其他表单数据，如地理位置、标题、内容介绍等
        success: function (res) {
          var data = res.data
          console.log('上传成功...')
        }
      })        
    }
  })  
}
```
