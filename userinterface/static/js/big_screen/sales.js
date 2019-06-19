drawEcharts();
var myChartForPieSelect;
var optionForPieSelect;
function drawEcharts(){
	drawPie1();
	drawPie2();
	radar1(); 
	drawPie3();
	drawBar1();
	drawBar2();
	drawLine1();
	drawBar3();
	drawPie4();
}
//pie1
function drawPie1(){
var myChart = echarts.init(document.getElementById('pie1'));
var option = {
	    color:['#0657a1','#15cef0'],
	    grid: {
	    	show: false,
	    	left: '10%',
	    },
	    series: [
	        {
	            name:'',
	            type:'pie',
	            hoverAnimation:false,
	            selectedMode:false,
	            silent:true,//图形是否不响应和触发鼠标事件，默认为 false，即响应和触发鼠标事件。
	            center: ['40%', '50%'],//图表的横坐标、纵坐标
	            radius: ['60%', '75%'],
	            avoidLabelOverlap: false,
	            label: {
	                
	                    show: true,
	                    position: 'center',
	                    formatter:function(){
		                        	return '83%'
		                        },
                        textStyle : {
                            fontSize : '22',
//                            fontWeight : 'bold',
                            color: '#fff'
                          
                        }        
	            },
	            labelLine: {
	                normal: {
	                    show: false
	                }
	            },
	            data:[
	                {value:17, name:''},
	                {value:83, name:''}
	            ]
	        }
	    ]
	};
 myChart.setOption(option); 
}
 //pie2
function drawPie2(){
 var myChart1 = echarts.init(document.getElementById('pie2'));
 var option1 = {
		    color:['#0657a1','#15cef0'],
		    grid: {
		    	show: false,
		    	left: '10%',
		    },
		    series: [
		        {
		            name:'',
		            type:'pie',
		            hoverAnimation:false,
		            selectedMode:false,
		            silent:true,//图形是否不响应和触发鼠标事件，默认为 false，即响应和触发鼠标事件。
		            center: ['40%', '50%'],//图表的横坐标、纵坐标
		            radius: ['60%', '75%'],
		            avoidLabelOverlap: false,
		            label: {
		                
		                    show: true,
		                    position: 'center',
		                    formatter:function(){
			                        	return '20%'
			                        },
	                        textStyle : {
	                            fontSize : '22',
//	                            fontWeight : 'bold',
	                            color: '#fff'
	                          
	                        }        
		            },
		            labelLine: {
		                normal: {
		                    show: false
		                }
		            },
		            data:[
		                {value:80, name:''},
		                {value:20, name:''}
		            ]
		        }
		    ]
		};
  myChart1.setOption(option1); 
}
//radar1
function radar1(){
	var myChart = echarts.init(document.getElementById('radar1'));
	var dataBJ = [
	    [267,216,280,4.8,108,64,9]
	];

	var lineStyle = {
	    normal: {
	        width: 1,
	        opacity: 0.5
	    }
	};

	var option = {
	    backgroundColor: '#121640',
	    radar: {
	        indicator: [
	            {name: '支付宝', max: 300},
	            {name: '会员卡', max: 250},
	            {name: '银联卡', max: 300},
	            {name: '现金', max: 5},
	            {name: '挂账', max: 200},
	            {name: '微信', max: 100}
	        ],
	        shape: 'circle',
	        splitNumber: 4,
	        name: {
	            show: true,
	            color: 'rgb(255, 255, 255)',
	            fontSize:16,
	            
	        },
	        splitLine: {
	            lineStyle: {
	                color: 'rgba(255, 255, 255, 0.1)'
	            }
	        },
	        splitArea: {
	            show: false
	        },
	        axisLine: {
	            lineStyle: {
	                color: 'rgba(255, 255, 255, 0.1)'
	            }
	        }
	    },
	    series: [
	        {
	            name: '支付方式',
	            type: 'radar',
	            lineStyle: lineStyle,
	            data: dataBJ,
	            symbol: 'none',
	            itemStyle: {
	                normal: {
	                    color: '#dde039'
	                }
	            },
	            areaStyle: {
	                normal: {
	                    opacity: 0.6
	                }
	            }
	        } 
	    ]
	};
	 myChart.setOption(option); 
}
//pie3
function drawPie3(){
// var 
	myChartForPieSelect = echarts.init(document.getElementById('pie3'));
// var
 optionForPieSelect = {
		    color:['#0657a1','#ff558d','#d7e432','#15cef0','#d4b583','#6053d7'],
		    series: [
		        {
		            name:'',
		            type:'pie',
		            center: ['48%', '50%'],//图表的横坐标、纵坐标
		            radius: ['75%', '85%'],
		            avoidLabelOverlap: false,
		            label: {
		                normal: {
		                    show: false,
		                    position: 'center'
		                },
		                emphasis: {
		                    show: true,
		                    textStyle: {
		                        fontSize: '16',
		                        color:'#FFFFFF'
		                    },
		                    formatter:  "{b}\n\n{d}%"
		                }
		            },
		            labelLine: {
		                normal: {
		                    show: false
		                }
		            },
		            data:[
		                {value:63, name:'堂食'},
		                {value:4, name:'百度外卖'},
		                {value:11, name:'美团外卖'},
		                {value:7, name:'饿了么'},
		                {value:6, name:'大众点评'},
		                {value:9, name:'支付宝'}
		            ]
		        }
		    ]
		};
 	myChartForPieSelect.setOption(optionForPieSelect); 

//  myChart.dispatchAction({
//	    type: 'downplay',
//	    seriesIndex: 0,
//	    dataIndex: 0
//	});
//	myChart.dispatchAction({
//	    type: 'highlight',
//	    seriesIndex: 0,
//	    dataIndex: 0
//	});
//	myChart.dispatchAction({
//	    type: 'showTip',
//	    seriesIndex: 0,
//	    dataIndex: 0
//	});
  
}
 

