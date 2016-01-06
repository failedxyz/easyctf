function login_form(email, password) {
    $("#login").attr("disabled", "disabled");
    $.post("/api/user/login", {
        email: email,
        password: password
    }, function(data) {
        if (data.success == 1) {
            display_message("status", "success", "Success!", function() {
                $("#login").removeAttr("disabled");
                window.location = "#/account";
            });
        } else {
            display_message("status", "danger", data.message, function() {$("#login").removeAttr("disabled");});
        }
    });
}
