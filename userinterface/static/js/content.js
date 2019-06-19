//确定按钮事件   
function submit(){
	sub1()   //画商品满意度的两个图表
	sub2()   //画客服满意度的两个图表
	sub3()   //画物流满意度的两个图表
	sub4()   //画活动满意度的两个图表
}

function sub1(){
var startTime=$("#startTime").val()
	var endTime=$("#endTime").val()
	$.ajax({
		type: "GET",  
        url: "http://139.196.80.178:8080/congoods?startTime="+startTime+"&endTime="+endTime,
        contentType: "application/json",
        success: function (data) {
			console.log()
        	drawGoods(data["data1"],data["data2"])
			
			console.log()
        	drawGoods2(data["data1"],data["data2"])	
    	}
    })
}

function sub2(){
var startTime=$("#startTime").val()
	var endTime=$("#endTime").val()
	$.ajax({
		type: "GET",  
        url: "http://139.196.80.178:8080/conservice?startTime="+startTime+"&endTime="+endTime,
        contentType: "application/json",
        success: function (data) {
			console.log()
        	drawService(data["data1"],data["data2"])
			
			console.log()
        	drawService2(data["data1"],data["data2"])	
    	}
    })
}

function sub3(){
var startTime=$("#startTime").val()
	var endTime=$("#endTime").val()
	$.ajax({
		type: "GET",  
        url: "http://139.196.80.178:8080/conlog?startTime="+startTime+"&endTime="+endTime,
        contentType: "application/json",
        success: function (data) {
			console.log()
        	drawLogs(data["data1"],data["data2"])
			
			console.log()
        	drawLog2(data["data1"],data["data2"])	
    	}
    })
}

function sub4(){
var startTime=$("#startTime").val()
	var endTime=$("#endTime").val()
	$.ajax({
		type: "GET",  
        url: "http://139.196.80.178:8080/conactivity?startTime="+startTime+"&endTime="+endTime,
        contentType: "application/json",
        success: function (data) {
			console.log(data["data1"],data["data2"],data["data3"])
        	drawActivity(data["data1"],data["data2"],data["data3"])
			
			console.log(data["data1"],data["data2"],data["data3"])
        	drawActivity2(data["data1"],data["data2"],data["data3"])
    	}
    })
}

//商品满意度的doughnut图
function drawGoods(data1,data2){
	var myChart = echarts.init(document.getElementById('goods'));
	var option= {
		tooltip : {
			formatter: "{a} <br/>{b} : {c}%"
		},
		series: [{
			name: '商品满意度',
			type: 'gauge',
			detail: {formatter:'{value}%'},
			data: [{value: (data1*100).toFixed(2), name: '商品满意度'}]
		}]
	};
	if (option && typeof option === "object") {
		myChart.setOption(option, true);
	}
}

//商品满意度词云图
 function drawGoods2(data1,data2){
	var text = data2;
	var data = text.split(/[\ ]+/g)
	.reduce(
		function (arr, word){
			var obj = arr.find(function (obj){
				return obj.name === word;
			});
			if (obj) {
				obj.weight += 1;
			} 
			else {
				obj = {
					name: word,
					weight: 1
				};
				arr.push(obj);
			}
			return arr;
		}, []);
		
		Highcharts.chart('goods2', {
			series: [{
				type: 'wordcloud',
				data: data
					}],
			title: {text: ''},
			credits: {
				enabled: false
				},
			exporting: {  
				enabled:false  
			}
		});
}

//客服满意度的排名表
function drawService(data1,data2){
	var kefu_paiming=document.getElementById('service');
	var arr_0=data1;
	str_0 = "";
	for(a=0;a<data1.length;a++){
		str_0 += "<tr>";
		for(b=0;b<3;b++){
			str_0 +="<td>"+arr_0[a][b]+"</td>";
		}
		str_0 += "</tr>";
	}
	kefu_paiming.innerHTML=str_0;
 }
 
//客服满意度的指标评分表
 function drawService2(data1,data2){
	var kefu_zhibiao=document.getElementById('service2');
	var arr=data2;
	str = "";
	for(i=0;i<data2.length;i++){
		str += "<tr>";
		for(j=0;j<5;j++){
			str +="<td>"+arr[i][j]+"</td>";
		}
		str += "</tr>";
	}
	kefu_zhibiao.innerHTML=str;
 }
 
//物流满意度的doughnut图
function drawLogs(data1,data2){
	var myChart = echarts.init(document.getElementById('logistic'));
	var option= {
		tooltip : {
			formatter: "{a} <br/>{b} : {c}%"
		},
		series: [{
			name: '物流满意度',
			type: 'gauge',
			detail: {formatter:'{value}%'},
			data: [{value: (data1*100).toFixed(2), name: '物流满意度'}]
		}]
	};
	if (option && typeof option === "object") {
		myChart.setOption(option, true);
	}
}