//轮流选择环形图
let currentIndex = -1;
var dataLen = optionForPieSelect.series[0].data.length;
setInterval(function() {
//     currentIndex--;
//     alert("currentIndex--:"+currentIndex); 
     if(currentIndex<dataLen-1){
       // 取消之前高亮的图形
       myChartForPieSelect.dispatchAction({
	           type: 'downplay',
	           seriesIndex: 0,
	           dataIndex: currentIndex
	       });
	   var toHighligt = (currentIndex + 1) % dataLen;
    	// 高亮当前图形
       myChartForPieSelect.dispatchAction({
           type: 'highlight',
           seriesIndex: 0,
           dataIndex: toHighligt
       });
       currentIndex++;
     }else{
    	// 取消之前高亮的图形
         myChartForPieSelect.dispatchAction({
  	           type: 'downplay',
  	           seriesIndex: 0,
  	           dataIndex: currentIndex
  	       });// 
  	   currentIndex=0;
      	// 高亮当前图形
         myChartForPieSelect.dispatchAction({
             type: 'highlight',
             seriesIndex: 0,
             dataIndex: currentIndex
         });
         
     }
 }, 1000);

//$("#pie3").mouseenter(function() {
//	gradeEchart.dispatchAction({
//	    type: 'downplay',
//	    seriesIndex: 0,
//	    dataIndex: currentIndex
//	});
//});
//$("#pie3").mouseleave(function() {
//	gradeEchart.dispatchAction({
//	    type: 'highlight',
//	    seriesIndex: 0,
//	    dataIndex: currentIndex
//	});
//});

function drawBar1(){
	var myChart = echarts.init(document.getElementById('bar1'));
	var option = {
		    color: {
		                type: 'linear',
		                x: 0,
		                y: 0,
		                x2: 0,
		                y2: 1,
		                colorStops: [{
		                    offset: 0, color: '#01ffcf' // 0% 处的颜色
		                }, {
		                    offset: 1, color: '#008bd3' // 100% 处的颜色
		                }],
		                globalCoord: false // 缺省为 false
		            },
		    xAxis: {
		        data: ['美团', '饿了么', '微信', '支付宝','大众点评', '百度外卖', '其他'],
		        axisTick: {show: false},
		        axisLine: {//坐标轴样式
				                show: false,
				                  lineStyle: {
				                      color: '#1398ff'
				                  }
				            },
		    },
		    yAxis: {
		         axisLine: {//坐标轴样式
				                show: false,
				            },
		         axisLabel: {//坐标值样式
		                          show: false, 
		                      },
		         splitLine: {show: false},
		         axisTick: {show: false},//分割线
		    },
		    series: [{
		        type: 'bar',
		        itemStyle: {
		            normal: {
		                color: '#082d4b'//bar的背景色
		            }
		        },
		        silent: true,//图形是否支持触发事件
		        barWidth: 16,
		        barGap: '-100%', // Make series be overlap
		        data: [7, 7, 7, 7, 7, 7, 7]
		    }, {
		        type: 'bar',
		        barWidth: 16,
//		        barCategoryGap:'100%',
		        z: 10,
		        itemStyle: {
		              normal: {
		                barBorderRadius:2, 
		                 
		                label: {
		                  show: true,
		                  textStyle: {
		                	  fontSize:'14',
		                      color: '#078fc0'
		                  },  
		                  position: 'top',//数据在中间显示
		                  formatter:'{c}'//百分比显示
		                }
		                
		              }
		        },
		        data: [7, 6, 5, 4,3,2,1]
		    }]
		};
	myChart.setOption(option); 
}

