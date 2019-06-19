//画双饼图函数
function drawPie(data1,data2,data3){
	var dom = document.getElementById("chart_1");
	var myChart = echarts.init(dom);
	var app = {};
	option = null;

	option = {
		
		tooltip: {
			trigger: 'item',
			formatter: "{a} <br/>{b}: {c} ({d}%)"
		},
		legend: {
			orient: 'vertical',
			x: 'left',
			data:data1,
			textStyle:{//图例文字的样式
				color:'#fff',
				fontSize:10
        }
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

//画图谱函数
function drawChart(data1,data2,data3,data4){
	var dom = document.getElementById("shenji_charts");
	var myChart = echarts.init(dom);
	var app = {};
	option = null;

	//var legendes =data1 ;
	var texts = [{"name":"trade","itemStyle":{"normal":{"color":"#2ca4bf"}}}];
	var listdata = data3;
	var links = data4;

	var option = {
        title: {
            text: ''
        },
		/*
        legend: {
            data: legendes
        },
        tooltip: {
            formatter: function (parmes) {
                if(parmes.data.name){
                    return legendes[parmes.data.category] +": " + parmes.name;
                }
            }
        },   */		
		animationDurationUpdate: 300,
        animationEasingUpdate: 'quinticInOut',
        series : [
            {
                type: 'graph',
                layout:'force',
                symbol:'circle',
                symbolSize:15,
                roam: true,
                focusNodeAdjacency:false,
                legendHoverLink:true,
                draggable:true,
                force : {
                    repulsion :240,
                    gravity : 0.03,
                    edgeLength :80,
                    layoutAnimation : true
                },
                categories: texts,
                label: {
                    normal: {
                        show: true,
                        position:"left",
                        textStyle:{
                            color:'#000',
                            fontSize:'12'
                        }

                    }
                },
                data: listdata,
                links:links,
                lineStyle: {
                    normal: {
                        width: 1,
                        color: {
                            type: 'radial',
                            x: 0.5,
                            y: 0.5,
                            r: 0.5,
                            globalCoord: false 
                        }

                    }
                }
            }
        ]
    };
	if (option && typeof option === "object") {
		myChart.setOption(option, true);
	}
}

//页面初始化函数，通过POST返回一个默认值的双饼图
function init(){
	window.d={"data1":[1],"data2":[0],"data3":[0],}
	$.ajax({
		type: "GET",  
        url: "http://localhost:8080",
        contentType: "application/json",
        success: function (data) {
        	console.log(data["data1"],data["data2"],data["data3"])
			d["data1"]=data["data1"]
			d["data2"]=data["data2"]
			d["data3"]=data["data3"]
			
			drawPie(d["data1"],d["data2"],d["data3"]);

    	},

    })

}

function chart(){
	$.ajax({
		type: "GET",  
        url: "http://localhost:8080/chart",
        contentType: "application/json",
        success: function (data) {
        	console.log(data["data1"],data["data2"],data["data3"],data["data4"])		
			drawChart(data["data1"],data["data2"],data["data3"],data["data4"]);

    	},

    })

}

//window.onload=init()
window.onload=chart()