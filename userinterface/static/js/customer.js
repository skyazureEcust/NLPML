//确定按钮事件：调用drawBar()函数画出重点客户和活跃客户TOP10的直方图
function submit(){
	var startTime=$("#startTime").val()
	var endTime=$("#endTime").val()
	$.ajax({
		type: "GET",  
        url: "http://139.196.80.178:8080/customers?startTime="+startTime+"&endTime="+endTime,
        contentType: "application/json",
        success: function (data) {
			console.log(data["cus1"],data["con1"],data["cus2"],data["con2"])
        	drawBar(data["cus1"],data["con1"],data["cus2"],data["con2"])
    	}
    })
}


//传入重点客户cus1和活跃客户cus2的TOP10列表，以及每个客户对应的满意度con1,con2
function drawBar(cus1,con1,cus2,con2){
    var colors = Highcharts.getOptions().colors,
    categories1 = cus1;
    categories2 = cus2;
	max1=0
	max2=0
    for(var i=0;i<cus1.length-1;i++){  
        for(var j=i+1;j<cus1.length;j++){  
            if(con1[i]<con1[j]){//如果前面的数据比后面的大就交换  
                var temp=con1[i];  
                con1[i]=con1[j];  
                con1[j]=temp;  
                var temp=cus1[i];  
                cus1[i]=cus1[j];  
                cus1[j]=temp; 				
            }  
			max1=Math.min(max1,con1[j])
        } 
		
    }   

	max1=(-1)*max1
	for(var i=0;i<con1.length;i++){  
		con1[i]=Math.round(con1[i]/max1*100)
	}
	
    for(var i=0;i<cus2.length-1;i++){  
        for(var j=i+1;j<cus2.length;j++){  
            if(con2[i]>con2[j]){//如果前面的数据比后面的大就交换  
                var temp=con2[i];  
                con2[i]=con2[j];  
                con2[j]=temp;  
                var temp=cus2[i];  
                cus2[i]=cus2[j];  
                cus2[j]=temp; 				
            }  
			max2=Math.max(max2,con2[j])
        }  
		
    }  	
	
	for(var i=0;i<con2.length;i++){  
		con2[i]=Math.round(con2[i]/max2*100)
	}
	categories1 = cus1;
    categories2 = cus2;
	
    $(document).ready(function () {
        $('#customergraph').highcharts({
            chart: {
                type: 'bar'
            },
            title: {
                text: '重点客户与活跃客户排行'
            },
            subtitle: {
                useHTML: true,
                text: '数据来源: P公司客服会话数据'
            },
			credits: {
				enabled: false
			},
			exporting: {  
				enabled:false  
			},
            xAxis: [{
                categories: categories1,
                reversed: false,
                labels: {
                    step: 1
                }
            }, { // mirror axis on right side
                opposite: true,
                reversed: false,
                categories: categories2,
                linkedTo: 0,
                labels: {
                    step: 1
                }
            }],
            yAxis: {
                title: {
                    text: null
                },
                labels: {
                    formatter: function () {
                        return (Math.abs(this.value) ) + '';
                    }
                },
                min: -100,
                max: 100
            },
            plotOptions: {
                series: {
                    stacking: 'normal'
                }
            },
            tooltip: {
                formatter: function () {
                    return '<b>' + this.series.name +  '</b><br/>' +
                        '评分: ' + Highcharts.numberFormat(Math.abs(this.point.y), 0);
                }
            },
            series: [{
                color: colors[0],
                name: '重点客户',
                data: con1
            }, {
                color: colors[2],
                name: '活跃客户',
                data: con2
            }]
        });
    });
}
 //页面初始化函数，通过POST返回一个默认值的直方图
function init(){
	var startTime=$("#startTime").val()
	var endTime=$("#endTime").val()
		$.ajax({
		type: "POST",  
        url: "http://139.196.80.178:8080/customers",
        contentType: "application/json",
        success: function (data) {
			console.log(data["cus1"],data["con1"],data["cus2"],data["con2"])
        	drawBar(data["cus1"],data["con1"],data["cus2"],data["con2"])
        	
    	}
    })
}

window.onload=init()