!function(e){var a=echarts.init(document.getElementById("thermo_chart"));option={tooltip:{trigger:"axis",axisPointer:{type:"shadow"},formatter:function(e){return e[0].name+"<br/>"+e[0].seriesName+" : "+e[0].value+"<br/>"+e[1].seriesName+" : "+(e[1].value+e[0].value)}},legend:{selectedMode:!1,data:["Acutal","Forecast"]},calculable:!0,xAxis:[{type:"category",data:["Cosco","CMA","APL","OOCL","Wanhai","Zim"]}],yAxis:[{type:"value",boundaryGap:[0,.1]}],series:[{name:"Acutal",type:"bar",stack:"sum",barCategoryGap:"50%",itemStyle:{normal:{color:"#727cf5",barBorderColor:"#727cf5",barBorderWidth:6,barBorderRadius:0,label:{show:!0,position:"insideTop"}}},data:[260,200,220,120,100,80]},{name:"Forecast",type:"bar",stack:"sum",itemStyle:{normal:{color:"#fff",barBorderColor:"#727cf5",barBorderWidth:6,barBorderRadius:0,label:{show:!0,position:"top",formatter:function(e){for(var a=0,t=option.xAxis[0].data.length;a<t;a++)if(option.xAxis[0].data[a]==e.name)return option.series[0].data[a]+e.value},textStyle:{color:"#727cf5"}}}},data:[40,80,50,80,80,70]}]},a.setOption(option),e(window).on("resize",function(){null!=a&&null!=a&&a.resize()})}(jQuery);