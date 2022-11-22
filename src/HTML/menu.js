submit_data("datasource=0");
update_selection();

	function submit_data(data) {
	    var http = new XMLHttpRequest();
	    http.open("POST", "json.asp", true);
	    //http.setRequestHeader("Content-type","application/x-www-form-urlencoded");
	    http.send(data);
	    http.onload = function() {
			var obj = JSON.parse(http.responseText); 
			//extracting ticket-list
			var t_lst = obj.ticket_lst;
			var n = t_lst.length;
			
			clear_select();
			
			for (i = 0; i < n; i++) {
				add_element_to_select(t_lst[i]);
			}
			update_selection();
			//title
			document.getElementById("mod_name").value=obj.title;
			document.getElementById("mod_name_in").value=obj.title;
			//off_txt
			document.getElementById("new_off_txt_in").value=obj.off_txt;
			//cabins
			document.getElementById("cab1").innerHTML = obj.cabin_lst[0];
			document.getElementById("cab2").innerHTML = obj.cabin_lst[1];
			document.getElementById("cab3").innerHTML = obj.cabin_lst[2];
			document.getElementById("cab4").innerHTML = obj.cabin_lst[3];
			document.getElementById("cab5").innerHTML = obj.cabin_lst[4];
			//active?
			if(obj.display_off==true)
			{
				inactive_display();
			}
			else
			{
				active_display();
			}
			
			
			
		}
	}
	
	function clear_select()
	{
		var select = document.getElementById("sel_tickets");
		var length_l = select.options.length;
		for (i = length_l-1; i >= 0; i--) {
			select.options[i] = null;
		}
		document.getElementById("pat_name_label").innerHTML = ""; 
	}
	
	function add_element_to_select(e)
	{
		var x = document.getElementById("sel_tickets");
		var option = document.createElement("option");
		option.text = e;
		x.add(option);
	}

function inactive_display()
{
	document.getElementById("main_tab").style.display="none";
	document.getElementById("msg_off").style.display="inline";
	main_menu();
}

function active_display()
{
	document.getElementById("main_tab").style.display="inline";
	document.getElementById("msg_off").style.display="none";
	main_menu();
}

function main_menu()
{
	document.getElementById("main_menu").style.display="block";
	document.getElementById("change_mod_name").style.display="none";
	document.getElementById("create_new_ticket").style.display="none";
	document.getElementById("mod_setup").style.display="none";
}

function setup_menu()
{
	document.getElementById("main_menu").style.display="none";
	document.getElementById("change_mod_name").style.display="none";
	document.getElementById("create_new_ticket").style.display="none";
	document.getElementById("mod_setup").style.display="block";
}

function change_name_menu()
{
	document.getElementById("main_menu").style.display="none";
	document.getElementById("change_mod_name").style.display="block";
	document.getElementById("create_new_ticket").style.display="none";
	document.getElementById("mod_setup").style.display="none";
	document.getElementById("mod_name_in").value=document.getElementById("mod_name").value;
	document.getElementById("mod_name_in").focus(); 
}

function ticket_menu()
{
	document.getElementById("main_menu").style.display="none";
	document.getElementById("change_mod_name").style.display="none";
	document.getElementById("create_new_ticket").style.display="block";
	document.getElementById("mod_setup").style.display="none";
	document.getElementById("new_ticket_in").value=""; 
	document.getElementById("new_ticket_in").focus(); 
}

function del_ticket()
{
	var tk_name = document.getElementById("pat_name_label").innerHTML; 
	if(tk_name!="")
	{
		var conf = confirm("Wollen Sie \"" + tk_name + "\" wirklich löschen?");
		if (conf == true) {
			submit_data("datasource=del_ticket&t_name=" + tk_name);
		} 
	}
}

function new_ticket()
{
	var tk_name = document.getElementById("new_ticket_in").value; 
	if(tk_name!="")
	{
		var re = tk_name.replace(/=|&|;|amp|"/gi , " ");
		submit_data("datasource=new_ticket&t_name=" + re);
		main_menu();
	}
}

function change_mod_name()
{
	var tk_name = document.getElementById("mod_name_in").value; 
	var re = tk_name.replace(/=|&|;|amp|"/gi , " ");
	submit_data("datasource=new_mod_name&mod_name=" + re);
	main_menu();
}

function change_off_txt()
{
	var tk_name = document.getElementById("new_off_txt_in").value; 
	var re = tk_name.replace(/=|&|;|amp|"/gi , " ");
	submit_data("datasource=new_off_txt&txt=" + re);
	main_menu();
}


function change_cab_status(nr, empty)
{
	 
	if(empty==true)
		{
			submit_data("datasource=change_cab_stat&t_name=Leer&number=" + nr);
		}
	else
		{
			var tk_name = document.getElementById("pat_name_label").innerHTML;
			if(tk_name!="")
			{
				submit_data("datasource=change_cab_stat&t_name=" + tk_name + "&number=" + nr);
			}
		}
}

function update_selection()
{
	d = document.getElementById("sel_tickets").value;
	document.getElementById("pat_name_label").innerHTML = d; 
}
