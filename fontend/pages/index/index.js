// index.js  
Page({

  /** 
   * 页面的初始数据 
   */
  data: {
    photos: "",
    latitude: 0, //纬度 
    longitude: 0 //经度 
  },

  /** 
  * 上传照片 
  */
  uploadImg: function () {
    var that = this;
    var filePath = that.data.photos[0]
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
            wx.switchTab({url: '../spot/spot'})
            var result = {
              'photo': filePath,
              'predict': data,
              'description': '景昃鸣禽集，水木湛清华', // [TODO] 每个景物的标语
              'standard': null // [TODO] 标准模板图片
            }
            wx.setStorageSync('result', result)
            console.log('上传成功...' + data)
          }
        })
      }
    })
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
        that.uploadImg()
        console.log('上传图片:' + that.data.photos)
      }
    })
  },

  getLocation: function() {
    var that = this;
    wx.getLocation({
      type: 'gcj02', //返回可以用于wx.openLocation的经纬度
      success: function (res) {
        var latitude = res.latitude
        var longitude = res.longitude
        that.setData({
          latitude: latitude, //纬度 
          longitude: longitude, //经度 
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
  },

  onLoad: function (options) {
    this.getLocation()
  }
})  