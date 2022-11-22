	//var  title
	var doctitle="";
	//var for checking if fist entry changed
	var last_ticket="";
	var last_cabin="";
	//blinking counter
	var blink = 0;
	//refresh-interval
	update_document();
	setInterval(update_document, 2000);
	setInterval(update_date_time, 1000);
	
	function play_sound()
	{
		var audio = new Audio('ding.mp3');
		audio.play();
	}
	
	function submit_data() {
	    var http = new XMLHttpRequest();
	    http.open("POST", "answer.asp", true);
	    //http.setRequestHeader("Content-type","application/x-www-form-urlencoded");
	    var params = "search=123"; 
	    http.send(params);
	    http.onload = function() {
			var obj = JSON.parse(http.responseText); 
			
			
			
			if(obj.doc_title!=doctitle)
			{
				doctitle=obj.doc_title;
				document.getElementById("doc_title").innerHTML=doctitle;
			}
			
			if(obj.clear_screen==true)
			{
				document.getElementById("main_tab").style.display="none";
				document.getElementById("off_txt").style.display="inline";
				document.getElementById("off_txt").innerHTML="<br><br><br><br>" + obj.screen_message;
				clear_lst();
			}
			else
			{
				document.getElementById("main_tab").style.display="inline";
				document.getElementById("off_txt").style.display="none";
				update_lst(obj);
				display_arrows(obj);
				check_for_change(obj);
			}
	    }
	}
	
	function check_for_change(o)
	{
		if ((last_ticket != o.ticket_nr[0])||(last_cabin != o.cabin[0]))
		{
		last_ticket = o.ticket_nr[0];
		last_cabin = o.cabin[0]; 
		play_sound();
		blink=30;
		}
	}
	
	function do_events()
	{
		if(blink>0)
		{
			toggle_first_line();
			setTimeout(toggle_first_line, 400);
			blink=blink-1;
		}
	}
	
	function toggle_first_line()
	{
		if(document.getElementById("la1").style.color == 'rgb(0, 0, 0)')
		{
			document.getElementById("la1").style.color = "#f00";
			document.getElementById("lb1").style.color = "#f00";
		}
		else
		{
			document.getElementById("la1").style.color = "#000";
			document.getElementById("lb1").style.color = "#000";
		}
	}
	
	function update_date_time()
	{
		set_time("time_l");
		set_date("date_l");
	}
	
	function update_document()
	{
		submit_data();
		//update_date_time();
		do_events();
	}
	
	
	function set_time(time_id)
	{
		var d = new Date();
		document.getElementById(time_id).innerHTML = pad_number(d.getHours()) + ":" + pad_number(d.getMinutes()) + ":" + pad_number(d.getSeconds());
	}
	
	function set_date(date_id)
	{
		var d = new Date();
		document.getElementById(date_id).innerHTML = pad_number(d.getDate()) + "." + pad_number(String(d.getMonth()+1)) + "." + d.getFullYear();
	}
	
	function clear_lst()
	{
		var temp_o = {ticket_nr:["","","","","","","","","",""], cabin:["","","","","","","","","",""]};
		
		update_lst(temp_o);
	}
	
	function update_lst(o)
	{
		if(typeof o.ticket_nr[0] != 'undefined'){
		document.getElementById("la1").innerHTML = o.ticket_nr[0];
		document.getElementById("lb1").innerHTML = o.cabin[0]; 
		}
		else
		{
			document.getElementById("la1").innerHTML = "";
			document.getElementById("lb1").innerHTML = ""; 
		}
		if(typeof o.ticket_nr[1] != 'undefined'){
		document.getElementById("la2").innerHTML = o.ticket_nr[1];
		document.getElementById("lb2").innerHTML = o.cabin[1]; 
		}
		else
		{
			document.getElementById("la2").innerHTML = "";
			document.getElementById("lb2").innerHTML = ""; 
		}
		if(typeof o.ticket_nr[2] != 'undefined'){
		document.getElementById("la3").innerHTML = o.ticket_nr[2];
		document.getElementById("lb3").innerHTML = o.cabin[2]; 
		}
		else
		{
			document.getElementById("la3").innerHTML = "";
			document.getElementById("lb3").innerHTML = ""; 
		}
		if(typeof o.ticket_nr[3] != 'undefined'){
		document.getElementById("la4").innerHTML = o.ticket_nr[3];
		document.getElementById("lb4").innerHTML = o.cabin[3]; 
		}
		else
		{
			document.getElementById("la4").innerHTML = "";
			document.getElementById("lb4").innerHTML = ""; 
		}
		if(typeof o.ticket_nr[4] != 'undefined'){
		document.getElementById("la5").innerHTML = o.ticket_nr[4];
		document.getElementById("lb5").innerHTML = o.cabin[4]; 
		}
		else
		{
			document.getElementById("la5").innerHTML = "";
			document.getElementById("lb5").innerHTML = ""; 
		}
		if(typeof o.ticket_nr[5] != 'undefined'){
		document.getElementById("la6").innerHTML = o.ticket_nr[5];
		document.getElementById("lb6").innerHTML = o.cabin[5]; 
		}
		else
		{
			document.getElementById("la6").innerHTML = "";
			document.getElementById("lb6").innerHTML = ""; 
		}
		if(typeof o.ticket_nr[6] != 'undefined'){
		document.getElementById("la7").innerHTML = o.ticket_nr[6];
		document.getElementById("lb7").innerHTML = o.cabin[6]; 
		}
		else
		{
			document.getElementById("la7").innerHTML = "";
			document.getElementById("lb7").innerHTML = ""; 
		}
		if(typeof o.ticket_nr[7] != 'undefined'){
		document.getElementById("la8").innerHTML = o.ticket_nr[7];
		document.getElementById("lb8").innerHTML = o.cabin[7]; 
		}
		else
		{
			document.getElementById("la8").innerHTML = "";
			document.getElementById("lb8").innerHTML = ""; 
		}
		if(typeof o.ticket_nr[8] != 'undefined'){
		document.getElementById("la9").innerHTML = o.ticket_nr[8];
		document.getElementById("lb9").innerHTML = o.cabin[8]; 
		}
		else
		{
			document.getElementById("la9").innerHTML = "";
			document.getElementById("lb9").innerHTML = ""; 
		}
		if(typeof o.ticket_nr[9] != 'undefined'){
		document.getElementById("la10").innerHTML = o.ticket_nr[9];
		document.getElementById("lb10").innerHTML = o.cabin[9]; 
		}
		else
		{
			document.getElementById("la10").innerHTML = "";
			document.getElementById("lb10").innerHTML = ""; 
		}
	}
	
	function display_arrows(o)
	{
		if((o.ticket_nr[0]!="")&&(o.cabin[0]!="")&&(typeof o.ticket_nr[0] != 'undefined'))
		{
			document.getElementById("a1").style.color = "#000";
		}
		else
		{
			document.getElementById("a1").style.color = "#fff";
		}
		
		if((o.ticket_nr[1]!="")&&(o.cabin[1]!="")&&(typeof o.ticket_nr[1] != 'undefined'))
		{
			document.getElementById("a2").style.color = "#000";
		}
		else
		{
			document.getElementById("a2").style.color = "#fff";
		}
		if((o.ticket_nr[2]!="")&&(o.cabin[2]!="")&&(typeof o.ticket_nr[2] != 'undefined'))
		{
			document.getElementById("a3").style.color = "#000";
		}
		else
		{
			document.getElementById("a3").style.color = "#fff";
		}
		if((o.ticket_nr[3]!="")&&(o.cabin[3]!="")&&(typeof o.ticket_nr[3] != 'undefined'))
		{
			document.getElementById("a4").style.color = "#000";
		}
		else
		{
			document.getElementById("a4").style.color = "#fff";
		}
		if((o.ticket_nr[4]!="")&&(o.cabin[4]!="")&&(typeof o.ticket_nr[4] != 'undefined'))
		{
			document.getElementById("a5").style.color = "#000";
		}
		else
		{
			document.getElementById("a5").style.color = "#fff";
		}
		if((o.ticket_nr[5]!="")&&(o.cabin[5]!="")&&(typeof o.ticket_nr[5] != 'undefined'))
		{
			document.getElementById("a6").style.color = "#000";
		}
		else
		{
			document.getElementById("a6").style.color = "#fff";
		}
		if((o.ticket_nr[6]!="")&&(o.cabin[6]!="")&&(typeof o.ticket_nr[6] != 'undefined'))
		{
			document.getElementById("a7").style.color = "#000";
		}
		else
		{
			document.getElementById("a7").style.color = "#fff";
		}
		if((o.ticket_nr[7]!="")&&(o.cabin[7]!="")&&(typeof o.ticket_nr[7] != 'undefined'))
		{
			document.getElementById("a8").style.color = "#000";
		}
		else
		{
			document.getElementById("a8").style.color = "#fff";
		}
		if((o.ticket_nr[8]!="")&&(o.cabin[8]!="")&&(typeof o.ticket_nr[8] != 'undefined'))
		{
			document.getElementById("a9").style.color = "#000";
		}
		else
		{
			document.getElementById("a9").style.color = "#fff";
		}
		if((o.ticket_nr[9]!="")&&(o.cabin[9]!="")&&(typeof o.ticket_nr[9] != 'undefined'))
		{
			document.getElementById("a10").style.color = "#000";
		}
		else
		{
			document.getElementById("a10").style.color = "#fff";
		}
	}
	
	function pad_number(nr)
	{
		var s_nr=String(nr);
		var ret_val="";
		
		if(s_nr.length<2)
		{
			ret_val="0"+s_nr;
		}
		else
		{
			ret_val=s_nr;
		}
		return ret_val;
	}
	
