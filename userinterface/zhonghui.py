# -*- coding: UTF-8 -*-
import web
import json
import MySQLdb

web.config.debug = False
render = web.template.render('templates/')
urls = (
    '/', 'zhonghui',
	'/chart', 'chart',
	'/way', 'way',
	'/mode', 'mode',
	'/product', 'product',
	'/agent', 'agent',
)
conn=MySQLdb.connect(host='fx2.huilab.cn',  port=3306,  user='root',  passwd='123456', db='trade',charset='utf8') 
conn.set_character_set('utf8') 
cursor=conn.cursor() 

class zhonghui:
    def GET(self):
        return render.zhonghui()
		
	def POST(self):
		web.header('content-type','text/json')
		web.header("Access-Control-Allow-Origin", "*")
			
		data={"data1":["事件产品", "事件人物", "事件主题", "背景事件", "事件品牌"],\
		"data2":[{"name":"事件产品","itemStyle":{"normal":{"color":"#2ca4bf"}}},{"name":"事件人物","itemStyle":{"normal":{"color":"#aacf44"}}},{"name":"事件主题","itemStyle":{"normal":{"color":"#ff9945"}}},{"name":"背景事件","itemStyle":{"normal":{"color":"#3ad1c5"}}},{"name":"事件品牌","itemStyle":{"normal":{"color":"#f7cb4a"}}}],\
		"data3":[{"name":"视频内容分析","category":0,"label":{"normal":{"show":"true","textStyle":{"color":"#2ca4bf"}}}},{"name":"云服务器BBC","category":0,"label":{"normal":{"show":"true","textStyle":{"color":"#2ca4bf"}}}},{"name":"理解与交互技术UNIT","category":0,"label":{"normal":{"show":"true","textStyle":{"color":"#2ca4bf"}}}},{"name":"文字识别","category":0,"label":{"normal":{"show":"true","textStyle":{"color":"#2ca4bf"}}}},{"name":"人脸识别","category":0,"label":{"normal":{"show":"true","textStyle":{"color":"#2ca4bf"}}}},{"name":"智能推荐BRS","category":0,"label":{"normal":{"show":"true","textStyle":{"color":"#2ca4bf"}}}},{"name":"视频内容分析VCA","category":0,"label":{"normal":{"show":"true","textStyle":{"color":"#2ca4bf"}}}},{"name":"视频内容审核 VCR","category":0,"label":{"normal":{"show":"true","textStyle":{"color":"#2ca4bf"}}}},{"name":"语音识别","category":0,"label":{"normal":{"show":"true","textStyle":{"color":"#2ca4bf"}}}},{"name":"视频内容审核","category":0,"label":{"normal":{"show":"true","textStyle":{"color":"#2ca4bf"}}}},{"name":"视频封面选图","category":0,"label":{"normal":{"show":"true","textStyle":{"color":"#2ca4bf"}}}},{"name":"图像识别","category":0,"label":{"normal":{"show":"true","textStyle":{"color":"#2ca4bf"}}}},{"name":"百度深度学习","category":0,"label":{"normal":{"show":"true","textStyle":{"color":"#2ca4bf"}}}},{"name":"视频封面选图VCS","category":0,"label":{"normal":{"show":"true","textStyle":{"color":"#2ca4bf"}}}},{"name":"张亚勤","category":1,"label":{"normal":{"show":"true","textStyle":{"color":"#aacf44"}}}},{"name":"百度与银联商务正式达成战略合作协议","category":2,"label":{"normal":{"show":"true","textStyle":{"color":"#ff9945"}}}},{"name":"百度云ABC技术标识——ABC Inspire发布，进入Cloud2.0时代","category":2,"label":{"normal":{"show":"true","textStyle":{"color":"#ff9945"}}}},{"name":"百度云高级产品专家黄锋视频AI产品发布","category":2,"label":{"normal":{"show":"true","textStyle":{"color":"#ff9945"}}}},{"name":"Ruff成为百度云生态合作伙伴","category":2,"label":{"normal":{"show":"true","textStyle":{"color":"#ff9945"}}}},{"name":"华数传媒网络有限公司亮相2017百度云智峰会","category":2,"label":{"normal":{"show":"true","textStyle":{"color":"#ff9945"}}}},{"name":"未来域，南京度房与百度云合作","category":2,"label":{"normal":{"show":"true","textStyle":{"color":"#ff9945"}}}},{"name":"百度云北京沙龙","category":2,"label":{"normal":{"show":"true","textStyle":{"color":"#ff9945"}}}},{"name":"百度公司总裁张亚勤百度云智峰会聊云计算","category":2,"label":{"normal":{"show":"true","textStyle":{"color":"#ff9945"}}}},{"name":"百度云CDN流量包1折闪促","category":2,"label":{"normal":{"show":"true","textStyle":{"color":"#ff9945"}}}},{"name":"百度云与传媒行业战略合作签约视频时代","category":2,"label":{"normal":{"show":"true","textStyle":{"color":"#ff9945"}}}},{"name":"百度云总经理尹世明云智峰会展示黑科技","category":2,"label":{"normal":{"show":"true","textStyle":{"color":"#ff9945"}}}},{"name":"2017百度云智峰会","category":3,"label":{"normal":{"show":"true","textStyle":{"color":"#3ad1c5"}}}},{"name":"百度云","category":4,"label":{"normal":{"show":"true","textStyle":{"color":"#f7cb4a"}}}}],
		"data4":[{"source":"Ruff成为百度云生态合作伙伴","target":"百度云"},{"source":"百度与银联商务正式达成战略合作协议","target":"百度云"},{"source":"百度云","target":"人脸识别"},{"source":"百度云","target":"百度深度学习"},{"source":"百度云北京沙龙","target":"百度云"},{"source":"2017百度云智峰会","target":"百度云总经理尹世明云智峰会展示黑科技"},{"source":"百度云总经理尹世明云智峰会展示黑科技","target":"百度云"},{"source":"百度云","target":"图像识别"},{"source":"2017百度云智峰会","target":"百度云与传媒行业战略合作签约视频时代"},{"source":"百度云与传媒行业战略合作签约视频时代","target":"百度云"},{"source":"百度云","target":"视频封面选图VCS"},{"source":"百度云","target":"视频内容分析"},{"source":"百度云","target":"语音识别"},{"source":"百度云","target":"视频内容审核"},{"source":"百度云","target":"理解与交互技术UNIT"},{"source":"百度云","target":"视频封面选图"},{"source":"百度云","target":"视频内容分析VCA"},{"source":"百度云","target":"视频内容审核 VCR"},{"source":"2017百度云智峰会","target":"百度云高级产品专家黄锋视频AI产品发布"},{"source":"百度云高级产品专家黄锋视频AI产品发布","target":"百度云"},{"source":"百度云","target":"文字识别"},{"source":"2017百度云智峰会","target":"华数传媒网络有限公司亮相2017百度云智峰会"},{"source":"华数传媒网络有限公司亮相2017百度云智峰会","target":"百度云"},{"source":"百度云","target":"智能推荐BRS"},{"source":"2017百度云智峰会","target":"百度云ABC技术标识——ABC Inspire发布，进入Cloud2.0时代"},{"source":"百度云ABC技术标识——ABC Inspire发布，进入Cloud2.0时代","target":"百度云"},{"source":"百度云ABC技术标识——ABC Inspire发布，进入Cloud2.0时代","target":"张亚勤"},{"source":"2017百度云智峰会","target":"百度公司总裁张亚勤百度云智峰会聊云计算"},{"source":"百度公司总裁张亚勤百度云智峰会聊云计算","target":"百度云"},{"source":"百度云","target":"云服务器BBC"},{"source":"百度公司总裁张亚勤百度云智峰会聊云计算","target":"张亚勤"},{"source":"未来域，南京度房与百度云合作","target":"百度云"},{"source":"百度云CDN流量包1折闪促","target":"百度云"}],}

		return json.dumps(data)
		
	def OPTIONS(self):
		web.header('Access-Control-Allow-Origin', '*')
		web.header('Access-Control-Allow-Headers',  'Content-Type, Access-Control-Allow-Origin, Access-Control-Allow-Headers, X-Requested-By, Access-Control-Allow-Methods')
		web.header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE')
		
		

