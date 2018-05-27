//app.js
App({

  globalData: {
    appid: "wxad42d342d620277e",
    secret: "96438f6091d7cf552fe884ef1f115f0a",
    userInfo: null
  },

  onLaunch: function () {
    // 展示本地存储能力
    var that = this
    var logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)

    // 登录
    wx.login({
      success: function (res) {
        if (res.code) {
          wx.getUserInfo({
            withCredentials: true,
            success: function (res_user) {
              wx.request({
                //后台接口地址
                url: 'https://api.weixin.qq.com/sns/jscode2session?appid=' + that.globalData.appid + '&secret=' + that.globalData.secret + '&js_code=' + res.code + '&grant_type=authorization_code',
                data: {
                  code: res.code,
                  encryptedData: res_user.encryptedData,
                  iv: res_user.iv
                },
                method: 'GET',
                header: {
                  'content-type': 'application/json'
                },
                success: function (res) {
                  wx.setStorageSync('openId', res.data.openId)
                  console.log('获取用户信息成功：openId:' + res.data.openid)
                }
              })
            }
          })
        }
      }
    })
    // 获取用户信息
    wx.getSetting({
      success: res => {
        if (res.authSetting['scope.userInfo']) {
          // 已经授权，可以直接调用 getUserInfo 获取头像昵称，不会弹框
          wx.getUserInfo({
            success: res => {
              // 可以将 res 发送给后台解码出 unionId
              this.globalData.userInfo = res.userInfo

              // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
              // 所以此处加入 callback 以防止这种情况
              if (this.userInfoReadyCallback) {
                this.userInfoReadyCallback(res)
              }
            }
          })
        }
      }
    })
  }
})