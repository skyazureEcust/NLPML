//咨询按钮事件函数：调用drawPie()函数画出双饼图
function consult(){
	var startTime=$("#startTime").val()
	var endTime=$("#endTime").val()
	$.ajax({
		type: "GET",  
        url: "http://139.196.80.178:8080/consult?startTime="+startTime+"&endTime="+endTime,
        contentType: "application/json",
        success: function (data) {
        	console.log(data["data"],data["data1"],data["data2"],data["data3"])
        	drawPie(data["data1"],data["data2"],data["data3"])
			var a=document.getElementById("a")
			a.innerHTML="咨询"+"<p>"+data["data"]+"</p>"
    	}
    })
	
}

//投诉按钮事件函数：调用drawPie()函数画出双饼图
function complain(){
	var startTime=$("#startTime").val()
	var endTime=$("#endTime").val()
	$.ajax({
		type: "GET",  
        url: "http://139.196.80.178:8080/complain?startTime="+startTime+"&endTime="+endTime,
        contentType: "application/json",
		success: function (data) {
        	console.log(data["data"],data["data1"],data["data2"],data["data3"])
        	drawPie(data["data1"],data["data2"],data["data3"])
			var b=document.getElementById("b")
			b.innerHTML="投诉"+"<p>"+data["data"]+"</p>"
    	}
    })
}

//表扬按钮事件函数：调用drawPie()函数画出双饼图
function praise(){
	var startTime=$("#startTime").val()
	var endTime=$("#endTime").val()
	$.ajax({
		type: "GET",  
        url: "http://139.196.80.178:8080/praise?startTime="+startTime+"&endTime="+endTime,
        contentType: "application/json",
        success: function (data) {
        	console.log(data["data"],data["data1"],data["data2"],data["data3"])
        	drawPie(data["data1"],data["data2"],data["data3"])
			var c=document.getElementById("c")
			c.innerHTML="表扬"+"<p>"+data["data"]+"</p>"
    	}
    })
}

//服务按钮事件函数：调用drawPie()函数画出双饼图
function service(){
	var startTime=$("#startTime").val()
	var endTime=$("#endTime").val()
	$.ajax({
		type: "GET",  
        url: "http://139.196.80.178:8080/service?startTime="+startTime+"&endTime="+endTime,
        contentType: "application/json",
        success: function (data) {
        	console.log(data["data"],data["data1"],data["data2"],data["data3"])
        	drawPie(data["data1"],data["data2"],data["data3"])
			var d=document.getElementById("d")
			d.innerHTML="服务"+"<p>"+data["data"]+"</p>"
    	}
    })
	//var d=document.getElementById("d");
	//d.innerHTML=count;
}
	
//画双饼图函数
function drawPie(data1,data2,data3){

	var dom = document.getElementById("container");
	var myChart = echarts.init(dom);
	var app = {};
	option = null;

	option = {
		backgroundColor: '#ffffff',
		tooltip: {
			trigger: 'item',
			formatter: "{a} <br/>{b}: {c} ({d}%)"
		},
		legend: {
			orient: 'vertical',
			x: 'left',
			data:data1
		},
		series: [
        {
            name:'二级分类',
            type:'pie',
            selectedMode: 'single',
            radius: [0, '30%'],
			center: ['55%', '60%'],
            label: {
                normal: {
                    position: 'inner'
                }
            },
            labelLine: {
                normal: {
                    show: false
                }
            },
            data:data2
        },
        {
            name:'三级分类',
            type:'pie',
            radius: ['40%', '55%'],
			center: ['55%', '60%'],
            label: {
                normal: {
                    formatter: '{a|{a}}{abg|}\n{hr|}\n  {b|{b}：}{c}  {per|{d}%}  ',
                    backgroundColor: '#eee',
                    borderColor: '#aaa',
                    borderWidth: 1,
                    borderRadius: 4,

                    rich: {
                        a: {
                            color: '#999',
                            lineHeight: 22,
                            align: 'center'
                        },
                        hr: {
                            borderColor: '#aaa',
                            width: '100%',
                            borderWidth: 0.5,
                            height: 0
                        },
                        b: {
                            fontSize: 16,
                            lineHeight: 33
                        },
                        per: {
                            color: '#eee',
                            backgroundColor: '#334455',
                            padding: [2, 4],
                            borderRadius: 2
                        }
                    }
                }
            },
            data:data3
        }
		]
	};;
	if (option && typeof option === "object") {
		myChart.setOption(option, true);
	}
}

//页面初始化函数，通过POST返回一个默认值的双饼图
function init(){
	$.ajax({
		type: "GET",  
        url: "http://139.196.80.178:8080",
        contentType: "application/json",
        success: function (data) {
        	console.log(data["data1"],data["data2"],data["data3"])
        	drawPie(data["data1"],data["data2"],data["data3"])
        	
    	}
    })
}

window.onload=init()