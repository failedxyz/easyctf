var app = angular.module("easyctf", [ "ngRoute" ]);

app.config(["$compileProvider", function($compileProvider) {
	$compileProvider.aHrefSanitizationWhitelist(/^\s*(https?|ftp|mailto|file|javascript):/);
}]);
app.config(function($routeProvider, $locationProvider) {
	$routeProvider.when("/", {
		templateUrl: "pages/home.html",
		controller: "mainController"
	})
	.when("/about", {
		templateUrl: "pages/about.html",
		controller: "mainController"
	})
	.when("/chat", {
		templateUrl: "pages/chat.html",
		controller: "mainController"
	})
	.when("/learn", {
		templateUrl: "pages/learn.html",
		controller: "mainController"
	})
	.when("/login", {
		templateUrl: "pages/login.html",
		controller: "mainController"
	})
	.when("/logout", {
		templateUrl: "pages/blank.html",
		controller: "logoutController"
	})
	.when("/profile", {
		templateUrl: "pages/profile.html",
		controller: "profileController"
	})
	.when("/profile/:username", {
		templateUrl: "pages/profile.html",
		controller: "profileController"
	})
	.when("/register", {
		templateUrl: "pages/register.html",
		controller: "mainController"
	})
	.when("/scoreboard", {
		templateUrl: "pages/scoreboard.html",
		controller: "mainController"
	})
	.when("/settings", {
		templateUrl: "pages/settings.html",
		controller: "mainController"
	})
	.when("/forgot", {
		templateUrl: "pages/forgot.html",
		controller: "resetController"
	})
	.when("/forgot/:token", {
		templateUrl: "pages/forgot.html",
		controller: "resetController"
	})
	.when("/team", {
		templateUrl: "pages/team.html",
		controller: "teamController"
	})
	.when("/team/:teamname", {
		templateUrl: "pages/team.html",
		controller: "teamController"
	})
	.when("/admin/problems", {
		templateUrl: "pages/admin/problems.html",
		controller: "adminProblemsController"
	})
	.otherwise({
		templateUrl: "pages/404.html",
		controller: "mainController"
	});
	$locationProvider.html5Mode(true);
});

app.controller("mainController", ["$scope", "$http", function($scope, $http) {
	$scope.config = { navbar: { } };
	$.get("/api/user/status", function(result) {
		if (result["success"] == 1) {
			delete result["success"];
			$scope.config.navbar = result;
			$scope.$emit("loginStatus");
		} else {
			$scope.config.navbar.logged_in = false;
		}
		$scope.$apply();
	}).fail(function() {
		$scope.config.navbar.logged_in = false;
		$scope.$apply();
	});
}]);

app.controller("logoutController", function() {
	$.get("/api/user/logout", function(result) {
		location.href = "/";
	});
});

app.controller("profileController", ["$controller", "$scope", "$http", "$routeParams", function($controller, $scope, $http, $routeParams) {
	var data = { };
	if ("username" in $routeParams) data["username"] = $routeParams["username"];
	$controller("mainController", { $scope: $scope });
	$.get("/api/user/info", data, function(result) {
		if (result["success"] == 1) {
			$scope.user = result["user"];
		}
		$scope.$apply();
		$(".timeago").timeago();
	});
}]);

app.controller("loginController", ["$controller", "$scope", "$http", function($controller, $scope, $http) {
	$controller("mainController", { $scope: $scope });
	$scope.$on("loginStatus", function() {
		if ($scope.config["navbar"].logged_in != true) {
			location.href = "/login";
			return;
		}
	});
}]);

app.controller("teamController", ["$controller", "$scope", "$http", "$routeParams", function($controller, $scope, $http, $routeParams) {
	var data = { };
	if ("teamname" in $routeParams) {
		data["teamname"] = $routeParams["teamname"];
	} else {
		$controller("loginController", { $scope: $scope });
	}
}]);

app.controller("resetController", ["$controller", "$scope", "$http", "$routeParams", function($controller, $scope, $http, $routeParams) {
	var data = { };
    $scope.token = false;
    data["csrf_token"] = $.cookie("csrf_token");
	if ("token" in $routeParams) {
        $scope.token = true;
		token = $routeParams["token"];
		$.get("/api/user/forgot/" + token, data, function(data) {
            $scope.body = data["message"];
            $scope.success = data["success"]
            $scope.$apply();
		});
	} else {
		$controller("mainController", { $scope: $scope });
	}
}]);

app.controller("adminController", ["$controller", "$scope", "$http", function($controller, $scope, $http) {
	$controller("mainController", { $scope: $scope });
	$scope.$on("loginStatus", function() {
		if ($scope.config["navbar"].logged_in != true) {
			location.href = "/login";
			return;
		}
		if ($scope.config["navbar"].admin != true) {
			location.href = "/profile";
			return;
		}
	});
}]);

