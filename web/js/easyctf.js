var app = angular.module("easyctf", [ "ngRoute" ]);
app.config(function($routeProvider, $locationProvider) {
	$routeProvider.when("/", {
		templateUrl: "pages/home.html",
		controller: "mainController"
	})
	.when("/about", {
		templateUrl: "pages/about.html",
		controller: "mainController"
	})
	.when("/scoreboard", {
		templateUrl: "pages/scoreboard.html",
		controller: "mainController"
	})
	.when("/learn", {
		templateUrl: "pages/learn.html",
		controller: "mainController"
	})
	.when("/register", {
		templateUrl: "pages/register.html",
		controller: "mainController"
	})
	.when("/login", {
		templateUrl: "pages/login.html",
		controller: "mainController"
	})
	.when("/profile", {
		templateUrl: "pages/profile.html",
		controller: "mainController"
	})
	.when("/logout", {
		templateUrl: "pages/blank.html",
		controller: "logoutController"
	});
	$locationProvider.html5Mode(true);
});

app.controller("mainController", ["$scope", "$http", function($scope, $http) {
	$scope.config = { navbar: { } };
	$.post("/api/user/status", function(result) {
		if (result["success"] == 1) {
			$scope.config.navbar.logged_in = result["logged_in"];
			$scope.config.navbar.username = result["username"];
		} else {
			$scope.config.navbar.logged_in = false;
		}
	}).fail(function() {
		$scope.config.navbar.logged_in = false;
	});
}]);

app.controller("logoutController", function() {
	$.post("/api/user/logout", function(result) {
		location.href = "/";
	});
});

function display_message(containerId, alertType, message, callback) {
	$("#" + containerId).html("<div class=\"alert alert-" + alertType + "\">" + message + "</div>");
	$("#" + containerId).hide().slideDown("fast", "swing", function() {
		window.setTimeout(function () {
			$("#" + containerId).slideUp("fast", "swing", callback);
		}, message.length * 75);
	});
};

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
	$.post("/api/user/register", data, function(result) {
		if (result["success"] == 1) {
			location.href = "/profile";
		} else {
			display_message("register_msg", "danger", result["message"])
		}
	});
};

// login page

var login_form = function() {
	var input = "#login_form input";
	var data = $("#login_form").serializeObject();
	$.post("/api/user/login", data, function(result) {
		if (result["success"] == 1) {
			location.href = "/profile";
		} else {
			display_message("login_msg", "danger", result["message"])
		}
	});
};