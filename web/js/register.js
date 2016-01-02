$("#registration-form").on("submit", function(e) {
    e.preventDefault();
    register($("#name").val(), $("#username").val(), $("#password").val(), $("#password_confirm").val(), $("#email").val(), $("#g-recaptcha-response").val());
});

function register(name, username, password, password_confirm, email, captcha_response) {
    $("#register").attr("disabled", "disabled");
    $.post("/api/user/register", {
        name: name,
        username: username,
        password: password,
        password_confirm: password_confirm,
        email: email,
        captcha_response: captcha_response
    }, function(data) {
        $("#status").text(data.message);
        if (data.success == 1) {
            display_message("status", "success", "Success!", function() {$("#register").removeAttr("disabled")});
            // wait then redirect or whatever
        } else {
            display_message("status", "danger", data.message, function() {$("#register").removeAttr("disabled")});
            grecaptcha.reset();
        }
    });
}
