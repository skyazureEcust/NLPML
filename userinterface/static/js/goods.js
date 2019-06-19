//确定按钮事件：调用drawBar()函数画出热销商品TOP10的条形图和单个热销商品热销原因分析的饼图
function submit(){
	var startTime=$("#startTime").val()
	var endTime=$("#endTime").val()
	$.ajax({
		type: "GET",  
        url: "http://139.196.80.178:8080/goods?startTime="+startTime+"&endTime="+endTime,
        contentType: "application/json",
        success: function (data) {
			console.log(data["data1"],data["data2"],data["data3"])
        	drawBar(data["data1"],data["data2"],data["data3"])
    	}
    })
}

//画出热销商品TOP10的条形图和单个热销商品热销原因分析的饼图
function drawBar(data1,data2,data3){
	var dom = document.getElementById("container");
	var myChart = echarts.init(dom);
	var app = {};
	option = null;
	max=0
    for(var i=0;i<data2.length-1;i++){  
        for(var j=i+1;j<data2.length;j++){  
            if(data2[i]<data2[j]){//如果前面的数据比后面的小就交换  
                var temp=data2[i];  
                data2[i]=data2[j];  
                data2[j]=temp;  
                var temp=data1[i];  
                data1[i]=data1[j];  
                data1[j]=temp; 	
                var temp=data3[i];  
                data3[i]=data3[j];  
                data3[j]=temp; 					
            }  
        }
		max=Math.max(max,data2[i])
    }	

	for(var i=0;i<data2.length;i++){  
		data2[i]=Math.round(data2[i]/max*100)
	}

	option = {
		baseOption: {
			timeline: {
				axisType: 'category',
				autoPlay: true,
				playInterval: 1000,
				data: data1,
				label: {
					normal: {
						show: true
					}
				}
			},
			title: {
				subtext: '数据来自宝洁公司'
			},
			tooltip: {},
			legend: {
				x: 'right',
				data: ['优惠活动', '代言人', '产品质量']
			},
			calculable : true,
			grid: {
				top: 80,
				bottom: 100
			},
			xAxis: [
				{
					'type':'category',
					'axisLabel':{'interval':0},
					'data':data1,
					splitLine: {show: false}
				}
			],
			yAxis: [
				{
					type: 'value',
					name: '热销指数',
					max: 100
				}
			],
			series: [
				{name: 'total', type: 'bar'},
				{
					name: '热销原因占比',
					type: 'pie',
					center: ['85%', '25%'],
					radius: '28%'
				}
			]
		},
		options: [
			{
				title: {text: '热销商品排行TOP10'},
				series: [
					{data: data2},
					{data: data3[0]}
					]
			},
			{
				title : {text: '热销商品排行TOP10'},
				series : [
					{data: data2},
					{data: data3[1]}
					]
			},
			{
				title : {text: '热销商品排行TOP10'},
				series : [
					{data:  data2},
					{data: data3[2]}
                
				]
			},
			{
				title : {text: '热销商品排行TOP10'},
				series : [
					{data:  data2},
					{data: data3[3]}
				]  
			},
			{
				title : {text: '热销商品排行TOP10'},
				series : [
					{data:  data2},
					{data: data3[4]}
				]  
			},
			{
				title : {text: '热销商品排行TOP10'},
				series : [
					{data:  data2},
					{data: data3[5]}
				]    
			},
			{
				title : {text: '热销商品排行TOP10'},
				series : [
					{data:  data2},
					{data: data3[6]}
				] 
			},
			{
				title : {text: '热销商品排行TOP10'},
				series : [
					{data:  data2},
					{data: data3[7]}
                
				]
			},
			{
				title : {text: '热销商品排行TOP10'},
				series : [
					{data:  data2},
					{data: data3[8]}
                
				]
			},
			{
				title : {text: '热销商品排行TOP10'},
				series : [
					{data:  data2},
					{data: data3[9]}
                
				]
			}
		]
	};
	if (option && typeof option === "object") {
		myChart.setOption(option, true);
	}
}

 //页面初始化函数，通过POST返回一个默认值的条形图和饼图
function init(){

	$.ajax({
		type: "POST",  
        url: "http://139.196.80.178:8080",
        contentType: "application/json",
        success: function (data) {
        	console.log(data["data1"],data["data2"],data["data3"])
        	drawBar(data["data1"],data["data2"],data["data3"])
        	
    	}
    })
}

window.onload=init()