function drawBar2(){
	var myChart = echarts.init(document.getElementById('bar2'));
	var option = {
		    color: {
		                type: 'linear',
		                x: 1,
		                y: 0,
		                x2: 0,
		                y2: 0,
		                colorStops: [{
		                    offset: 0, color: '#01ffcf' // 0% 处的颜色
		                }, {
		                    offset: 1, color: '#008bd3' // 100% 处的颜色
		                }],
		                globalCoord: false // 缺省为 false
		            },
		    xAxis: {
		    	type: 'value',
				            axisLine: {//坐标轴样式
				                show: false,
				            },
		         axisLabel: {//坐标值样式
		                          show: false, 
		                      },
		         splitLine: {show: false},
		         axisTick: {show: false},//分割线
		    },
		    yAxis: {
		    	type: 'category',
		    	 data: ['沙茶风味鸡排', '大咖特调炸鸡', '老鸭汤冒菜', '高丽参鸡汤鲜辣烫','蓝莓多拿滋', '芒果杯', '樱桃芝士','柚多美大果粒', '红豆布丁奶茶', '椰果奶茶'],
			        axisTick: {show: false},
			        axisLine: {//坐标轴样式
					                show: false,
					                  lineStyle: {
					                      color: '#1398ff'
					                  }
					            },
		    },
		    grid: { // 控制图的大小，调整下面这些值就可以，
	             x: 80,
	             x2: 50,
	             y2: 5,// y2可以控制 X轴跟Zoom控件之间的间隔，避免以为倾斜后造成 label重叠到zoom上
	         },
		    series: [{
		        type: 'bar',
		        itemStyle: {
		            normal: {
		                color: '#082d4b'//bar的背景色
		            }
		        },
		        silent: true,//图形是否支持触发事件
		        barWidth: 16,
		        barGap: '-100%', // Make series be overlap
		        data: [10, 10, 10, 10, 10, 10, 10,10,10,10]
		    }, {
		        type: 'bar',
		        barWidth: 16,
//		        barCategoryGap:'100%',
		        z: 10,
		        itemStyle: {
		              normal: {
		                barBorderRadius:2, 
		                 
		                label: {
		                  show: true,
		                  textStyle: {
		                	  fontSize:'14',
		                      color: '#078fc0'
		                  },  
		                  position: 'right',//数据在中间显示
		                  formatter:'{c}'//百分比显示
		                }
		                
		              }
		        },
		        data: [1, 2, 3, 4,5,6,7,8,9,10]
		    }]
		};
	myChart.setOption(option); 
}
function drawLine1(){
	var myChart = echarts.init(document.getElementById('line1'));
	var option = {
		    // title: {
		    //     text: '折线图堆叠'
		    // },
		    // tooltip: {
		    //     trigger: 'axis'
		    // },
		    // legend: {
		    //     data:['邮件营销','联盟广告','视频广告','直接访问','搜索引擎']
		    // },
		    color:['#04ceb0','#f0f103'],
		    grid: {
		        left: '3%',
		        right: '4%',
		        bottom: '3%',
		        containLabel: true
		    },
		    // toolbox: {
		    //     feature: {
		    //         saveAsImage: {}
		    //     }
		    // },
		    xAxis: {
		        type: 'category',
		        boundaryGap: false,
		        data: ['1','2','3','4','5','6','7'],
		          axisLine: {//坐标轴样式
						                show: true,
						            },
				         axisLabel: {//坐标值样式
				                          show: true, 
				                          color:'#04ceb0',
				                      },
				         splitLine: {show: false},
				         axisTick: {show: false},//分割线
		    },
		    yAxis: {
		        type: 'value',
		          axisLine: {//坐标轴样式
						                show: false,
						            },
				         axisLabel: {//坐标值样式
				                          show: false, 
				                      },
				         splitLine: {show: true,
				             lineStyle: {
							                      color: '#0f1936'
							                  }
				         },
				         axisTick: {show: false},//分割线
		    },
		    series: [
		        // {
		        //     name:'邮件营销',
		        //     type:'line',
		        //     stack: '总量',
		        //     data:[120, 132, 101, 134, 90, 230, 210]
		        // },
		        // {
		        //     name:'联盟广告',
		        //     type:'line',
		        //     stack: '总量',
		        //     data:[220, 182, 191, 234, 290, 330, 310]
		        // },
		        // {
		        //     name:'视频广告',
		        //     type:'line',
		        //     stack: '总量',
		        //     data:[150, 232, 201, 154, 190, 330, 410]
		        // },
		        {
		            name:'直接访问',
		            type:'line',
		            stack: '总量',
		            data:[520, 332, 301, 334, 390, 330, 320]
		        },
		        {
		            name:'搜索引擎',
		            type:'line',
		            stack: '总量',
		            data:[820, 932, 901, 934, 1290, 1330, 1320]
		        }
		    ]
		};
	myChart.setOption(option); 
}