#图谱
class chart:
	def GET(self):
		web.header('content-type','text/json')
		web.header("Access-Control-Allow-Origin", "*")
		conn=MySQLdb.connect(host='fx2.huilab.cn',  port=3306,  user='root',  passwd='123456', db='trade',charset='utf8') 
		conn.set_character_set('utf8') 
		cursor=conn.cursor() 
		
		
		#sql="select distinct TKR_INSTN_EN_SHRT_NM from fx_deal union select distinct EN_SHRT_NM from fx_deal"
		sql="select EN_SHRT_NM,count(DL_CD) from fx_deal where TKR_INSTN_EN_SHRT_NM='ICBC' or EN_SHRT_NM='ICBC' group by EN_SHRT_NM"
		count=cursor.execute(sql)
		rows=cursor.fetchall()

		div_list=[]
		sum=0
		min=10
		for row in rows:
			sum=sum+int(row[1])
		for row in rows:
			size=int(row[1])*200/sum
			if size<min:
				size=min
			result={"name": str(row[0]),"value":int(row[1]),"symbolSize":size, "category":0,"label":{"normal":{"show":"true","textStyle":{"color":"#aacf44"}}}}
			div_list.append(result)
			
		conn=MySQLdb.connect(host='fx2.huilab.cn',  port=3306,  user='root',  passwd='123456', db='trade',charset='utf8') 
		conn.set_character_set('utf8') 
		cursor=conn.cursor() 
		sql1="select TKR_INSTN_EN_SHRT_NM,EN_SHRT_NM from fx_deal where TKR_INSTN_EN_SHRT_NM='ICBC' or EN_SHRT_NM='ICBC'"
		count=cursor.execute(sql1)
		rows=cursor.fetchall()
		div_list1=[]
		for row in rows:
			result={'source': str(row[0]), 'target': str(row[1])}
			div_list1.append(result)

		data1=[]
		data2=[]
		data={"data1":data1,"data2":data2,"data3":div_list,"data4":div_list1,}
		print data
		return json.dumps(data)
		
	def OPTIONS(self):
		web.header('Access-Control-Allow-Origin', '*')
		web.header('Access-Control-Allow-Headers',  'Content-Type, Access-Control-Allow-Origin, Access-Control-Allow-Headers, X-Requested-By, Access-Control-Allow-Methods')
		web.header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE')
		
