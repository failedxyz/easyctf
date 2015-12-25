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
	.when("/register", {
		templateUrl: "pages/register.html",
		controller: "mainController"
	})
	.when("/login", {
		templateUrl: "pages/login.html",
		controller: "mainController"
	});
	$locationProvider.html5Mode(true);
});
app.controller("mainController", function($scope) {

});