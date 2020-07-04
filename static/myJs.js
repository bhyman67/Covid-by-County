$(function() {
	$("#text-one").change(function() {
		$("#text-two").load("static/" + $(this).val() + ".txt");
	});
});