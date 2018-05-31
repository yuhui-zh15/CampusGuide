// pages/share/share.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    photo: "../../images/demo/poster.jpg",
    predict: null,
    description: null,
    longabstract: null,
  },

  getData: function () {
    var that = this
    var result = wx.getStorageSync('result')
    that.setData({
      photo: result.photo,
      predict: result.predict,
      description: result.description,
      longabstract: result.longabstract,
    })
  },

  getRandomInt: function (max) {
    return Math.floor(Math.random() * Math.floor(max));
  },

  downloadImg: function () {
    var that = this
    wx.saveImageToPhotosAlbum({
      filePath: that.data.photo,
      success: function (res) {
        console.log(res)
      },
      fail: function (res) {
        console.log(res)
        console.log('fail')
      }
    })
  },

  refreshImg: function () {
    var that = this
    var openid = wx.getStorageSync('openid')
    var option = that.getRandomInt(2)

    wx.downloadFile({
      url: "http://166.111.5.246:8080/share?" + "openid=" + openid + "&option=" + option,
      success: function (res) {
        console.log('downloadFile success, res is', res)
        that.setData({
          photo: res.tempFilePath
        })
      },
      fail: function ({ errMsg }) {
        console.log('downloadFile fail, err is:', errMsg)
      }
    })
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    // this.getData()
    this.refreshImg()
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {
  
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
  
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {
  
  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {
  
  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {
  
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {
  
  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {
  
  }
})