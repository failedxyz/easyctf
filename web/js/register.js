$("#registration-form").on("submit", function(e) {
    e.preventDefault();
    register($("#name").val(), $("#username").val(), $("#password").val(), $("#password_confirm").val(), $("#email").val());
});

function register(name, username, password, password_confirm, email) {
    $.post("/api/user/register", {
        name: name,
        username: username,
        password: password,
        password_confirm: password_confirm,
        email: email
    }, function(data) {
        $("#status").text(data.message);
        if (data.success == 1) {
            // wait then redirect or whatever
        }
    });
}