#交易方式
class way:
	def GET(self):
		web.header('content-type','text/json')
		web.header("Access-Control-Allow-Origin", "*")
		conn=MySQLdb.connect(host='fx2.huilab.cn',  port=3306,  user='root',  passwd='123456', db='trade',charset='utf8') 
		conn.set_character_set('utf8') 
		cursor=conn.cursor() 
		
		
		#sql="select distinct TKR_INSTN_EN_SHRT_NM from fx_deal union select distinct EN_SHRT_NM from fx_deal"
		sql="select TRDNG_MTHD_CD,count(DL_CD) from fx_deal where TKR_INSTN_EN_SHRT_NM='ICBC' or EN_SHRT_NM='ICBC' group by TRDNG_MTHD_CD"
		count=cursor.execute(sql)
		rows=cursor.fetchall()

		div_list=[]
		for row in rows:
			if str(row[0])=='ESP':
				nameItem='点击成交'
			elif str(row[0])=='Matching':
				nameItem='连续撮合'
			elif str(row[0])=='Negotiate':
				nameItem='协商成交'
			elif str(row[0])=='RFQ':
				nameItem='询价成交'
			result={"name": nameItem,"value":int(row[1])}
			div_list.append(result)

		data={"data1":div_list,}
		return json.dumps(data)
		
	def OPTIONS(self):
		web.header('Access-Control-Allow-Origin', '*')
		web.header('Access-Control-Allow-Headers',  'Content-Type, Access-Control-Allow-Origin, Access-Control-Allow-Headers, X-Requested-By, Access-Control-Allow-Methods')
		web.header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE')
		
#交易模式
class mode:
	def GET(self):
		web.header('content-type','text/json')
		web.header("Access-Control-Allow-Origin", "*")
		conn=MySQLdb.connect(host='fx2.huilab.cn',  port=3306,  user='root',  passwd='123456', db='trade',charset='utf8') 
		conn.set_character_set('utf8') 
		cursor=conn.cursor() 
		
		
		sql="select TRDNG_MD_CD,count(DL_CD) from fx_deal where TKR_INSTN_EN_SHRT_NM='ICBC' or EN_SHRT_NM='ICBC' group by TRDNG_MD_CD"
		count=cursor.execute(sql)
		rows=cursor.fetchall()

		div_list=[]
		for row in rows:
			if str(row[0])=='ODM':
				nameItem='订单驱动'
			elif str(row[0])=='QDM':
				nameItem='报价驱动'
			elif str(row[0])=='NDM':
				nameItem='协商驱动'
			result={"name": nameItem,"value":int(row[1])}
			div_list.append(result)

		data1=[x['name'] for x in div_list]
	
		data={"data1":data1,"data2":div_list,}
		return json.dumps(data)
		
	def OPTIONS(self):
		web.header('Access-Control-Allow-Origin', '*')
		web.header('Access-Control-Allow-Headers',  'Content-Type, Access-Control-Allow-Origin, Access-Control-Allow-Headers, X-Requested-By, Access-Control-Allow-Methods')
		web.header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE')

