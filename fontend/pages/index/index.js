// index.js  
Page({

  /** 
   * 页面的初始数据 
   */
  data: {
    photos: ""
  },
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
  },
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
  },

  /**
   * 用于调试
   */
  debug: function() {
    wx.request({
      url: 'http://166.111.5.246:8080/upload',
      data: this.data.photos[0],
      method: 'POST',
      header: { 'content-type': 'application/x-www-form-urlencoded' },
      success: function (res) {
        console.log('submit success');
      },
      fail: function (res) {
        console.log('submit fail');
      },
      complete: function (res) {
        console.log('submit complete');
      }
    })  
  }
})  