function drawBar3(){
	var myChart = echarts.init(document.getElementById('bar3'));
	var option = {
		    color: {
		                type: 'linear',
		                x: 1,
		                y: 0,
		                x2: 0,
		                y2: 0,
		                colorStops: [{
		                    offset: 0, color: '#01ffcf' // 0% 处的颜色
		                }, {
		                    offset: 1, color: '#008bd3' // 100% 处的颜色
		                }],
		                globalCoord: false // 缺省为 false
		            },
		    xAxis: {
		    	type: 'value',
				            axisLine: {//坐标轴样式
				                show: false,
				            },
		         axisLabel: {//坐标值样式
		                          show: false, 
		                      },
		         splitLine: {show: false},
		         axisTick: {show: false},//分割线
		    },
		    yAxis: {
		    	type: 'category',
		    	 data: ['安徽', '黑龙江', '吉林', '辽宁','浙江'],
			        axisTick: {show: false},
			        axisLine: {//坐标轴样式
					                show: false,
					                  lineStyle: {
					                      color: '#1398ff'
					                  }
					            },
		    },
		    grid: { // 控制图的大小，调整下面这些值就可以，
	             x: 50,
	             x2: 30,
	             y2: 5,// y2可以控制 X轴跟Zoom控件之间的间隔，避免以为倾斜后造成 label重叠到zoom上
	         },
		    series: [{
		        type: 'bar',
		        itemStyle: {
		            normal: {
		                color: '#fcf51f'//bar的背景色
		            }
		        },
		        silent: true,//图形是否支持触发事件
		        barWidth: 12,
		        barGap: '20%', // Make series be overlap
		        data: [5, 2, 6, 4, 7]//, 7, 7
		    }, {
		        type: 'bar',
		        barWidth: 12,
//		        barCategoryGap:'100%',
		        z: 10,
		        itemStyle: {
		              normal: {
		                barBorderRadius:2, 
		                 
		                label: {
		                  show: true,
		                  textStyle: {
		                	  fontSize:'14',
		                      color: '#078fc0'
		                  },  
		                  position: 'right',//数据在中间显示
		                  formatter:''//'{c}'//百分比显示
		                }
		                
		              }
		        },
		        data: [7, 6, 5, 4,3]//,2,1,3,2,1
		    }]
		};
	myChart.setOption(option); 
}

function drawPie4(){
	// var 
	var myChart = echarts.init(document.getElementById('pie4'));
	// var
	var option = {
			    color:['#d7e432','#0657a1'],
			    series: [
			        {
			            name:'',
			            type:'pie',
			            center: ['48%', '50%'],//图表的横坐标、纵坐标
			            radius: ['65%', '85%'],
			            avoidLabelOverlap: false,
//			            hoverAnimation:false,
//			            selectedMode:false,
			            silent:true,//图形是否不响应和触发鼠标事件，默认为 false，即响应和触发鼠标事件。
			            label: {
			                normal: {
			                    show: false,
			                    position: 'center'
			                },
			                emphasis: {
			                    show: true,
			                    textStyle: {
			                        fontSize: '16',
			                        color:'#FFFFFF'
			                    },
			                    formatter:  ""//"{b}\n\n{d}%"
			                }
			            },
			            labelLine: {
			                normal: {
			                    show: false
			                }
			            },
			            data:[
			                {value:15, name:'新客户'},
			                {value:36, name:'老客户'}
//			                {value:11, name:'美团外卖'},
//			                {value:7, name:'饿了么'},
//			                {value:6, name:'大众点评'},
//			                {value:9, name:'支付宝'}
			            ]
			        }
			    ]
			};
	myChart.setOption(option); 

	//  myChart.dispatchAction({
//		    type: 'downplay',
//		    seriesIndex: 0,
//		    dataIndex: 0
//		});
		myChart.dispatchAction({
		    type: 'highlight',
		    seriesIndex: 0,
		    dataIndex: 0
		});
//		myChart.dispatchAction({
//		    type: 'showTip',
//		    seriesIndex: 0,
//		    dataIndex: 0
//		});
	  
	}