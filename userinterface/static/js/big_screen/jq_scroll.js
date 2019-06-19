/*
jQ鍚戜笂婊氬姩甯︿笂涓嬬炕椤垫寜閽�
*/
(function($){
$.fn.extend({
        Scroll:function(opt,callback){
                //鍙傛暟鍒濆鍖�
                if(!opt) var opt={};
                var _btnUp = $("#"+ opt.up);//Shawphy:鍚戜笂鎸夐挳
                var _btnDown = $("#"+ opt.down);//Shawphy:鍚戜笅鎸夐挳
                var timerID;
                var _this=this.eq(0).find("ul:first");
                var     lineH=_this.find("li:first").height(), //鑾峰彇琛岄珮
                        line=opt.line?parseInt(opt.line,10):parseInt(this.height()/lineH,10), //姣忔婊氬姩鐨勮鏁帮紝榛樿涓轰竴灞忥紝鍗崇埗瀹瑰櫒楂樺害
                        speed=opt.speed?parseInt(opt.speed,10):500; //鍗峰姩閫熷害锛屾暟鍊艰秺澶э紝閫熷害瓒婃參锛堟绉掞級
                        timer=opt.timer //?parseInt(opt.timer,10):3000; //婊氬姩鐨勬椂闂撮棿闅旓紙姣锛�
                if(line==0) line=1;
                var upHeight=0-line*lineH;
                //婊氬姩鍑芥暟
                var scrollUp=function(){
                        _btnUp.unbind("click",scrollUp); //Shawphy:鍙栨秷鍚戜笂鎸夐挳鐨勫嚱鏁扮粦瀹�
                        _this.animate({
                                marginTop:upHeight
                        },speed,function(){
                                for(i=1;i<=line;i++){
                                        _this.find("li:first").appendTo(_this);
                                }
                                _this.css({marginTop:0});
                                _btnUp.bind("click",scrollUp); //Shawphy:缁戝畾鍚戜笂鎸夐挳鐨勭偣鍑讳簨浠�
                        });

                }
                //Shawphy:鍚戜笅缈婚〉鍑芥暟
                var scrollDown=function(){
                        _btnDown.unbind("click",scrollDown);
                        for(i=1;i<=line;i++){
                                _this.find("li:last").show().prependTo(_this);
                        }
                        _this.css({marginTop:upHeight});
                        _this.animate({
                                marginTop:0
                        },speed,function(){
                                _btnDown.bind("click",scrollDown);
                        });
                }
               //Shawphy:鑷姩鎾斁
                var autoPlay = function(){
                        if(timer)timerID = window.setInterval(scrollUp,timer);
                };
                var autoStop = function(){
                        if(timer)window.clearInterval(timerID);
                };
                 //榧犳爣浜嬩欢缁戝畾
                _this.hover(autoStop,autoPlay).mouseout();
                _btnUp.css("cursor","pointer").click( scrollUp ).hover(autoStop,autoPlay);//Shawphy:鍚戜笂鍚戜笅榧犳爣浜嬩欢缁戝畾
                _btnDown.css("cursor","pointer").click( scrollDown ).hover(autoStop,autoPlay);

        }       
})
})(jQuery);