!function(i){"use strict";i(function(){i(".icheck input").iCheck({checkboxClass:"icheckbox_minimal-blue",radioClass:"iradio_minimal",increaseArea:"20%"}),i(".icheck-square input").iCheck({checkboxClass:"icheckbox_square-blue",radioClass:"iradio_square",increaseArea:"20%"}),i(".icheck-flat input").iCheck({checkboxClass:"icheckbox_flat-blue",radioClass:"iradio_flat",increaseArea:"20%"});for(var e=i(".icheck-line input"),c=0;c<e.length;c++){var a=i(e[c]),s=a.next(),r=s.text();s.remove(),a.iCheck({checkboxClass:"icheckbox_line-blue",radioClass:"iradio_line",insert:'<div class="icheck_line-icon"></div>'+r})}i(".icheck-polaris input").iCheck({checkboxClass:"icheckbox_polaris",radioClass:"iradio_polaris",increaseArea:"20%"}),i(".icheck-futurico input").iCheck({checkboxClass:"icheckbox_futurico",radioClass:"iradio_futurico",increaseArea:"20%"})})}(jQuery);