// index.js  
var amapFile = require('../../libs/amap-wx.js')
Page({

  /** 
   * 页面的初始数据 
   */
  data: {
    photos: "",
    latitude: 0, //纬度 
    longitude: 0, //经度 
    key: '289a795ce3b19b70cefa8a924b338b83',
    show: false,
    currentLo: null,
    currentLa: null,
    newCurrentLo: null,
    newCurrentLa: null,
    distance: 0,
    duration: 0,
    markers: null,
    scale: 16,
    polyline: null,
    statusType: 'car',
    includePoints: []
  },

  /** 
  * 上传照片 
  */
  uploadImg: function () {
    var that = this;
    var filePath = that.data.photos[0]
    console.log(filePath)
    var openid = wx.getStorageSync('openid')
    console.log('in index.js: openid:' + openid)
    wx.getImageInfo({
      src: filePath,
      success: function (res) {
        console.log('准备上传...')
        wx.uploadFile({
          url: 'http://166.111.5.246:8080/upload', //接口地址
          filePath: filePath,//文件路径
          name: 'file',//文件名，不要修改，Flask直接读取
          formData: {
            'user': 'test',
            'openid': openid
          }, // 其他表单数据，如地理位置、标题、内容介绍等
          success: function (res) {
            var data = JSON.parse(res.data)
            wx.switchTab({url: '../spot/spot'})
            var result = {
              'photo': filePath,
              'predict': data.predicted,
              'description': data.description,
              'longabstract': data.longabstract,
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
          currentLo: res.longitude,
          currentLa: res.latitude,
          includePoints: [{
            longitude: res.longitude,
            latitude: res.latitude
          }],
          markers: [{
            id: 0,
            longitude: res.longitude,
            latitude: res.latitude,
            title: res.address,
            iconPath: '../../images/navi_s.png',
            width: 32,
            height: 32
          }]
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
  },

  // navigation
  getAddress(e){
    var _this = this;
    wx.chooseLocation({
      success(res) {
        var markers = _this.data.markers;
        markers.push({
          id: 0,
          longitude: res.longitude,
          latitude: res.latitude,
          title: res.address,
          iconPath: '../../images/navi_e.png',
          width: 32,
          height: 32
        });

        var points = _this.data.includePoints;
        points.push({
          longitude: res.longitude,
          latitude: res.latitude
        });
        _this.setData({
          newCurrentLo: res.longitude,
          newCurrentLa: res.latitude,
          includePoints: points,
          markers: markers,
          show: true
        });
        _this.getPolyline(_this.data.statusType);
      }
    });
  },
  drawPolyline(self, color){
    return {
      origin: this.data.currentLo + ',' + this.data.currentLa,
      destination: this.data.newCurrentLo + ',' + this.data.newCurrentLa,
      success(data) {
        var points = [];
        if (data.paths && data.paths[0] && data.paths[0].steps) {
          var steps = data.paths[0].steps;
          for (var i = 0; i < steps.length; i++) {
            var poLen = steps[i].polyline.split(';');
            for (var j = 0; j < poLen.length; j++) {
              points.push({
                longitude: parseFloat(poLen[j].split(',')[0]),
                latitude: parseFloat(poLen[j].split(',')[1])
              })
            }
          }
        }
        self.setData({
          distance: data.paths[0].distance,
          duration: parseInt(data.paths[0].duration / 60),
          polyline: [{
            points: points,
            color: color,
            width: 6,
            arrowLine: true
          }]
        });
      }
    }
  },
  getPolyline(_type){
    var amap = new amapFile.AMapWX({ key: this.data.key });
    var self = this;
    switch(_type) {
      case 'car':
      amap.getDrivingRoute(this.drawPolyline(this, "#0091ff"));
      break;
      case 'walk':
      amap.getWalkingRoute(this.drawPolyline(this, "#1afa29"));
      break;
      case 'ride':
      amap.getRidingRoute(this.drawPolyline(this, "#1296db"));
      break;
      default:
          return false;
    }
  },
  goTo(e){
    var _type = 'walk';
    this.setData({ statusType: _type });
    this.getPolyline(_type);
  }
})  