$(function() {
	$("#text-one").change(function() {
		$("#text-two").load($(this).val() + ".txt");
	});
});