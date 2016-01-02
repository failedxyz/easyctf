$("#login-form").on("submit", function(e) {
    e.preventDefault();
    login($("#email").val(), $("#password").val());
});

function login(email, password) {
    $("#login").attr("disabled", "disabled");
    $.post("/api/user/login", {
        email: email,
        password: password
    }, function(data) {
        if (data.success == 1) {
            display_message("status", "success", "Success!", function() {$("#login").removeAttr("disabled");});
            // wait then redirect or whatever
        } else {
            display_message("status", "warning", data.message, function() {$("#login").removeAttr("disabled");});
        }
    });
}
