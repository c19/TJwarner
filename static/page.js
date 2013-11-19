function bind( obj, type, fn ) {       
if ( obj.attachEvent ) {       
		obj['e'+type+fn] = fn;       
		obj[type+fn] = function(){obj['e'+type+fn]( window.event );}       
		obj.attachEvent( 'on'+type, obj[type+fn] );       
	} else       
		obj.addEventListener( type, fn, false );       
}

district = document.getElementsByName('district')[0];

bind(district,'change',
	function () {
		current = document.getElementsByName('building')[0];
		current.removeAttribute('name');
		current.setAttribute('class','hide');
		newselect = document.getElementById(district.value);
		newselect.setAttribute('class','');
		newselect.setAttribute('name','building');
	}
);

button =  document.getElementById('button');
bind(button, 'click',
	function () {
		this.disabled = true;
		this.value = "正在查询电费，以及发送测试邮件，应该在10秒内完成。";
		form = document.getElementsByName('input')[0];
		form.submit();
		return true;
	}	
);