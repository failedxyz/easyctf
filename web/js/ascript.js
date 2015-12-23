var app = angular.module('myApp', []);
app.controller('myCtrl', function($scope) {
    $scope.test = "Successful!";
    if($scope.test == "Successful!") {
        document.getElementById("result").style.color="#00FF00";
    }
});
