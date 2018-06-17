// pages/spot/spot.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    photo: "../../images/demo/shuimuqinghua.jpg",
    predict: "水木清华",
    description: "景昃鸣禽集，水木湛清华",
    longabstract: "水木清华是北京清华园中最著名的景点，位于清华大学工字厅的北侧。清华园的名字即来源于此，被称作清华园“园中之园”。水木清华的主体景观是工字厅后面的一个荷塘，荷塘之畔垂杨山水之中掩映着一幢秀雅的古建筑，常与颐和园中的谐趣园相比。"
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
    this.getData()
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