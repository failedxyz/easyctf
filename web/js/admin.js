$(document).ready(function() {
	$(".panel-title > a[data-toggle=collapse]").click(function(e) {
		e.preventDefault();
	});
});

var create_problem = function() {
	var input = "#new_problem_form input";
	var data = $("#new_problem_form").serializeObject();
	$(input).attr("disabled", "disabled");
	api_call("POST", "/api/problem/add", data, function(result) {
		if (result["success"] == 1) {
			display_message("add-status", "success", result["message"], function() {
				$(input).removeAttr("disabled");
			});
		} else {
			display_message("add-status", "danger", result["message"], function() {
				$(input).removeAttr("disabled");
			});
		}
	}, function(jqXHR, status, error) {
		var result = jqXHR["responseText"];
		display_message("add-status", "danger", "Error " + jqXHR["status"] + ": " + result["message"], function() {
			$(input).removeAttr("disabled");
		});
	});
}
