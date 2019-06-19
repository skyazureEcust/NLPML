function ECUSTMap(id) {
    var _this = this;

    /**
     * 三大校区坐标与缩放配置
     **/
    _this.XuHui = {
        point: new BMap.Point(121.43098, 31.150202),
        zoom: 17.5,
        polyline: new BMap.Polyline([
            new BMap.Point(121.435525, 31.14834),
            new BMap.Point(121.426542, 31.145041),
            new BMap.Point(121.425554, 31.146324),
            new BMap.Point(121.426156, 31.150766),
            new BMap.Point(121.427953, 31.152412),
            new BMap.Point(121.433109, 31.153756),
            new BMap.Point(121.433818, 31.153208),
            new BMap.Point(121.433836, 31.151894),
            new BMap.Point(121.434968, 31.152041),

            new BMap.Point(121.435525, 31.14834)

        ], {strokeColor: "blue", strokeWeight: 3, strokeOpacity: 0.5}),
        points: []

    };
    _this.FengXian = {
        point: new BMap.Point(121.510574, 30.837142),
        zoom: 17,
        polyline: new BMap.Polyline([
            new BMap.Point(121.518371, 30.836336),
            new BMap.Point(121.507861, 30.830569),
            new BMap.Point(121.502328, 30.837437),
            new BMap.Point(121.51246, 30.842724),

            new BMap.Point(121.518371, 30.836336)

        ], {strokeColor: "blue", strokeWeight: 3, strokeOpacity: 0.5}),
        points: []

    };
    _this.JinShan = {
        point: new BMap.Point(121.327025, 30.74614),
        zoom: 18,
        polyline: new BMap.Polyline([
            new BMap.Point(121.328876, 30.743921),
            new BMap.Point(121.326244, 30.74337),
            new BMap.Point(121.324681, 30.747544),
            new BMap.Point(121.328499, 30.748677),

            new BMap.Point(121.328876, 30.743921)

        ], {strokeColor: "blue", strokeWeight: 3, strokeOpacity: 0.5}),
        points: []

    };

    _this.allPoints = [];
    _this.allHeatPoints = [];
    // 热力图覆盖层初始化
    var HeatMapOverlay = null;
    // 蜂窝图初始化
    var HoneycombMap = null;
    var map = null;
    newMap(id);

    // 添加对外扩展接口
    _this.map = map;

    // 创建地图原型
    function newMap(id) {
        // 添加地图对象，并关闭POI功能
        var Bmap = new BMap.Map(id, {enableMapClick: false});
        // 开启鼠标滚轮缩放功能
        Bmap.enableScrollWheelZoom(true);
        // 添加带有定位的导航控件
        var navigationControl = new BMap.NavigationControl({
            // 靠左上角位置
            anchor: BMAP_ANCHOR_TOP_LEFT,
            // LARGE类型
            type: BMAP_NAVIGATION_CONTROL_SMALL,
            // 启用显示定位
            enableGeolocation: true
        });
        Bmap.addControl(navigationControl);

        // 添加校区范围
        Bmap.addOverlay(_this.XuHui.polyline);
        Bmap.addOverlay(_this.FengXian.polyline);
        Bmap.addOverlay(_this.JinShan.polyline);

        signature(Bmap);
        map = Bmap;
    }


    /**
     * 三大校区定位切换
     **/
    // 移动视觉中心至不同校区
    _this.moveToXuHui = function () {
        map.centerAndZoom(_this.XuHui.point, _this.XuHui.zoom);
    };

    _this.moveToFengXian = function () {
        map.centerAndZoom(_this.FengXian.point, _this.FengXian.zoom);
    };

    _this.moveToJinShan = function () {
        map.centerAndZoom(_this.JinShan.point, _this.JinShan.zoom);
    };


    /**
     * 标记点样式配置
     **/
    // 统一信息样式
    _this.msg = function (title, content, img) {
        var msgTitle = "<h5 style='text-align:center;font-weight:bold;margin:0 0 5px 0;padding:0.2em 0'>" + title + "</h5>";
        // var msgImage = "<img id='msgImg' style='margin:4px' src='" + img + "' width='150' height='auto'/>";
        var msgContent = content ;
        return "<div style='text-align: center'>" + msgTitle + msgContent + "</div>";
    };

    // 根据标记点添加事件
    _this.addMsg = function (marker, content) {
        // 创建信息窗口对象
        var infoWindow = new BMap.InfoWindow(content);
        // 监听点击坐标点与鼠标移动事件
        marker.addEventListener("onmouseover", function () {
            this.openInfoWindow(infoWindow);
            // 图片加载完毕重绘infowindow
            document.getElementById('msgImg').onload = function () {
                infoWindow.redraw();  //防止在网速较慢，图片未加载时，生成的信息框高度比图片的总高度小，导致图片部分被隐藏
            }
        });
        marker.addEventListener("click", function () {
            this.openInfoWindow(infoWindow);
            // 图片加载完毕重绘infowindow
            document.getElementById('msgImg').onload = function () {
                infoWindow.redraw();  //防止在网速较慢，图片未加载时，生成的信息框高度比图片的总高度小，导致图片部分被隐藏
            }
        });
    };


    /**
     * 标记点控制
     **/
    // 添加标记点
    _this.addPoint = function (lng, lat, count, iconUrl, campus) {
        var point = new BMap.Point(lng, lat);
        var Icon = new BMap.Icon(
            iconUrl,
            new BMap.Size(40, 40),
            {
                imageSize: new BMap.Size(40, 40)
            });
        // 生成坐标点
        var marker = new BMap.Marker(point, {
            icon: Icon,
            // 根据自定义的图标修改标记偏移值
            offset: new BMap.Size(0, -20)
        });
        // 设置跳动动画
        // marker.setAnimation(BMAP_ANIMATION_BOUNCE);

        map.addOverlay(marker);

        _this.allPoints.push({
            point: point,
            count: count
        });

        switch (campus) {
            case 'JinShan':
                _this.JinShan.points.push(marker);
                break;
            case 'FengXian':
                _this.FengXian.points.push(marker);
                break;
            default:
                _this.XuHui.points.push(marker);
        }

        return marker;
    };

    // 删除标记点
    _this.deleteAllPoints = function () {
        _this.hidePoints();
        _this.XuHui.points = [];
        _this.FengXian.points = [];
        _this.JinShan.points = [];
    };

    // 隐藏标记点
    _this.hidePoints = function () {

        for (var i = 0; i <= _this.XuHui.points.length - 1; i++) {
            map.removeOverlay(_this.XuHui.points[i]);
        }

        for (var i = 0; i <= _this.FengXian.points.length - 1; i++) {
            map.removeOverlay(_this.FengXian.points[i]);
        }

        for (var i = 0; i <= _this.JinShan.points.length - 1; i++) {
            map.removeOverlay(_this.JinShan.points[i]);
        }
    };

    // 显示标记点
    _this.showPoints = function () {

        for (var i = 0; i <= _this.XuHui.points.length - 1; i++) {
            map.addOverlay(_this.XuHui.points[i]);
        }

        for (var i = 0; i <= _this.FengXian.points.length - 1; i++) {
            map.addOverlay(_this.FengXian.points[i]);
        }

        for (var i = 0; i <= _this.JinShan.points.length - 1; i++) {
            map.addOverlay(_this.JinShan.points[i]);
        }
    };


    /**
     * 热力图控制
     **/
    // 添加热力点
    _this.addHeatPoint = function (lng, lat, count) {
        _this.allHeatPoints.push({
            geometry: {
                type: 'Point',
                coordinates: [lng, lat]
            },
            count: count
        });
    };

    // 删除热力点
    _this.deleteHeatPoints = function () {
        _this.closeHeatMap();
        _this.closeHoneycombMap();
        _this.allHeatPoints = [];
    };

    // 显示热力图
    _this.showHeatMap = function (max) {
        var dataSet = new mapv.DataSet(_this.allHeatPoints);
        var options = {
            max: max,
            size: 20,
            gradient: {
                1: "rgb(255,0,0)",
                0.9: "rgb(255,51,0)",
                0.8: "rgb(255,102,0)",
                0.7: "rgb(255,153,0)",
                0.6: "rgb(0,204,255)",
                0.5: "rgb(0,102,255)",
                0.4: "rgb(0,0,255)"
            },
            draw: 'heatmap'
        };

        HeatMapOverlay = new mapv.baiduMapLayer(map, dataSet, options);

    };

    // 关闭热力图
    _this.closeHeatMap = function () {
        if (HeatMapOverlay != null) {
            HeatMapOverlay.hide();
        }
    };


    /**
     * 地图样式配置
     **/
    // 更换地图样式
    _this.setMapStyle = function (mapStyle) {
        map.setMapStyle(mapStyle);
    };


    /**
     * 蜂窝图控制
     **/
    // 显示蜂窝图
    _this.showHoneycombMap = function (max) {
        var dataSet = new mapv.DataSet(_this.allHeatPoints);
        var options = {
            fillStyle: 'rgba(55, 50, 250, 0.8)',
            shadowColor: 'rgba(255, 250, 50, 1)',
            shadowBlur: 20,
            max: max,
            size: 30,
            label: {
                show: true,
                fillStyle: 'white',
                // shadowColor: 'yellow',
                // font: '20px Arial',
                // shadowBlur: 10,
            },
            globalAlpha: 0.5,
            gradient: {
                0.25: "rgb(0,0,255)",
                0.55: "rgb(0,255,0)",
                0.85: "yellow",
                1.0: "rgb(255,0,0)"
            },
            draw: 'honeycomb'
        };

        HoneycombMap = new mapv.baiduMapLayer(map, dataSet, options);
    };

    // 隐藏蜂窝图
    _this.closeHoneycombMap = function () {
        if (HoneycombMap != null) {
            HoneycombMap.hide();
        }
    };


    // 署名
    function signature(map) {
        // XX
        var xx1 = new BMap.Polyline([
            new BMap.Point(45.750025, -68.712996),
            new BMap.Point(59.584792, -73.293536)

        ], {strokeColor: "black", strokeWeight: 3, strokeOpacity: 0.5});
        map.addOverlay(xx1);

        var xx2 = new BMap.Polyline([
            new BMap.Point(59.584792, -68.712996),
            new BMap.Point(45.750025, -73.293536)

        ], {strokeColor: "black", strokeWeight: 3, strokeOpacity: 0.5});
        map.addOverlay(xx2);

        // QXX
        var point = new BMap.Point(109.331083, 84.194645);

        var label = new BMap.Label("QXX", {offset: new BMap.Size(-60, -60), position: point});
        label.setStyle({
            width: "120px",
            background: 'transparent',
            border: '1px solid "#ff8355"',
            borderRadius: "5px",
            textAlign: "center",
            height: "26px",
            lineHeight: "26px"
        });
        map.addOverlay(label);

    }
}

