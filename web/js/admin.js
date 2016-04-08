$(document).ready(function() {
	$(".panel-title > a[data-toggle=collapse]").click(function(e) {
		e.preventDefault();
	});
});

var create_problem = function() {
	var input = "#new_problem_form input";
	var data = $("#new_problem_form").serializeObject();
	var grader_contents = ace.edit("new_grader").getValue();
	data["grader_contents"] = grader_contents;
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
};

var update_problem = function(form_id) {
	var input = "#" + form_id + " input";
	var data = $("#" + form_id).serializeObject();
	pid = data["pid"];

	var grader_contents = ace.edit(pid + "_grader").getValue();
	data["grader_contents"] = grader_contents;

	$(input).attr("disabled", "disabled");
	api_call("POST", "/api/problem/update", data, function(result) {
		if (result["success"] == 1) {
			display_message(pid + "_status", "success", result["message"], function() {
				$(input).removeAttr("disabled");
			});
		} else {
			display_message(pid + "_status", "danger", result["message"], function() {
				$(input).removeAttr("disabled");
			});
		}
	}, function(jqXHR, status, error) {
		var result = jqXHR["responseText"];
		display_message(pid + "_status", "danger", "Error " + jqXHR["status"] + ": " + result["message"], function() {
			$(input).removeAttr("disabled");
		});
	});
};

var delete_problem = function(form_id) {
	$('#confirm').modal("show", { backdrop: 'static', keyboard: false })
        .one('click', '#delete', function() {
		var input = "#" + form_id + " input";
		var pid = form_id.split("_")[1];
		$(input).attr("disabled", "disabled");
		api_call("POST", "/api/problem/delete", {"pid": pid}, function(result) {
			if (result["success"] == 1) {
				display_message(pid + "_status", "success", result["message"], function() {
					$(input).removeAttr("disabled");
				});
			} else {
				display_message(pid + "_status", "danger", result["message"], function() {
					$(input).removeAttr("disabled");
				});
			}
		}, function(jqXHR, status, error) {
			var result = jqXHR["responseText"];
			display_message(pid + "_status", "danger", "Error " + jqXHR["status"] + ": " + result["message"], function() {
				$(input).removeAttr("disabled");
			});
		});

        });
}
