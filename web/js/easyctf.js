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
    })
    .when("/chat", {
        templateUrl: "pages/chat.html",
        controller: "mainController"
    })
    .when("/updates", {
        templateUrl: "pages/updates.html",
        controller: "mainController"
    })
    .when("/problems", {
        templateUrl: "pages/problems.html",
        controller: "mainController"
    })
    .when("/programming", {
        templateUrl: "pages/programming.html",
        controller: "mainController"
    })
    .when("/shell", {
        templateUrl: "pages/shell.html",
        controller: "mainController"
    })
    .when("/rules", {
        templateUrl: "pages/rules.html",
        controller: "mainController"
    })
    .when("/scoreboard", {
        templateUrl: "pages/scoreboard.html",
        controller: "mainController"
    });
    $locationProvider.html5Mode(true);
});
app.controller("mainController", function($scope) {

});

function display_message(containerId, alertType, message, callback) {
    $("#" + containerId).html('<div class="alert alert-' + alertType + '">' + message + '</div>');
    $("#" + containerId).hide().slideDown("fast", "swing", function() {
        window.setTimeout(function () {
            $("#" + containerId).slideUp("fast", "swing", callback);
        });
    }, 2000);
}

function load_navbar() {
    $.post("/api/user/status", {
    },
    function(data) {
        if (data.logged_in) {
            $("#logout").show();
            $("#account_link").show();
        } else {
            $("#login_link").show();
            $("#register_link").show();
        }
    });
}

$("#logout").click(function(e) {
    e.preventDefault();
    $.post("/api/user/logout", {
    }, function (data) {
        window.location = "/";
    });
})

$(document).ready( load_navbar() );