#交易产品
class product:
	def GET(self):
		web.header('content-type','text/json')
		web.header("Access-Control-Allow-Origin", "*")
		conn=MySQLdb.connect(host='fx2.huilab.cn',  port=3306,  user='root',  passwd='123456', db='trade',charset='utf8') 
		conn.set_character_set('utf8') 
		cursor=conn.cursor() 
		
		sql="select PRDCT_CD,count(DL_CD) from fx_deal where TKR_INSTN_EN_SHRT_NM='ICBC' or EN_SHRT_NM='ICBC' group by PRDCT_CD"
		count=cursor.execute(sql)
		rows=cursor.fetchall()

		div_list=[]
		for row in rows:
			if str(row[0])=='FIRDV':
				nameItem='货币掉期'
			elif str(row[0])=='FXCL':
				nameItem='外币拆借'
			elif str(row[0])=='FXF':
				nameItem='外汇远期'
			elif str(row[0])=='FXO':
				nameItem='外汇期权'
			elif str(row[0])=='FXSPT':
				nameItem='外汇即期'
			elif str(row[0])=='FXSWP':
				nameItem='外汇掉期'
			result={"name": nameItem,"value":int(row[1])}
			div_list.append(result)

		data={"data1":div_list,}
		return json.dumps(data)
		
#交易量
class agent:
	def GET(self):
		web.header('content-type','text/json')
		web.header("Access-Control-Allow-Origin", "*")
		conn=MySQLdb.connect(host='fx2.huilab.cn',  port=3306,  user='root',  passwd='123456', db='trade',charset='utf8') 
		conn.set_character_set('utf8') 
		cursor=conn.cursor() 
		
		#每月发起量
		sql="select count(DL_CD),CONCAT(YEAR(TXN_DT),'-',MONTH(TXN_DT)) AS releaseYearMonth from fx_deal \
		where TKR_INSTN_EN_SHRT_NM='ICBC' group by releaseYearMonth order by releaseYearMonth"
		count=cursor.execute(sql)
		rows=cursor.fetchall()

		div_list=[]
		for row in rows:
			result={"amount": int(row[0]),"date":str(row[1])}
			div_list.append(result)
		
		#每月报价量
		sql1="select count(DL_CD),CONCAT(YEAR(TXN_DT),'-',MONTH(TXN_DT)) AS releaseYearMonth from fx_deal \
		where EN_SHRT_NM='ICBC' group by releaseYearMonth order by releaseYearMonth"
		count=cursor.execute(sql1)
		rows=cursor.fetchall()

		div_list1=[]
		for row in rows:
			result={"amount": int(row[0]),"date":str(row[1])}
			div_list1.append(result)


		date1=[x['date'] for x in div_list]
		date2=[x['date'] for x in div_list1]
		amount1=[x['amount'] for x in div_list]
		amount2=[x['amount'] for x in div_list1]
		data1=date1+date2
		list=[]
		for i in data1:
			if i not in list:
				list.append(i)
		#data1=list(set(data1)).sort(key=data1.index)
		
		data2=[]
		amount3=[]
		amount4=[]
		for item in list:
			i=0
			while i<len(date1):
				if item==date1[i]:
					item1=amount1[i]
					break
				else:
					item1=0
				i=i+1
			amount3.append(item1)
				
				
			i=0
			while i<len(date2):
				if item==date2[i]:
					item2=amount2[i]
					break
				else:
					item2=0
				i=i+1
			amount4.append(item2)
		data2.append(amount3)
		data2.append(amount4)
		print data2
	
		data={"data1":list,"data2":data2,}
		return json.dumps(data)
		
	def OPTIONS(self):
		web.header('Access-Control-Allow-Origin', '*')
		web.header('Access-Control-Allow-Headers',  'Content-Type, Access-Control-Allow-Origin, Access-Control-Allow-Headers, X-Requested-By, Access-Control-Allow-Methods')
		web.header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE')
		
if __name__ == "__main__":
    app = web.application(urls, globals())
    # session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'username': None})
    app.run()