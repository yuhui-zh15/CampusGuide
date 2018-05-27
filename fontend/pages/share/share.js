// pages/share/share.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    photo: "",
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

  downloadImg: function () {
    var that = this
    var openid = wx.getStorageSync('openid')
    var option = 1
    console.log("http://166.111.5.246:8080/share?" + "openid=" + openid + "&option=" + option)
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
    this.getData()
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