//物流问题分析的doughnut图
function drawLog2(data1,data2){
	var dom = document.getElementById("logistic2");
	var myChart = echarts.init(dom);
	var app = {};
	option = null;

	var scale = 1;
	var echartData =data2
	var rich = {
		yellow: {
			color: "#ffc72b",
			fontSize: 15 * scale,
			padding: [5, 4],
			align: 'center'
		},
		total: {
			color: "#ffc72b",
			fontSize: 40 * scale,
			align: 'center'
		},
		white: {
			color: "#fff",
			align: 'center',
			fontSize: 14 * scale,
			padding: [21, 0]
		},
		blue: {
			color: '#49dff0',
			fontSize: 13 * scale,
			align: 'center'
		},
		hr: {
			borderColor: '#0b5263',
			width: '100%',
			borderWidth: 1,
			height: 0,
		}
	}
	option = {
		backgroundColor: '#fff',
		title: {
			text:'物流会话总数',
			left:'center',
			top:'53%',
			padding:[24,0],
			textStyle:{
				color:'#c487ee',
				fontSize:16*scale,
				align:'center'
			}
		},
		legend: {
			selectedMode:false,
			formatter: function(name) {
				var total = 0; 
				var averagePercent; 
				echartData.forEach(function(value, index, array) {
					total += value.value;
				});
				return '{total|' + total + '}';
			},
			data: [echartData[0].name],
			left: 'center',
			top: 'center',
			icon: 'none',
			align:'center',
			textStyle: {
				color: "#c487ee",
				fontSize: 13 * scale,
				rich: rich
			},
		},
		series: [{
			name: '会话总数',
			type: 'pie',
			center: ['50%', '52%'],
			radius: ['35%', '45%'],
			hoverAnimation: true,
			color: ['#c487ee', '#deb140', '#49dff0', '#034079', '#6f81da', '#00ffb4'],
			label: {
				normal: {
					formatter: function(params, ticket, callback) {
						var total = 0; 
						var percent = 0;
						echartData.forEach(function(value, index, array) {
							total += value.value;
						});
						percent = ((params.value / total) * 100).toFixed(1);
						return '{yellow|' + params.name + '}\n{hr|}\n{yellow|' + params.value + '}\n{blue|' + percent + '%}';
					},
					rich: rich
				},
			},
			labelLine: {
				normal: {
					length: 45 * scale,
					length2:0,
					lineStyle: {
						color: '#0b5263'
					}
				}
			},
			data: echartData
		}]
	};
	if (option && typeof option === "object") {
		myChart.setOption(option, true);
	}
}
 
//活动满意度的doughnut图
function drawActivity(data1,data2,data3){
	var myChart = echarts.init(document.getElementById('activity'));
	var option= {
		tooltip : {
			formatter: "{a} <br/>{b} : {c}%"
		},
		series: [{
			name: '活动满意度',
			type: 'gauge',
			detail: {formatter:'{value}%'},
			data: [{value: (data1*100).toFixed(2), name: '活动满意度'}]
		}]
	};
	if (option && typeof option === "object") {
		myChart.setOption(option, true);
	}
	if (option && typeof option === "object") {
		myChart.setOption(option, true);
	}
}

//活动满意度的雷达图
function drawActivity2(data1,data2,data3){
	var dom = document.getElementById("activity2");
	var myChart = echarts.init(dom);
	var app = {};
	option = null;

	option = {
		radar: [{
            indicator: data2,
            center: ['50%','55%'],
            radius: 145
        }],
		series: [{
            type: 'radar',
			tooltip: {
                trigger: 'item'
            },
            itemStyle: {normal: {areaStyle: {type: 'default'}}},
            data: [{
                    value: data3,
                    name: '服务'
            }]
        }]
	};
	if (option && typeof option === "object") {
		myChart.setOption(option, true);
	}
}
 
function initGoods(){
	$.ajax({
		type: "POST",  
        url: "http://139.196.80.178:8080/congoods",
        contentType: "application/json",
        success: function (data) {
        	console.log(data["data1"],data["data2"])
        	drawGoods(data["data1"],data["data2"])
			
			console.log(data["data1"],data["data2"])
			drawGoods2(data["data1"],data["data2"])

    	}
    })
}

function initService(){
			

	$.ajax({
		type: "POST",  
        url: "http://139.196.80.178:8080/conservice",
        contentType: "application/json",
        success: function (data) {
			
			
			console.log(data["data1"],data["data2"])
        	drawService(data["data1"],data["data2"])
			
			console.log(data["data1"],data["data2"])
        	drawService2(data["data1"],data["data2"])	
					}
		})	
}

function initLog(){
	$.ajax({
		type: "POST",  
        url: "http://139.196.80.178:8080/conlog",
        contentType: "application/json",
        success: function (data) {
			
			console.log(data["data1"],data["data2"])
        	drawLogs(data["data1"],data["data2"])
			
			console.log(data["data1"],data["data2"])
        	drawLog2(data["data1"],data["data2"])	
			
    	}
    })
}

function initActivity(){
	$.ajax({
		type: "POST",  
        url: "http://139.196.80.178:8080/conactivity",
        contentType: "application/json",
        success: function (data) {
			
			console.log(data["data1"],data["data2"],data["data3"])
        	drawActivity(data["data1"],data["data2"],data["data3"])
			
			console.log(data["data1"],data["data2"],data["data3"])
        	drawActivity2(data["data1"],data["data2"],data["data3"])
    	}
    })
}

//页面初始化函数，通过POST返回商品、客服、物流、活动满意度的默认值图表
window.onload=initGoods()
window.onload=initService()
window.onload=initLog()
window.onload=initActivity()