$(document).ready(function (){
	var empleado = $('input[name="empleado"]').val();
	$("#avisos").fullCalendar({
		eventSources: [{
			'url': '/notificacion/mostrar/avisos/' + empleado + '/'
		}],
		eventClick: function(calEvent, jsEvent, view) {
			dialog(calEvent.link);
		}
	});
});

function dialog(href){
	var dialog;
	$("<div style='display:none'></div>").load(href, function (){
		dialog = $(this);
		dialog.dialog({
			buttons: {
				Cerrar: function (){
					dialog.dialog('close');
				},
				Enviar: function(){
					submit_form(this, function (){
						$("#avisos").fullCalendar('refetchEvents');
						dialog.dialog('close');	
					});
					
				}
			}
		});
	});
}


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