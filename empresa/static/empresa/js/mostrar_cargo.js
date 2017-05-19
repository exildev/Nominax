$(document).ready(function (){
	$("ul#popups a").click(function (){
		var href = $(this).attr("href");
		var form = $(this).attr("form");
		var dialog;
		$("<div style='display:none'></div>").load(href, function (){
			dialog = $(this);
			if (form){
				dialog.dialog({
					buttons: {
						Cerrar: function (){
							dialog.dialog('close');
						},
						Enviar: function(){
							submit_form(this, function (){
								dialog.dialog('close');	
							});
							
						}
					}
				});
			}else{
				dialog.dialog({
					buttons: {
						Cerrar: function (){
							dialog.dialog('close');
						}
					}
				})
			}
		});
		return false;
	});
});

function submit_form(self, success){
	form = $(self).children('form');
	form.ajaxSubmit({
		target: self,
		success: function (text, statusText, xhr, $form){
			if (xhr.status === 201){
				success();
			}
		}
	});

}