app.controller("adminProblemsController", ["$controller", "$scope", "$http", function($controller, $scope, $http) {
	$controller("adminController", { $scope: $scope });
	$.get("/api/admin/problems/list", function(result) {
		if (result["success"] == 1) {
			$scope.problems = result["problems"];
		}
		$scope.$apply();
	});
}]);

function display_message(containerId, alertType, message, callback) {
	$("#" + containerId).html("<div class=\"alert alert-" + alertType + "\">" + message + "</div>");
	$("#" + containerId).hide().slideDown("fast", "swing", function() {
		window.setTimeout(function () {
			$("#" + containerId).slideUp("fast", "swing", callback);
		}, message.length * 75);
	});
};

function api_call(method, url, data, callback) {
	if (method.toLowerCase() == "post") {
		data["csrf_token"] = $.cookie("csrf_token");
	}
	$.ajax({
		"type": method,
		"datatype": "json",
		"data": data,
		"url": url
	}).done(callback);
}

$.fn.serializeObject = function() {
	var a, o;
	o = {};
	a = this.serializeArray();
	$.each(a, function() {
		if (o[this.name]) {
			if (!o[this.name].push) {
				o[this.name] = [o[this.name]];
			}
			return o[this.name].push(this.value || "");
		} else {
			return o[this.name] = this.value || "";
		}
	});
	return o;
};

// register page

var register_form = function() {
	var input = "#register_form input";
	var data = $("#register_form").serializeObject();
	api_call("POST", "/api/user/register", data, function(result) {
		if (result["success"] == 1) {
			location.href = "/profile";
		} else {
			display_message("register_msg", "danger", result["message"]);
		}
	}).fail(function(jqXHR, status, error) {
		var result = JSON.parse(jqXHR["responseText"]);
		display_message("register_msg", "danger", "Error " + jqXHR["status"] + ": " + result["message"]);
	});
};

// password reset
var request_reset_form = function() {
    var data = $("#request_reset_form").serializeObject();
    api_call("POST", "/api/user/forgot", data, function(result) {
        if (result["success"] == 1) {
            display_message("reset_msg", "success", result["message"]);
        } else {
            display_message("reset_msg", "danger", result["message"]);
        }
    }).fail(function(jqXHR, status, error) {
		var result = JSON.parse(jqXHR["responseText"]);
		display_message("reset_msg", "danger", "Error " + jqXHR["status"] + ": " + result["message"]);
    });
}

var reset_form = function() {
    var data = $("#reset_form").serializeObject();
    data["csrf_token"] = $.cookie("csrf_token");
    var url = window.location.href;
    var token = url.substr(url.lastIndexOf("/")+1);
    api_call("POST", "/api/user/forgot/" + token, data, function(result) {
        if (result["success"] == 1) {
            display_message("reset_msg", "success", result["message"], function() {
                location.href = "/login";
            });
        } else {
            display_message("reset_msg", "danger", result["message"]);
        }
    }).fail(function(jqXHR, status, error) {
		var result = JSON.parse(jqXHR["responseText"]);
		display_message("reset_msg", "danger", "Error " + jqXHR["status"] + ": " + result["message"]);
    });
}

// login page

var login_form = function() {
	var input = "#login_form input";
	var data = $("#login_form").serializeObject();
	api_call("POST", "/api/user/login", data, function(result) {
		if (result["success"] == 1) {
			location.href = "/profile";
		} else {
			display_message("login_msg", "danger", result["message"]);
		}
	}).fail(function(jqXHR, status, error) {
		var result = JSON.parse(jqXHR["responseText"]);
		display_message("login_msg", "danger", "Error " + jqXHR["status"] + ": " + result["message"]);
	});
};

// team page

var create_team = function() {
	var input = "#create_team input";
	var data = $("#create_team").serializeObject();
	api_call("POST", "/api/team/create", data, function(result) {
		if (result["success"] == 1) {
			location.reload(true);
		} else {
			display_message("create_team_msg", "danger", result["message"]);
		}
	}).fail(function(jqXHR, status, error) {
		var result = JSON.parse(jqXHR["responseText"]);
		display_message("create_team_msg", "danger", "Error " + jqXHR["status"] + ": " + result["message"]);
	});
};

var add_member = function() {
	var input = "#add_member input";
	var data = $("#add_member").serializeObject();
	api_call("POST", "/api/team/invite", data, function(result) {
		if (result["success"] == 1) {
			location.reload(true);
		}
	});
};
