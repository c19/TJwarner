districts = {
	"jiading":'
	<option value="07号公寓    ">07号公寓    </option>
	<option value="08号公寓    ">08号公寓    </option>
	<option value="09号公寓    ">09号公寓    </option>
	<option value="10号公寓    ">10号公寓    </option>
	<option value="12号公寓    ">12号公寓    </option>
	<option value="13号公寓    ">13号公寓    </option>
	<option value="14号公寓    ">14号公寓    </option>
	<option value="15号公寓    ">15号公寓    </option>
	<option value="16号公寓    ">16号公寓    </option>
	<option value="17号公寓    ">17号公寓    </option>
	<option value="18号公寓    ">18号公寓    </option>
	<option selected="selected" value="19号楼      ">19号楼      </option>
	<option value="20号楼      ">20号楼      </option>
	<option value="本科4       ">本科4       </option>
	<option value="本科5       ">本科5       </option>
	<option value="本科6       ">本科6       </option>
	<option value="研究2       ">研究2       </option>
	<option value="研究3       ">研究3       </option>',
	"siping":'
	<option value="赤峰路后勤2">赤峰路后勤2</option>
	<option value="后勤工寓    ">后勤工寓    </option>
	<option value="后勤公寓三相">后勤公寓三相</option>
	<option value="解放楼      ">解放楼      </option>
	<option value="青年楼      ">青年楼      </option>
	<option value="西北二楼    ">西北二楼    </option>
	<option value="西北三楼    ">西北三楼    </option>
	<option value="西北四楼    ">西北四楼    </option>
	<option value="西北五楼    ">西北五楼    </option>
	<option value="西北一楼    ">西北一楼    </option>
	<option value="西南八楼    ">西南八楼    </option>
	<option value="西南二楼    ">西南二楼    </option>
	<option value="西南九楼    ">西南九楼    </option>
	<option value="西南七楼    ">西南七楼    </option>
	<option value="西南三楼    ">西南三楼    </option>
	<option value="西南十二楼  ">西南十二楼  </option>
	<option value="西南十楼A楼">西南十楼A楼</option>
	<option value="西南十楼B楼">西南十楼B楼</option>
	<option value="西南十一楼  ">西南十一楼  </option>
	<option value="西南一楼    ">西南一楼    </option>
	<option value="学三楼      ">学三楼      </option>
	<option value="学四楼      ">学四楼      </option>
	<option value="学五楼      ">学五楼      </option>
	<option value="研究生公寓3 ">研究生公寓3 </option>
	<option value="研究生公寓4">研究生公寓4</option>
	<option value="研究生公寓5">研究生公寓5</option>',
	"siping2":'
	<option value="行政北楼    ">行政北楼    </option>
	<option value="行政南楼    ">行政南楼    </option>',
	"zhangwu":'
	<option value="1号楼       ">1号楼       </option>
	<option value="2号楼       ">2号楼       </option>
	<option value="3号楼       ">3号楼       </option>
	<option value="4号楼       ">4号楼       </option>
	<option value="5号楼       ">5号楼       </option>
	<option value="6号楼       ">6号楼       </option>
	<option value="7号楼       ">7号楼       </option>',
	"hubei":'
	<option value="第二宿舍    ">第二宿舍    </option>
	<option value="第三宿舍    ">第三宿舍    </option>
	<option value="第一宿舍    ">第一宿舍    </option>',
}

function bind( obj, type, fn ) {       
if ( obj.attachEvent ) {       
obj['e'+type+fn] = fn;       
obj[type+fn] = function(){obj['e'+type+fn]( window.event );}       
obj.attachEvent( 'on'+type, obj[type+fn] );       
} else       
obj.addEventListener( type, fn, false );       
}

bind(district,'change',function(){})